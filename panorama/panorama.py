import cv2
import numpy as np
import serial
import time

info = {
    "dir": 0
}

def connectSer():
    ser = None

    for i in range(10):
        try:
            ser = serial.Serial(f'/dev/ttyACM{i}', 9600)
            print(f"Connected to /dev/ttyACM{i}")
            return ser
        except:
            ser = None
            print(f"Failed to connect to /dev/ttyACM{i}")
            time.sleep(0.05)
            pass
    if(ser is None):
        for i in range(10):
            try:
                ser = serial.Serial(f'/dev/ttyUSB{i}', 9600)
                print(f"Connected to /dev/ttyUSB{i}")
                return ser
            except:
                print(f"Failed to connect to /dev/ttyUSB{i}")
                time.sleep(0.05)
                pass
    return None


def createPanorama(ser):
    cap = cv2.VideoCapture(2)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    imCount = 20
    images = []
    ang = 0
    angStep = 180 // imCount
    time.sleep(2)
    ser.write(f"{180-ang}\n".encode())

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        
        while(ser.in_waiting > 0):
            line = ser.readline().decode('utf-8').strip()
            print(f"[{time.time():.4f}] Received: {line}")
            if line == "done":
                print("got")
                images.append(frame)
                ang += angStep
                ser.write(f"{180-ang}\n".encode())
                break
            

        cv2.imshow('Camera Feed', frame)

        if(ang >= 180+angStep/2):
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    imStitcher = cv2.Stitcher_create()
    status, panorama = imStitcher.stitch(images)

    if not status == cv2.Stitcher_OK:
        print("Error: Could not stitch images.")
        return None

    return panorama


if(__name__ == "__main__"):
    ser = connectSer()
    if(ser is None):
        print("Could not connect to serial port.")
        exit()

    panorama = createPanorama(ser)
    if(panorama is None):
        print("Error: Could not create panorama.")
        exit()

    cv2.imshow('Panorama', panorama)
    if cv2.waitKey(0) & 0xFF == ord('s'):
        cv2.imwrite('panorama.jpg', panorama)
    cv2.destroyAllWindows()
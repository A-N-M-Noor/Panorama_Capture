import cv2, math
from panorama import panorama
from panorama import overlay

def capture_mark(gps, heading):
    ser = panorama.connectSer()
    if(ser is None):
        print("Could not connect to serial port.")
        exit()

    pan = panorama.createPanorama()
    if(pan is None):
        print("Error: Could not create panorama.")
        exit()

    cv2.imwrite(f'lat_{gps['lat']},lon_{gps['lon']}__panorama.jpg', pan)

    img = overlay.overlayScale(img)
    img = overlay.overlayAng(img, offset=math.degrees(heading))
    cv2.imwrite(f'lat_{gps['lat']},lon_{gps['lon']}__panorama_marked.jpg', img)
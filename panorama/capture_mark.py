import cv2, math
import panorama
import overlay

def capture_mark(gps, heading):
    ser = panorama.connectSer()
    if(ser is None):
        print("Could not connect to serial port.")
        exit()

    pan = panorama.createPanorama(ser)
    if(pan is None):
        print("Error: Could not create panorama.")
        exit()

    pan = overlay.crop(pan)
    cv2.imwrite(f"lat_{gps['lat']},lon_{gps['lon']}__panorama.jpg", pan)

    img = overlay.overlayScale(pan)
    img = overlay.overlayAng(img, offset=math.degrees(heading))
    cv2.imwrite(f"lat_{gps['lat']},lon_{gps['lon']}__panorama_marked.jpg", img)


if(__name__ == "__main__"):
    gps = {
        'lat': 0,
        'lon': 0
    }
    heading = 0
    capture_mark(gps, heading)
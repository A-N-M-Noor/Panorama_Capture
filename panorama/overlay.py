import cv2, math, numpy as np

ang = {
    0: "N",
    90: "E",
    180: "S",
    270: "W"
}

def lerp(a, b, t):
    return a + (b-a)*t

def text(img, txt, x, y, sz, col=(0,255,0), bck = False):
    (text_width, text_height), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_TRIPLEX, sz, 1)
    x -= text_width // 2
    y += text_height // 2
    if bck:
        overlay = img.copy()
        cv2.rectangle(overlay, (int(x - 5), int(y - text_height - 5)), (int(x + text_width + 5), int(y + 5)), (255, 255, 255), -1)
        alpha = 0.6  # Transparency factor.
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    cv2.putText(img, txt, (int(x), int(y)), cv2.FONT_HERSHEY_TRIPLEX, sz, col, 1 if(sz < 1) else 2, cv2.LINE_AA)

def lineV(img, x, y, weight, col=(0,255,0)):
    cv2.line(img, (int(x), int(y)), (int(x), img.shape[0]), col, weight, cv2.LINE_AA)

def lineH(img, x, y, l, weight, col=(0,255,0)):
    cv2.line(img, (int(x-l), int(y)), (int(x), int(y)), col, weight, cv2.LINE_AA)

def getLineProp(infY, oneY, oneL, oneD, t):
    y = lerp(infY, oneY, t)
    l = lerp(0, oneL, t)
    d = oneD * ((oneY - infY)/(y-infY))

    return y, l, d

def overlayLine(_img, infY, oneY, oneL, oneD, sX, h, t, weight, offs, tSize, col = (0, 255, 0)):
    y, l, d = getLineProp(infY, oneY, oneL, oneD, t)
    lineH(_img, sX, y*h, l, weight, col)
    text(_img, f"{d:.0f}m" if d > 10 else f"{d:.1f}m", sX-l-offs, y*h, tSize, (0, 0, 100), True)

def overlayScale(img, frameSz = (640, 480), infY = 0.5, oneY = 0.9, oneL = 200, oneD = 4):
    _img = img.copy()
    w = img.shape[1]
    h = img.shape[0]
    sX = w

    overlayLine(_img, infY, oneY, oneL, oneD, sX, h, 0.4325, 1, 20, 0.4)
    overlayLine(_img, infY, oneY, oneL, oneD, sX, h, 0.5, 2, 40, 0.6, (0, 255, 100))
    overlayLine(_img, infY, oneY, oneL, oneD, sX, h, 0.6, 3, 60, 0.9, (0, 255, 255))
    overlayLine(_img, infY, oneY, oneL, oneD, sX, h, 0.75, 5, 80, 1.3, (0, 100, 255))
    overlayLine(_img, infY, oneY, oneL, oneD, sX, h, 1.0, 8, 100, 1.8, (0, 0, 100))

    return _img

def overlayAng(img, frameSz = (640, 480), offset = 0, rng = (0, 180)):
    w = img.shape[1]
    h = img.shape[0]
    fw = frameSz[0]
    fh = frameSz[1]

    bh = h * 0.25

    dr = rng[1] - rng[0]
    ratio = (w-fw//2) / dr

    _img = cv2.copyMakeBorder(img, 0, int(bh), 0, 0, cv2.BORDER_CONSTANT, None, [0]*3)

    

    res = 15
    resSm = 3
    for i in range(-360, 360+1):
        cAng = int(i + offset)
        if(cAng < 0):
            cAng += 360
        xp = ratio*(i-rng[0]) + fw//4
        if(cAng % res == 0):
            if(cAng in ang):
                text(_img, ang[cAng], xp, h*0.8+bh, 1.5)
            else:
                text(_img, f"{cAng:.0f}", xp, h*0.8+bh, 1)
            lineV(_img, xp, h*0.85+bh, 3)
        elif(i % resSm == 0):
            lineV(_img, xp, h*0.9+bh, 2)
    return _img

def crop(img):
    stitched_img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))

    gray = cv2.cvtColor(stitched_img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(gray, 0, 255 , cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areaOI = max(contours, key=cv2.contourArea)

    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(areaOI)
    cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    minRectangle = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, thresh_img)


    contours, _ = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    areaOI = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(areaOI)

    stitched_img = stitched_img[y:y + h, x:x + w]

    return stitched_img

if(__name__ == "__main__"):
    img = cv2.imread("panorama.jpg")
    if(img is None):
        print("No image")
        exit()
    
    img = crop(img)

    cv2.imshow('crop', img)

    img = overlayScale(img)
    img = overlayAng(img, offset=-90)
    cv2.imshow('overlay', img)
    if cv2.waitKey(0) & 0xFF == ord('s'):
        cv2.imwrite('panorama_marked.jpg', img)
    cv2.destroyAllWindows()

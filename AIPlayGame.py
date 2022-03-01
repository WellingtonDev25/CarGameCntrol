import  cv2
import numpy as np
#this module was created to simplify the coding process
import HandTrackingModule as htm
import time
import autopy

######################## getting size of screen
wScr,hScr = autopy.screen.size()

#define the size of camera window
wCan, hCan = 640,480
# frame is the variable using to create a little window where the mouse will scroll
frameR = 100
# smothening is used to adjust the usability of the mouse
smothening = 3
# these variables is also using to create a smothening in the mouse
plocX,plocY = 0,0
clocX,clocy = 0,0

cap = cv2.VideoCapture(0)

cap.set(3,wCan)
cap.set(4,hCan)

detector = htm.handDetector(trackCon=0.7,maxHands=1)
wScr,hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList,bbox = detector.findPosition(img)

    if len(lmList) !=0:
        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCan - frameR, hCan - frameR), (255,0,0), 2)

        if fingers[1]==1 and fingers[2] ==0:
            x3 = np.interp(x1,(frameR,wCan-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR, hCan-frameR), (0, hScr))

            #Smoothing
            clocX = plocX + (x3-plocX) / smothening
            clocY = plocY + (y3 - plocY) / smothening

            #autopy.mouse.move(wScr-x3,y3)
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
            plocX,plocY = clocX,clocY

            if fingers[0] == 0:
                autopy.mouse.click()
                print('click')


    cv2.imshow('Imagem',img)
    cv2.waitKey(1)

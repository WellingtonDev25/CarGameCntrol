import  cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

########################
wScr,hScr = autopy.screen.size()

wCan, hCan = 640,480
frameR = 100
########################
cap = cv2.VideoCapture(0)

cap.set(3,wCan)
cap.set(4,hCan)

detector = htm.handDetector(maxHands=1)
wScr,hScr = autopy.screen.size()

while True:
    #1- Find hand landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img,draw=False)

    # 2 -Get the tip of the index an middle fungers
    if len(lmList) !=0:
        x1,y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        #3 -check wich finger are up
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCan - frameR, hCan - frameR), (255, 0, 255), 2)
        #4 -only index finger in move mode
        if fingers[1]==1 and fingers[2] ==0:
            #5 -Convert cordenates
            #x3 = np.interp(x1,(0,wCan),(0,wScr))
            #y3 = np.interp(y1, (0, hCan), (0, hScr))
            x3 = np.interp(x1,(frameR,wCan-frameR),(0,wScr))
            y3 = np.interp(y1, (frameR, hCan-frameR), (0, hScr))
            #6 -Smoothen values
            #7 - move mouse
            autopy.mouse.move(wScr-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        #8 - both index and middle fingers are up: clicking mode
        #if fingers[1] == 1 and fingers[2] == 1:
        #9 - find dista#10 - click mouse if distance is short

        #1nce betwen fingers
        #1 - frame rate
        #12 - display
        #a1 = lmList[12][1]
        #b1 = lmList[10][1]
        #if fingers[1] ==1:
            #print(1)
        if fingers[2] == 1:
            print(2)
        if fingers[3] == 1:
            print(3)
        if fingers[4] == 1:
            print(4)
        if lmList[5] ==1:
            print(5)
            #if fingers[5]==0:
                #print('click')
                #autopy.mouse.click()

    cv2.imshow('Imagem',img)
    cv2.waitKey(1)

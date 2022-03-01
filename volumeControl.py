import cv2
import  time
import  numpy as np
import HandTrackingModule as htm
import  math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#################################
wCan,hCan = 540,480
################################

cap = cv2.VideoCapture(0)
cap.set(3,wCan)
cap.set(4,hCan)

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]


while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img)
    if len(lmList) !=0:
        #print(lmList[4],lmList[8])

        x1,y1 = lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        #calcular distancia entre os pontos
        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(92,152,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (92,152,0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(92,152,0),3)
        cv2.circle(img, (cx, cy), 15, (92,152,0), cv2.FILLED)

        lenth = math.hypot(x2-x1,y2-y1)
        #print(lenth)

        #hand rate 15 to 185
        # valume rate -65 to 0

        #proporção equivalente entre volume e hand
        vol = np.interp(lenth,[15,185],[minVol,maxVol])
        perc = np.interp(vol, [minVol, maxVol], [0, 100])

        texto = f'Vol: {int(vol)}%'

        cv2.putText(img,texto,(40,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)

        volume.SetMasterVolumeLevel(vol, None)

        if lenth<15:
            cv2.circle(img, (cx, cy), 15, (92,152,0), cv2.FILLED)

    cv2.imshow('Image', img)
    cv2 .waitKey(1)


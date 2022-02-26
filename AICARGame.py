import  cv2
import numpy as np
#this module was created to simplify the coding process
import HandTrackingModule as htm
import time
import autopy
import mediapipe as mp

#define the size of camera window
wCan, hCan = 640,480

cap = cv2.VideoCapture(0)

cap.set(3,wCan)
cap.set(4,hCan)

hands = mp.solutions.hands.Hands(False,2,.5,.5)
mpDwaw = mp.solutions.drawing_utils

while True:
    myhands = []
    success, img = cap.read()
    frameRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(frameRGB)
    #verificar se aparece alguma mão na imagem
    if results.multi_hand_landmarks != None:
        for handLandMarks in results.multi_hand_landmarks: #para cada mão que apaerce na imagem
            myHand = []
            #mpDwaw.draw_landmarks(img,handLandMarks) #desenhar as mãos

            for Landmark in handLandMarks.landmark: #para cada ponto da mão
                myHand.append((int(Landmark.x*wCan),int(Landmark.y*hCan)))

            myhands.append(myHand)
            posicao = 20 #ponto posição da mão
            cv2.circle(img,myhands[0][posicao],25,(255,0,255),-1)
            #print(len(myhands))

            if len(myhands) >=2:
                cv2.circle(img, myhands[1][posicao], 25, (0, 255, 255), -1)

            #print(myhands)

    cv2.imshow('Imagem',img)
    cv2.waitKey(1)

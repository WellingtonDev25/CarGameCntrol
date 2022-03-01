import  cv2
import numpy as np
import time
import autopy
import mediapipe as mp
import  math

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

            #print(len(myhands))
            if len(myhands) >=2:
                m1 = myhands[0]
                m2 = myhands[1]

                cv2.circle(img, myhands[0][posicao], 25, (0, 255, 255), -1)
                cv2.circle(img, myhands[1][posicao], 25, (255, 0, 255), -1)

                #print(f"mao 01 {myhands[0][posicao]}")
                #print(f"mao 02 {myhands[1][posicao]}")

                #print(f"mao 01 {m1[posicao]}")
                #print(f"mao 02 {m2[posicao]}")

                x1, y1 = m1[posicao][0], m1[posicao][1]
                x2, y2 = m2[posicao][0], m2[posicao][1]
                # calcular distancia entre os pontos
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                lenth = math.hypot(x2 - x1, y2 - y1)

                #print(lenth)
                if (lenth >=130) and (lenth <=270):
                    cv2.line(img, (x1, y1), (x2, y2), (92, 152, 0), 3)
                    cv2.circle(img, (cx, cy), 15, (92, 152, 0), cv2.FILLED)
                    # separar mão da essquerda e direita
                    if x1 <x2:
                        moEsqX = x1
                        moEsqY = y1
                        moDirX = x2
                        moDirY = y2
                    else:
                        moEsqX = x2
                        moEsqY = y2
                        moDirX = x1
                        moDirY = y1

                    cv2.putText(img,"ESQUERDA",(moEsqX-50,moEsqY+50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),3)
                    cv2.putText(img, "DIREITA", (moDirX - 50, moDirY + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)







            #print(myhands)

    cv2.imshow('Imagem',img)
    cv2.waitKey(1)

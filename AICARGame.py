import  cv2
from pynput.keyboard import Key, Controller
import mediapipe as mp
import  math
import time

#define the size of camera window
wCan, hCan = 640,480

cap = cv2.VideoCapture(0)

cap.set(3,wCan)
cap.set(4,hCan)

hands = mp.solutions.hands.Hands(False,2,.5,.5)
mpDwaw = mp.solutions.drawing_utils

setaDir = cv2.imread('seta direita.png')
setaEsq = cv2.imread('seta esquerda.png')

setaDir = cv2.resize(setaDir,(100,100))
setaEsq = cv2.resize(setaEsq,(100,100))

kb = Controller()

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
            posicao = 11 #ponto posição da mão (mindinho)

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
                if (lenth >=100) and (lenth <=250):
                    kb.press(Key.up)
                else:
                    kb.release(Key.up)

                if (lenth >= 200) and (lenth <= 400):
                    cv2.line(img, (x1, y1), (x2, y2), (92, 152, 0), 3)
                    cv2.circle(img, (cx, cy), 15, (92, 152, 0), cv2.FILLED)
                    # separar mão da essquerda e direita
                    if x1 >x2:
                        moEsqX = x1
                        moEsqY = y1
                        moDirX = x2
                        moDirY = y2
                    else:
                        moEsqX = x2
                        moEsqY = y2
                        moDirX = x1
                        moDirY = y1

                    print(moEsqY-moDirY)
                    diff = (moEsqY-moDirY) #direita sobe (positivo) esqueda sobe (negativo)
                    h_img, w_img, _ = img.shape
                    h_seta, w_seta, _ = setaDir.shape

                    center_y = int(h_img / 2)
                    center_x = int(w_img / 2)
                    # calculating from top, bottom, right and left
                    top_y = center_y - int(h_seta / 2)
                    left_x = center_x - int(w_seta / 2)
                    bottom_y = top_y + h_seta
                    right_x = left_x + w_seta

                    if diff >=100:
                        # adding setas to the image
                        #kb.release(Key.up)
                        kb.press(Key.left)
                        img[top_y - 150:bottom_y - 150, left_x - 250:right_x - 250] = setaEsq ## direita da tela
                    elif diff <=-100:
                        #kb.release(Key.up)
                        kb.press(Key.right)
                        img[top_y - 150:bottom_y - 150, left_x + 250:right_x + 250] = setaDir  # esquerda da tela
                    else:
                        kb.release(Key.left)
                        kb.release(Key.right)


                    cv2.putText(img,"ESQUERDA",(moEsqX-50,moEsqY+50),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 0, 0),3)
                    cv2.putText(img, "DIREITA", (moDirX - 50, moDirY + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)



            #print(myhands)

    cv2.imshow('Imagem',img)
    #cv2.imshow('Dir',setaDir)
    #cv2.imshow('Esq', setaEsq)

    cv2.waitKey(1)

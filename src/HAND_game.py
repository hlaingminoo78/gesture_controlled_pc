import cv2
from classes import imgprocess
from classes.HandTrackingModule import HandDetector
import mediapipe as mp
import numpy as np
import winsound

def game_mode():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4,720)

    #Importing all images
    imgBackground = cv2.imread("public/image/pong/Background.png")
    imgBall = cv2.imread("public/image/pong/Ball.png",cv2.IMREAD_UNCHANGED)
    imgBat1 = cv2.imread("public/image/pong/bat1.png",cv2.IMREAD_UNCHANGED)
    imgBat2 = cv2.imread("public/image/pong/bat2.png",cv2.IMREAD_UNCHANGED)
    imgGameOver = cv2.imread("public/image/pong/gameOver.png")

    #Hand Detector
    detector = HandDetector(detectionCon=0.8,maxHands=2)

    #Variables
    ballPos = [100,100]
    speedX = 20
    speedY = 20
    gameOver = False
    score = [0,0]
    frequency = 400
    duration = 10

    while True:
        _, img = cap.read()
        imgRaw = img.copy()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img,flipType=False)

        #Overlaying Background Image
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        #Check for hands
        if hands:
            for hand in hands:
                x,y,w,h = hand['bbox']
                h1,w1,_ = imgBat1.shape
                y1 = y-h1//2
                y1 = np.clip(y1,20,410)

                if hand['type']=="Left":
                    img = imgprocess.overlayPNG(img, imgBat1,(59,y1))
                    if 59 < ballPos[0] < 59+w1 and y1 < ballPos[1] < y1+h1:
                        winsound.Beep(frequency, duration)
                        speedX = -speedX
                        ballPos[0]+=30
                        score[0] += 1

                if hand['type']=="Right":
                    img = imgprocess.overlayPNG(img, imgBat2,(1195,y1))
                    if 1195-50 < ballPos[0] < 1195-30 and y1 < ballPos[1] < y1+h1:
                        winsound.Beep(frequency, duration)
                        speedX = -speedX
                        ballPos[1]-=30
                        score[1] += 1

        #Game Over
        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True

        if gameOver:
            img = imgGameOver
            cv2.putText(img, str(score[0]+score[1]).zfill(2), (585,360), cv2.FONT_HERSHEY_COMPLEX, 2.5, (200,0,200),5)
        else:
            #Move Ball
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                winsound.Beep(frequency, duration)
                speedY = -speedY
            ballPos[0] += speedX
            ballPos[1] += speedY

            #Draw Ball
            img = imgprocess.overlayPNG(img, imgBall,ballPos)

            #Scores
            cv2.putText(img, str(score[0]), (300,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255),5)
            cv2.putText(img, str(score[1]), (900,650), cv2.FONT_HERSHEY_COMPLEX, 3, (255,255,255),5)

        img[580:700,20:233] = cv2.resize(imgRaw, (213,120))

        cv2.imshow("Image",img)
        key = cv2.waitKey(1)
        if key == ord('r'):
            ballPos = [100,100]
            speedX = 20
            speedY = 20
            gameOver = False
            score = [0,0]
            imgGameOver = cv2.imread("public/image/pong/gameOver.png")
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


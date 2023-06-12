import cv2
from classes.HandTrackingModule import HandDetector
import mediapipe as mp
from time import sleep
import numpy as np
import classes.img_process_keyboard as ipk
from pynput.keyboard import Key,Controller

def keyboard_mode():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8,maxHands=1)
    keys = [["Q","W","E","R","T","Y","U","I","O","P","-"],
            ["A","S","D","F","G","H","J","K","L",";"],
            ["Z","X","C","V","B","N","M",",",".","/"," "]]

    finalText = ""
    keyboard = Controller()

    # def drawAll(img, buttonList):
    #     for button in buttonList:
    #         x,y = button.pos
    #         w,h = button.size
    #         ipk.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
    #                            20, rt=0)
    #         cv2.rectangle(img, button.pos , (x+w,y+h) , (255,0,255),cv2.FILLED)
    #         cv2.putText(img, button.text , (x+20,y+65), cv2.FONT_HERSHEY_PLAIN,
    #                 4, (255,255,255), 4 )
    #     return img

    def drawAll(img, buttonList):
        for button in buttonList:
            x,y = button.pos
            w,h = button.size
            alpha = 0.3
            overlay = img.copy()
            cv2.rectangle(overlay, (x,y), (x+w, y+h), (0,0,0), cv2.FILLED)
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,0), 2)
            cv2.putText(img, button.text, (x+30, y+60), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 2, cv2.LINE_AA)
        return img

    class Button():
        def __init__(self,pos,text,size=[85,85]):
            self.pos = pos
            self.text = text
            self.size = size

    buttonList = []

    for i in range(len(keys)):
        for j,key in enumerate(keys[i]):
            buttonList.append(Button([100*j+50, 100*i+50], key))

    while True:
        success, img = cap.read()
        img = cv2.flip(img,1) #Flip image
        hands, img = detector.findHands(img,flipType=False)
        img = drawAll(img, buttonList)

        if hands:
            lmList = hands[0]['lmList']
            bbox = hands[0]['bbox']

            for button in buttonList:
                x,y = button.pos
                w,h = button.size

                #change color while in range of keyboard
                if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h :
                    #changed darker color
                    cv2.rectangle(img, (x-5,y-5) , (x+w+5,y+h+5) , (0,0,0),cv2.FILLED)
                    cv2.putText(img, button.text , (x+20,y+65), cv2.FONT_HERSHEY_PLAIN,
                         4, (255,255,255), 4 )

                    l,_,_ = detector.findDistance((lmList[8][0],lmList[8][1]),
                                             (lmList[12][0],lmList[12][1]),img)

                    #when clicked
                    if l < 30:
                        if button.text == '-':
                            keyboard.press(Key.backspace)
                        else:
                            keyboard.press(button.text)
                        cv2.rectangle(img, button.pos , (x+w,y+h) , (0,255,0),cv2.FILLED)
                        cv2.putText(img, button.text , (x+20,y+65), cv2.FONT_HERSHEY_PLAIN,
                             4, (255,255,255), 4 )
                        #input texts
                        if button.text == '-':
                            finalText = finalText[:-1]
                        elif len(finalText) < 15:
                            if button.text == ' ':
                                finalText += ' '
                            else:
                                finalText += button.text
                        #finalText += button.text 
                        sleep(0.20)

        #output textbox                
        cv2.rectangle(img, (50,350) , (1140,450) , (255,255,255), cv2.FILLED)
        cv2.putText(img, finalText , (60,430), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0), 5)   

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


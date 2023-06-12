import cv2
import time
import pyperclip as clip

from classes.Constants import *
from classes.HandDetector import HandDetector
from classes.Util import *
from classes.GestureEventController import GestureEventController
from classes.ASLGestureClassifier import ASLGestureClassifier

def asl_mode():
#     variable initialization
    ##########################
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    hd = HandDetector()
    aslc = ASLGestureClassifier()
    pTime, cTime = 0, 0
    currentLetter = ''
    str_dict = {'currentStr': 'Hello World'}
    buttonList = {'Copy':(448, 332+14), 'Delete':(543, 332+14), 'Ques':(448, 332+58), 'Comma':(543, 332+58), 'Dot':(448, 332+102), 'Clear':(543,332+102)}
    buttonW, buttonH = 80, 32
    
#     function for string manipulation
    #########################
    def clearStr(dct): dct['currentStr']=''

    def addStr(dct, char): dct['currentStr']+=char

    def delStr(dct):
        if len(dct['currentStr'])>0: dct['currentStr']=dct['currentStr'][:-1]
    #########################
    
#     bind the events
    #########################
    gec = GestureEventController()
    gec.on('Copy', lambda x: clip.copy(str_dict['currentStr']))
    gec.on('Delete', lambda x: delStr(str_dict))
    gec.on('Ques', lambda x: addStr(str_dict, '?'))
    gec.on('Comma', lambda x: addStr(str_dict, ','))
    gec.on('Dot', lambda x: addStr(str_dict, '.'))
    gec.on('Clear', lambda x: clearStr(str_dict))
    #########################
        
#     mouse event listener callback function
    #########################
    def callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            for k, v in buttonList.items():
                if x > v[0] and x < v[0]+buttonW and y > v[1] and y < v[1]+buttonH:
                    gec.emit(k, [])
    #########################
    
#     set window name
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', wCam, hCam)
#     set mouse event handler
    cv2.setMouseCallback('Image', callback)
    
    while True:
        # read image
        success, img = cap.read()
    
        # flip the image
        img = cv2.flip(img,1)
    
        # set low part of image to empty white screen
        img[332:, :] = (227,227,227)

        # detect hand
        hd.findHands(img)
        hd.drawHands(img)
        crds, bbox, htype = hd.findPosition(img)
        
        if len(crds) > 0: currentLetter = aslc.classify(crds)
        else: currentLetter = ''
        
        # calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
        if htype == 'Left': label = 'LH'
        elif htype == 'Right': label = 'RH'
        else: label = ''
        
        # write frame rate text
        overlay_text_circle(img, str(int(fps)), (35,35), 20, 0.6)
        overlay_text_circle(img, label, (35,90), 20, 0.6)
        overlay_text_box(img, currentLetter, (555, 15), 70, 90, C_YELLOW, 0.6)
    
        # put textbox
        text_box(img, str_dict['currentStr'], (16, 332+14), 418, 120, 0.1, (255,255,255), (255,255,255), 1, (0,0,0))

        # draw buttons
        for k,v in buttonList.items():
            text_box(img, k, v, buttonW, buttonH, 0.1, (0,0,0), (0,0,0), 1, C_YELLOW)
        
        key = cv2.waitKey(1)
        
        # add new char when space is pressed
        if key == ord(' '): str_dict['currentStr'] += currentLetter
        # quit when q is pressed
        if key == ord('q'): break
        
        # quit on window exit button
        if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:break
            
        # show final image
        cv2.imshow("Image", img)

        # OxFF is equal to 0b11111111

    cap.release()
    cv2.destroyAllWindows()
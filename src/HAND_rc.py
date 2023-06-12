import cv2
import time
import numpy as np
import pyautogui as gui
import autopy

from classes.Constants import *
from classes.HandDetector import HandDetector
from classes.Util import *
from classes.GestureClassifier import GestureClassifier
from classes.GestureEventController import GestureEventController
from classes.RemoteGestureClassifier import RemoteGestureClassifier

def remotecontrol_mode():
    # variable initialization
    ##########################
    wCam, hCam = 640, 480  # 4:3
    # wCam, hCam = 1280, 720 # 16:9
    # wCam, hCam = 1920, 1080 # 16:9
    smoothening = 10
    frameXOffset = 100
    frameYTopOffset = 10
    frameYBottomOffset = 150
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime, cTime = 0, 0
    scale = 1
    screenW, screenH = autopy.screen.size()
    mousePos = {'currx': 0, 'curry': 0, 'prevx': 0, 'prevy': 0}
    indexDiff = {'curr': 0, 'prev': 0}
    hd = HandDetector(maxHands=2)
    rgc = RemoteGestureClassifier()
    #########################

    # functions for 1 hand
    #########################
    def moveMouse(crds):
        indexx, indexy = crds[INDEX_FINGER_TIP]['x'], crds[INDEX_FINGER_TIP]['y']
        mousePos['currx'] = np.interp(
            indexx, [frameXOffset, wCam-frameXOffset], [0, screenW])
        mousePos['curry'] = np.interp(
            indexy, [frameYTopOffset, hCam-frameYBottomOffset], [0, screenH])
        mousePos['currx'] = mousePos['prevx'] + \
            (mousePos['currx'] - mousePos['prevx']) / smoothening
        mousePos['curry'] = mousePos['prevy'] + \
            (mousePos['curry'] - mousePos['prevy']) / smoothening
#         gui.moveTo(mousePos['currx'], mousePos['curry'])
        autopy.mouse.move(mousePos['currx'], mousePos['curry'])
        mousePos['prevx'] = mousePos['currx']
        mousePos['prevy'] = mousePos['curry']

    def moveWindow(crds):
        moveMouse(crds)
        windows = gui.getWindowsAt(mousePos['currx'], mousePos['curry'])
        windows = list(filter(lambda x: x.title != 'Program Manager', windows))
        if len(windows) == 0:
            return
        windows[0].center = (mousePos['currx'], mousePos['curry'])

    def swipeWindow(crds):
        indexx, indexy = crds[INDEX_FINGER_TIP]['x'], crds[INDEX_FINGER_TIP]['y']
        mousePos['currx'] = indexx
        mousePos['curry'] = indexy
        if dist1(mousePos['currx'], mousePos['curry'], mousePos['prevx'], mousePos['prevy']) > two_index_diff_threshold:
            if mousePos['currx'] > mousePos['prevx']:
                gui.hotkey('alt', 'esc')
                win = gui.getActiveWindow()
                if not win == None and win.isMinimized:
                    win.maximize()
        mousePos['prevx'] = mousePos['currx']
        mousePos['prevy'] = mousePos['curry']

    # function for 2 hands
    #########################
    def maxminWindow(ary):
        crdsL, crdsR = ary[0], ary[1]
        lhx, lhy = crdsL[INDEX_FINGER_TIP]['x'], crdsL[INDEX_FINGER_TIP]['y']
        rhx, rhy = crdsR[INDEX_FINGER_TIP]['x'], crdsR[INDEX_FINGER_TIP]['y']
        indexDiff['curr'] = dist1(lhx, lhy, rhx, rhy)
        if abs(indexDiff['curr'] - indexDiff['prev']) > two_index_diff_threshold:
            windows = gui.getWindowsAt(mousePos['currx'], mousePos['curry'])
            windows = list(filter(lambda x: x.title !=
                           'Program Manager', windows))
            if indexDiff['curr'] < two_index_fingers_close_threshold:
                if len(windows) > 0:
                    windows[0].minimize()
            if indexDiff['curr'] > two_index_fingers_far_threshold:
                if len(windows) > 0:
                    windows[0].maximize()
        indexDiff['prev'] = indexDiff['curr']
    #########################

    # bind the events
    #########################
    gec = GestureEventController()
    gec.on('NO_1', lambda x: moveMouse(x))
    gec.on('NO_3', lambda x: moveWindow(x))
    gec.on('NO_4', lambda x: swipeWindow(x))
    gec.on('TWO_INDEX_FINGERS_UP', lambda x: maxminWindow(x))
    #########################

    # set window name
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Image', int(wCam*scale), int(hCam*scale))

    while True:
        success, img = cap.read()

        # flip the image
        img = cv2.flip(img, 1)

        hd.findHands(img)
        hd.drawHands(img)
        hands = hd.findAllPosition(img)

        if len(hands) == 1:
            crds = hands[0]['lmList']
            gName = rgc.classifyOne(crds)
            # print(gName)
            gec.emit(gName, crds)

        if len(hands) == 2:
            if hands[0]['type'] == 'Left':
                crdsL = hands[0]['lmList']
                crdsR = hands[1]['lmList']
            else:
                crdsL = hands[1]['lmList']
                crdsR = hands[0]['lmList']

            gName = rgc.classifyTwo(crdsL, crdsR)
            # print(gName)
            gec.emit(gName, [crdsL, crdsR])

        # calculate FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        # write frame rate text
        overlay_text_circle(img, str(int(fps)), (35, 35), 20, 0.6)

        cv2.rectangle(img, (frameXOffset, frameYTopOffset),
                      (wCam-frameXOffset, hCam-frameYBottomOffset), C_YELLOW, 2)

        key = cv2.waitKey(1)

        # quit when q is pressed
        if key == ord('q'):
            break

        # quit on window exit button
        if cv2.getWindowProperty('Image', cv2.WND_PROP_VISIBLE) < 1:
            break

        # show final image
        cv2.imshow("Image", img)

    cap.release()
    cv2.destroyAllWindows()

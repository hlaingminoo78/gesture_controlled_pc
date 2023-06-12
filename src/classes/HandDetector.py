import mediapipe as mp
import cv2


class HandDetector:
    def __init__(self, mode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = 1
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            mode, maxHands, modelComplexity, detectionCon, trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.result = None

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

    def drawHands(self, img):
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)

#     def drawBoundingBox(self, img):
#         img.flags.writeable = True
#         if self.result.multi_hand_landmarks:
#             for handLms in self.result.multi_hand_landmarks:

    def findPosition(self, img, handNo=0):
        lmList = []
        xList = []
        yList = []
        bbox = []
        htype = ''
        # calculate id and its landmarks(coordinates)
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            htype = self.result.multi_handedness[handNo].classification[0].label
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                # lmList.append([id, cx, cy])
                lmList.append({'x': cx, 'y': cy})

            # calculate bounding box
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            # return [{'lmList':lmList, 'bbox': bbox, 'type': htype}]
        return lmList, bbox, htype

    def findAllPosition(self, img):
        # calculate id and its landmarks(coordinates)
        allHands = []
        if self.result.multi_hand_landmarks:
            loops = len(self.result.multi_hand_landmarks) if len(
                self.result.multi_hand_landmarks) < self.maxHands else self.maxHands
            for i in range(loops):
                currentHand = {}
                lmList = []
                xList = []
                yList = []
                bbox = []
                myHand = self.result.multi_hand_landmarks[i]
                myHandType = self.result.multi_handedness[i]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    xList.append(cx)
                    yList.append(cy)
                    lmList.append({'x': cx, 'y': cy})

                # calculate bounding box
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax

                currentHand['lmList'] = lmList
                currentHand['bbox'] = bbox
                currentHand['type'] = myHandType.classification[0].label

                allHands.append(currentHand)

            # Left-0,Right-1
            if allHands[0]['type'] == 'Left':
                return allHands
            return allHands[::-1]
        return allHands

    def drawPosition(self, img, lmList):
        for id, cx, cy in lmList:
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return img

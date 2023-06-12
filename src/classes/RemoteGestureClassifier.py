from classes.GestureClassifier import GestureClassifier
from classes.Util import *


class RemoteGestureClassifier(GestureClassifier):
    def classifyOne(self, crds):
        # only work for right hand
        # rule 1: NO_1
        if self.thumbBend(crds) and self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'NO_1'
        # rule 2: NO_2
        if self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'NO_2'
        # rule 3: NO_3
        if self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'NO_3'
        # rule 4: NO_4
        if self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and self.ringFingerUp(crds) and self.pinkyFingerUp(crds):
            return 'NO_4'
        # rule 5: NO_5
        if not self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and self.ringFingerUp(crds) and self.pinkyFingerUp(crds):
            return 'NO_5'
        # rule : HAND_CLOSE
        # if (dist2(crds[THUMB_TIP],crds[INDEX_FINGER_TIP])+dist2(crds[INDEX_FINGER_TIP],crds[MIDDLE_FINGER_TIP])+dist2(crds[MIDDLE_FINGER_TIP],crds[RING_FINGER_TIP])+dist2(crds[RING_FINGER_TIP],crds[PINKY_TIP])) < hand_close_threshold:
        #     return 'HAND_CLOSE'
        return 'UNKNOWN'

    def classifyTwo(self, crdsL, crdsR):
        # rule : TWO_INDEX_FINGER_UP
        if self.thumbBendLeft(crdsL) and self.indexFingerUp(crdsL) and not self.middleFingerUp(crdsL) and not self.ringFingerUp(crdsL) and not self.pinkyFingerUp(crdsL):
            if self.thumbBend(crdsR) and self.indexFingerUp(crdsR) and not self.middleFingerUp(crdsR) and not self.ringFingerUp(crdsR) and not self.pinkyFingerUp(crdsR):
                return 'TWO_INDEX_FINGERS_UP'

        return 'UNKNOWN'

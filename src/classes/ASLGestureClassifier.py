from classes.Constants import *
from classes.Util import *
from classes.GestureClassifier import GestureClassifier


class ASLGestureClassifier(GestureClassifier):

    # do not change the order of if statements
    # TODO: change rule no
    def classify(self, crds):
        # rule 3: C
        if dist2(crds[THUMB_TIP], crds[PINKY_TIP]) > 70 and self.sideHand(crds) and not self.thumbBend(crds) and not self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'C'
        # rule 15: O
        if self.sideHand(crds) and not self.thumbBend(crds) and not self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'O'
        # rule 1: A
        # -all TIP must be under MCP except THUMB
        # -THUMB must point up
        if not self.thumbBend(crds) and not self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'A'
        # rule 2: B
        if self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and self.ringFingerUp(crds) and self.pinkyFingerUp(crds):
            return 'B'
        # rule 4: D
        if self.thumbBend(crds) and self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'D'
        # rule 4: E
        if self.thumbBend(crds) and not self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'E'
        # rule 4: F
        if self.thumbBend(crds) and not self.indexFingerUp(crds) and self.middleFingerUp(crds) and self.ringFingerUp(crds) and self.pinkyFingerUp(crds):
            return 'F'
        # rule 9: I
        if self.thumbBend(crds) and not self.indexFingerUp(crds) and not self.middleFingerUp(crds) and not self.ringFingerUp(crds) and self.pinkyFingerUp(crds):
            return 'I'
        # rule 21: U
        if self.thumbBend(crds) and self.indexFingerUp(crds) and self.middleFingerUp(crds) and dist2(crds[INDEX_FINGER_TIP], crds[MIDDLE_FINGER_TIP]) < index_middle_space and not self.ringFingerUp(crds) and not self.pinkyFingerUp(crds):
            return 'U'

        return ''

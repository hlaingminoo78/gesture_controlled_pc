from classes.Constants import *
class GestureClassifier:
    
    @staticmethod
    def thumbBend(crds):
        return crds[THUMB_TIP]['x'] > crds[THUMB_IP]['x']
    
    @staticmethod
    def thumbBendLeft(crds):
        return crds[THUMB_TIP]['x'] < crds[THUMB_IP]['x']
    
    @staticmethod
    def indexFingerUp(crds):
        return crds[INDEX_FINGER_TIP]['y'] < crds[INDEX_FINGER_PIP]['y']
    
    @staticmethod
    def middleFingerUp(crds):
        return crds[MIDDLE_FINGER_TIP]['y'] < crds[MIDDLE_FINGER_PIP]['y']
    
    @staticmethod
    def ringFingerUp(crds):
        return crds[RING_FINGER_TIP]['y'] < crds[RING_FINGER_PIP]['y']
    
    @staticmethod
    def pinkyFingerUp(crds):
        return crds[PINKY_TIP]['y'] < crds[PINKY_PIP]['y']
    
    @staticmethod
    def backHand(crds):
        # return (crds[THUMB_MCP]['x'] > crds[INDEX_FINGER_MCP]['x'] > crds[MIDDLE_FINGER_MCP]['x'] > crds[RING_FINGER_MCP]['x'] > crds[PINKY_MCP]['x'])
        return crds[MIDDLE_FINGER_MCP]['x'] > crds[RING_FINGER_MCP]['x']

    @staticmethod
    def frontHand(crds):
        # return (crds[THUMB_MCP]['x'] > crds[INDEX_FINGER_MCP]['x'] > crds[MIDDLE_FINGER_MCP]['x'] > crds[RING_FINGER_MCP]['x'] > crds[PINKY_MCP]['x'])
        return crds[MIDDLE_FINGER_MCP]['x'] < crds[RING_FINGER_MCP]['x']

    @staticmethod
    def sideHand(crds):
        return (
            abs(crds[INDEX_FINGER_MCP]['x'] - crds[MIDDLE_FINGER_MCP]['x']) +
            abs(crds[MIDDLE_FINGER_MCP]['x'] - crds[RING_FINGER_MCP]['x']) +
            abs(crds[RING_FINGER_MCP]['x'] - crds[PINKY_MCP]['x'])) < sidehand_threshold

    @staticmethod
    def leftHand(h):
        return True if h['type'] == 'Left' else False
    
    @staticmethod
    def rightHand(h):
        return True if h['type'] == 'Right' else False
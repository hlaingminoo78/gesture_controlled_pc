class GestureEventController:
    events = {}

    def emit(self, gesture, params):
        if gesture in self.events.keys():
            emitter = self.events[gesture]
            emitter(params)

    def on(self, gesture, callback):
        self.events[gesture] = callback

    def off(self, gesture):
        self.events.pop(gesture)

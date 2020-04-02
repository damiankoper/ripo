from .Event import Event

class SetInitConfigEvent(Event):
    def __init__(self, eventType, time: int):
        super(SetInitConfigEvent, self).__init__(self, eventType)

        self.initTime = time


from .Event import Event

class BallParam2ChangeEvent(Event):
    def __init__(self, param2):
        self.eventType = "ballParam2Change"
        self.param2 = param2
from .Event import Event

class BallParam1ChangeEvent(Event):
    def __init__(self, param1):
        self.eventType = "ballParam1Change"
        self.radius = param1
from .Event import Event

class BallLowerRadiusChangeEvent(Event):
    def __init__(self, radius):
        self.eventType = "ballLowerRadiusChange"
        self.radius = radius
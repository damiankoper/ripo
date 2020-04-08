from .Event import Event

class BallUpperRadiusChangeEvent(Event):
    def __init__(self, radius):
        self.eventType = "ballUpperRadiusChange"
        self.radius = radius
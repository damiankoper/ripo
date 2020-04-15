from .Event import Event

class BallMinDistChangeEvent(Event):
    def __init__(self, minDist):
        self.eventType = "ballMinDistChange"
        self.minDist = minDist
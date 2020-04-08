from .Event import Event

class BallThresholdChangeEvent(Event):
    def __init__(self, threshold):
        self.eventType = "ballThresholdChange"
        self.threshold = threshold
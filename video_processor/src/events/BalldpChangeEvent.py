from .Event import Event

class BalldpChangeEvent(Event):
    def __init__(self, dp):
        self.eventType = "balldpChange"
        self.radius = dp
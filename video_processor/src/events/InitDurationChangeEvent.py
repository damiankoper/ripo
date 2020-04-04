from .Event import Event

class InitDurationChangeEvent(Event):
    def __init__(self, time: int):
        self.eventType = "initDurationChange"
        self.initDuration = time


from .Event import Event


class RerunInitRequestEvent(Event):
    def __init__(self):
        self.eventType = "rerunInitRequest"

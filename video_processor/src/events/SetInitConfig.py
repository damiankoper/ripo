from .Event import Event

class SetInitConfig(Event):
    def __init__(self, eventType, time: int):
        super(SetInitConfig, self).__init__(self, eventType)

        self.initTime = time


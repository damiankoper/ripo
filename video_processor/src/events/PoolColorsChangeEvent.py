from .Event import Event

class PoolColorsChangeEvent(Event):
    def __init__(self, color_range):
        self.eventType = "poolColorsChange"
        self.pool_color_range = color_range


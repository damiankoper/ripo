import time
from .Ball import Ball
from .Cue import Cue


class PoolState:
    def __init__(self):
        self.balls = []
        self.cues = []

        self.sentAt = time.time()

    def toJson(self):
        return {'balls': [{'position': {'x': 0.5, 'y': 0.5}, 'type': 'SOLID', 'number': 6}], 'cues': []}

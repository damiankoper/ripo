import time
from .Ball import Ball
from .Cue import Cue


class PoolState:
    def __init__(self):
        self.balls = []
        self.cues = []

        self.sentAt = time.time()

    def toJson(self):
        return {
            'balls': [
                {
                    'position': {'x': i.position.x, 'y': i.position.y},
                    'type': i.type.value,
                    'number': i.number
                } for i in self.balls
            ],
            'cues': []
        }

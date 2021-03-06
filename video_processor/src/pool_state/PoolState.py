import time
from .Ball import Ball
from .Cue import Cue


class PoolState:
    def __init__(self):
        self.balls = []
        self.cues = []

    def toJson(self):
        return {
            'balls': [
                {
                    'position': {'x': i.position.x, 'y': i.position.y},
                    'type': i.type.value,
                    'number': i.number,
                    'detectedAt': i.detected_at
                } for i in self.balls
            ],
            'cues': [
                {
                    'positionStart': {'x': i.positionStart.x, 'y': i.positionStart.y},
                    'positionEnd': {'x': i.positionEnd.x, 'y': i.positionEnd.y},
                } for i in self.cues
            ]
        }

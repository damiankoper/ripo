from .Vector2i import Vector2i
from .Player import Player

class Cue:
    def __init__(self, positionStart: Vector2i, positionEnd: Vector2i, player: Player):
        self.positionStart = positionStart
        self.positionEnd = positionEnd
        self.player = player

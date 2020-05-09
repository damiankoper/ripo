from .Vector2i import Vector2i

class Cue:
    def __init__(self, positionStart: Vector2i, positionEnd: Vector2i):
        self.positionStart = positionStart
        self.positionEnd = positionEnd

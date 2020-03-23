from enum import Enum
from .Vector2i import Vector2i

class BallType(Enum):
    SOLID = "SOLID"
    STRIPED = "STRIPED"

class Ball:
    def __init__(self, number: int, position: Vector2i, ball_type: BallType):
        self.number = number
        self.position = position
        self.type = ball_type
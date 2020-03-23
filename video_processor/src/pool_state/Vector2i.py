from __future__ import annotations
import math

class Vector2i:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
  
    def add(self, v: Vector2i):
        return Vector2i(self.x + v.x, self.y + v.y)

    def multiply(self, a: int | Vector2i):
        if isinstance(a, Vector2i):
            return Vector2i(self.x * a.x, self.y * a.y)
        return Vector2i(self.x * a, self.y * a)

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
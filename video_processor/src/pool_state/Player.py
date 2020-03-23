from enum import Enum

class PlayerName(Enum):
    A = "A"
    B = "B"

class Player:
    def __init__(self, name: PlayerName, color: (int, int, int)):
        self.name = name
        self.color = color
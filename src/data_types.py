from dataclasses import dataclass
#from random import choice
from enum import Enum

class Color(Enum):
    Red = '\U0001F534'
    Green = '\U0001F7E2'
    White = '\u26AA'

def randomSymbol() -> str:
    return Color.White.value

@dataclass(frozen=True)
class Point:
    letter: str
    number: int

class Node:
    def __init__(self):
        self.neighbours: list[Node] = []
        self.symbol: str = randomSymbol()
        self.point: Point = Point("X", 0)


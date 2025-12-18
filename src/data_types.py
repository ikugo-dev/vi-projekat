from dataclasses import dataclass
from random import choice
from enum import Enum

class Color(Enum):
    Red = '\U0001F534'
    Green = '\U0001F7E2'
    White = '\u26AA'

def randomSymbol() -> str:
    return choice(list(Color)).value

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

class Node:
    def __init__(self):
        self.neighbours: list[Node] = []
        self.symbol = randomSymbol()


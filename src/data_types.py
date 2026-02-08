from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    Red = '\U0001F534'
    Green = '\U0001F7E2'
    White = '\u26AA'

@dataclass(frozen=True)
class Point:
    letter: str
    number: int

class Node:
    def has_value(self) -> bool:
        return self.symbol != Color.White.value

    def __init__(self, symbol: str = Color.White.value, point: Point = Point("X", 0)):
        self.neighbours: list[Node] = []
        self.symbol: str = symbol
        self.point: Point = point

def opposite_color(color: Color) -> Color:
    return Color.Red if color == Color.Green else Color.Green

class GameState:
    def __init__(self, starting_graph: dict[Point, Node], size: int, starting_color: Color):
        self.graph: dict[Point, Node] = starting_graph
        self.board_size: int = size
        self.current_player = starting_color
        self.main_player = Color.Green
        self.opponent = Color.Red
        self.turn = 0

    def next_turn(self):
        self.turn += 1
        self.current_player = opposite_color(self.current_player)

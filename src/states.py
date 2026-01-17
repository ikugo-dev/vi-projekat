import copy

from data_types import Node, Point, Color
from moves import get_available_moves

#state = graph
def set_new_state(graph: dict[Point, Node], letter: str, number: int, player: Color) -> dict[Point, Node]:
    graph[Point(letter, number)].symbol = str(player.value)
    return graph

def get_new_states(graph: dict[Point, Node], player: Color) -> list[dict[Point, Node]]:
    available_moves = get_available_moves(graph)

    new_states = []
    for point in available_moves:
        possible_graph = copy.deepcopy(graph)
        set_new_state(possible_graph, point.letter, point.number, player)
        new_states.append(possible_graph)

    return new_states if new_states!=[] else None


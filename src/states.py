import copy

from data_types import Node, Point, Color
from moves import get_available_moves
from heuristics import determine_heuristic

#state = graph
def set_new_state(graph: dict[Point, Node], point: Point, player: Color) -> None:
    graph[point].symbol = str(player.value)
# def set_new_state(graph: dict[Point, Node], letter: str, number: int, player: Color) -> dict[Point, Node]:
#     graph[Point(letter, number)].symbol = str(player.value)
#     return graph

def get_new_states(graph: dict[Point, Node], player: Color) -> list[dict[Point, Node]]:
    available_moves = get_available_moves(graph)

    new_states = []
    for point in available_moves:
        possible_graph = copy.deepcopy(graph)
        set_new_state(possible_graph, point, player)
        new_states.append(possible_graph)

    return new_states if new_states!=[] else []

# def min_state(graph: dict[Point, Node], player: Color, size:int) -> tuple[dict[Point, Node], int]:
#     state_heur_pairs = []
#     for state in get_new_states(graph, player):
#         heuristic = determine_heuristic(state, player, size)
#         state_heur_pairs.append((state, heuristic))
#
#     return min(state_heur_pairs, key=lambda x: x[1])
#
# def max_state(graph: dict[Point, Node], player: Color, size:int) -> tuple[dict[Point, Node], int]:
#     state_heur_pairs = []
#     for state in get_new_states(graph, player):
#         heuristic = determine_heuristic(state, player, size)
#         state_heur_pairs.append((state, heuristic))
#
#     return max(state_heur_pairs, key=lambda x: x[1])

import copy

from data_types import Color, GameState, Node, Point
from graph import create_starting_graph
from moves import get_available_moves

def set_new_state(old_state: GameState, point: Point) -> None:
    old_state.graph[point].symbol = str(old_state.current_player.value)
# def set_new_state(graph: dict[Point, Node], letter: str, number: int, player: Color) -> dict[Point, Node]:
#     graph[Point(letter, number)].symbol = str(player.value)
#     return graph

def get_possible_future_states(old_state: GameState) -> list[GameState]:
    available_moves = get_available_moves(old_state.graph)

    new_states: list[GameState] = []
    for point in available_moves:
        possible_state = copy_state(old_state)
        set_new_state(possible_state, point)
        new_states.append(possible_state)

    return new_states

def copy_state(state: GameState) -> GameState:
    new_nodes: dict[Point, Node] = {}
    for point, node in state.graph.items():
        new_nodes[point] = Node(node.symbol, point)

    for point, node in state.graph.items():
        new_nodes[point].neighbours = [new_nodes[n.point] for n in node.neighbours]

    return GameState(new_nodes, state.board_size, state.current_player)

def create_starting_state(player_one_first: bool, size: int) -> GameState:
    return GameState(create_starting_graph(size), size, Color.Green if player_one_first else Color.Red)


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

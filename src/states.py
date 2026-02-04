import copy

from matplotlib.pyplot import connect

from data_types import Node, Point, Color
from moves import get_available_moves
from src.bridges import has_winning_bridges, get_green_island_points
from src.heuristics import distances_from_islands, segment_connected_to_island


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

    return new_states if new_states!=[] else []



#issue: too broad in endgame
#numbers should be tweaked to encourage going forward in one direction rather than broadening in endgame

def determine_heuristic(graph: dict[Point, Node], player: Color, size:int) -> int:
    if has_winning_bridges(graph, player, get_green_island_points(size)):
        heuristic = 0
        return heuristic


    distances = distances_from_islands(graph, player.value, size)

    heuristics = []
    for distance in distances:

        try:
            segment_islands = distance[0]
        except KeyError:
            segment_islands = []

        heuristic = 0
        if segment_islands == []:

            for key in distance.keys():
                heuristic += key * len(distance[key])
            heuristics.append(heuristic)
            break

        for segment in segment_islands:

            if segment_islands == []:
                opposites = range(6)
            else:
                opposites = [(segment + 2) % 6, (segment + 3) % 6, (segment + 4) % 6]

            while opposites:
                opposite = opposites.pop()
                found = False
                for key in distance.keys():
                    if opposite in distance[key]:
                        found = True
                        heuristic += key
                if not found:
                    heuristic += 10

        heuristic += 6 - len(segment_islands)
        heuristics.append(heuristic)

    return min(heuristics)


def min_state(graph: dict[Point, Node], player: Color, size:int) -> tuple[dict[Point, Node], int]:
    state_heur_pairs = []
    for state in get_new_states(graph, player):
        heuristic = determine_heuristic(state, player, size)
        state_heur_pairs.append((state, heuristic))

    return min(state_heur_pairs, key=lambda x: x[1])

def max_state(graph: dict[Point, Node], player: Color, size:int) -> tuple[dict[Point, Node], int]:
    state_heur_pairs = []
    for state in get_new_states(graph, player):
        heuristic = determine_heuristic(state, player, size)
        state_heur_pairs.append((state, heuristic))

    return max(state_heur_pairs, key=lambda x: x[1])


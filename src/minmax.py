from data_types import Color, Node, Point
from states import determine_heuristic, get_new_states
from bridges import has_winning_bridges, get_green_island_points, get_red_island_points

INF = 10**9

# ---------------- TRANSPOSITION TABLE ----------------
TRANSPOSITION = {}

def hash_graph(graph):
    return tuple(
        graph[p].symbol for p in sorted(graph.keys(), key=lambda p:(p.letter, p.number))
    )

# ---------------- EVALUATION ----------------
def evaluate(graph, player, opponent, size):
    p = determine_heuristic(graph, player, size)
    o = determine_heuristic(graph, opponent, size)
    return o - p   # vece = bolje za AI

# ---------------- MINMAX ----------------
def minmax_alpha_beta(
    graph,
    player,
    opponent,
    depth,
    size,
    alpha=-INF,
    beta=INF,
    is_maximizing=True
):
    # Hash state
    key = (hash_graph(graph), depth, is_maximizing)
    if key in TRANSPOSITION:
        return TRANSPOSITION[key]

    # Island points
    if player == Color.Green:
        player_islands = get_green_island_points(size)
        opponent_islands = get_red_island_points(size)
    else:
        player_islands = get_red_island_points(size)
        opponent_islands = get_green_island_points(size)

    # Terminal
    if has_winning_bridges(graph, player, player_islands):
        return (100000, None)

    if has_winning_bridges(graph, opponent, opponent_islands):
        return (-100000, None)

    if depth == 0:
        value = evaluate(graph, player, opponent, size)
        TRANSPOSITION[key] = (value, None)
        return value, None

    current_player = player if is_maximizing else opponent
    states = get_new_states(graph, current_player)

    if not states:
        value = evaluate(graph, player, opponent, size)
        TRANSPOSITION[key] = (value, None)
        return value, None

    # MOVE ORDERING
    states.sort(
        key=lambda s: evaluate(s, player, opponent, size),
        reverse=is_maximizing
    )

    best_state = None

    if is_maximizing:
        best_value = -INF
        for state in states:
            value, _ = minmax_alpha_beta(
                state, player, opponent, depth - 1, size, alpha, beta, False
            )
            if value > best_value:
                best_value = value
                best_state = state
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        best_value = INF
        for state in states:
            value, _ = minmax_alpha_beta(
                state, player, opponent, depth - 1, size, alpha, beta, True
            )
            if value < best_value:
                best_value = value
                best_state = state
            beta = min(beta, value)
            if beta <= alpha:
                break

    TRANSPOSITION[key] = (best_value, best_state)
    return best_value, best_state

# ---------------- API ----------------
def find_move_difference(old_graph, new_graph):
    for point in old_graph:
        if old_graph[point].symbol != new_graph[point].symbol:
            return point
    return None

def get_best_move(graph, player, size, depth=3):
    opponent = Color.Red if player == Color.Green else Color.Green
    score, best_state = minmax_alpha_beta(graph, player, opponent, depth, size, True)

    if best_state is None:
        return None, score

    move = find_move_difference(graph, best_state)
    return move, score

def get_computer_move(graph, player, size, depth=3, verbose=True):
    move, score = get_best_move(graph, player, size, depth)

    if move is None:
        from moves import get_available_moves
        move = get_available_moves(graph)[0]

    if verbose:
        print(f"Računar igra: {move.letter}{move.number}  |  score = {score}")

    return move.letter, move.number

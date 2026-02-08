from data_types import Color, GameState, Point
from heuristics import determine_heuristic_for
from states import get_possible_future_states
from bridges import has_winning_bridges, get_green_island_points, get_red_island_points

INF = 10**9

# ---------------- TRANSPOSITION TABLE ----------------
TRANSPOSITION = {}

def hash_graph(graph):
    return tuple(
        graph[p].symbol for p in sorted(graph.keys(), key=lambda p:(p.letter, p.number))
    )

# ---------------- EVALUATION ----------------
def evaluate(state: GameState):
    p = determine_heuristic_for(state, state.main_player)
    o = determine_heuristic_for(state, state.opponent)
    return o - p   # vece = bolje za AI

# ---------------- MINMAX ----------------
def minmax_alpha_beta(
    state: GameState,
    depth: int,
    alpha: int = -INF,
    beta: int = INF,
    is_maximizing: bool =True
) -> tuple[int, GameState | None]:
    key = (hash_graph(state.graph), depth, is_maximizing)
    if key in TRANSPOSITION:
        return TRANSPOSITION[key]

    if state.main_player == Color.Green:
        player_islands = get_green_island_points(state.board_size)
        opponent_islands = get_red_island_points(state.board_size)
    else:
        player_islands = get_red_island_points(state.board_size)
        opponent_islands = get_green_island_points(state.board_size)

    # Terminal
    if has_winning_bridges(state.graph, state.main_player, player_islands):
        return (100000, None)

    if has_winning_bridges(state.graph, state.opponent, opponent_islands):
        return (-100000, None)

    if depth == 0:
        value = evaluate(state)
        TRANSPOSITION[key] = (value, None)
        return value, None

    future_tates = get_possible_future_states(state)

    if not future_tates:
        value = evaluate(state)
        TRANSPOSITION[key] = (value, None)
        return value, None

    future_tates.sort(
        key=lambda s: evaluate(s),
        reverse=is_maximizing
    )

    best_state = None

    if is_maximizing:
        best_value = -INF
        for state in future_tates:
            value, _ = minmax_alpha_beta(state, depth - 1, alpha, beta, False)
            if value > best_value:
                best_value = value
                best_state = state
            alpha = max(alpha, value)
            if beta <= alpha:
                break
    else:
        best_value = INF
        for state in future_tates:
            value, _ = minmax_alpha_beta(state, depth - 1, alpha, beta, True)
            if value < best_value:
                best_value = value
                best_state = state
            beta = min(beta, value)
            if beta <= alpha:
                break

    TRANSPOSITION[key] = (best_value, best_state)
    return best_value, best_state

def find_move_difference(old_state: GameState, new_state: GameState) -> Point | None:
    for point in old_state.graph:
        if old_state.graph[point].symbol != new_state.graph[point].symbol:
            return point
    return None

def get_best_move(state:GameState, depth:int =3) -> tuple[Point | None, int]:
    score, best_state = minmax_alpha_beta(state, depth, is_maximizing=True)

    if best_state is None:
        return None, score

    move = find_move_difference(state, best_state)
    return move, score

def get_computer_move(state: GameState, depth=3, verbose=True) -> Point:
    move, score = get_best_move(state, depth)

    if move is None:
        from moves import get_available_moves
        move = get_available_moves(state.graph)[0]

    if verbose:
        print(f"Computer plays: {move.letter}{move.number} | score = {score}")

    return move

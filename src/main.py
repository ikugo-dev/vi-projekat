from bridges import get_green_island_points, get_red_island_points, has_winning_bridges
from data_types import Color, Point, Node
# from moves import get_available_moves
from minmax import get_computer_move
from printer import print_state
from heuristics import determine_heuristic_for
from states import create_starting_state, set_new_state
def get_move(graph: dict[Point, Node]) -> tuple[str, int, bool]:
    try:
        move = input('Field: ').replace(" ", "")
        if len(move) < 2:
            raise(Exception)
        letter, number = move[0].upper(), int(move[1:])
        node = graph[Point(letter, number)]
        if node.symbol != str(Color.White.value):
            raise(Exception)
        return letter, int(number), True
    except Exception:
        return '', 0, False

def get_size(prompt: str) -> int:
    try:
        size = int(input(prompt))
        return size
    except Exception:
        return -1

def get_yn(prompt: str) -> bool:
    yn = input(prompt).lower()
    if yn == "n" or yn == "no":
        return False
    return True

def get_difficulty() -> int:
    try:
        depth = int(input("Enter computer difficulty (1-5, default = 3): "))
        if 1 <= depth <= 5:
            return depth
        return 3
    except:
        return 3

if __name__ == "__main__":
    valid_sizes = [5, 7, 9]
    size = get_size(f"Enter board size: ")
    while size not in valid_sizes:
        size = get_size(f"Wrong size! (Avalable {valid_sizes}):\nEnter size: ")

    computer_opponent: bool = get_yn("Do you want to play againts a computer? [Y/n]")
    difficulty = 0 # zbog unbound error
    if computer_opponent:
        difficulty = get_difficulty()
    player_one_first: bool = get_yn("Should player one go first? [Y/n]")

    green_island_points = get_green_island_points(size)
    red_island_points = get_red_island_points(size)
    # print(f'Green island points {green_island_points}')
    # print(f'Red island points {red_island_points}')

    state = create_starting_state(player_one_first, size)
    while True:

        print(f"\n{'='*50}")
        print(f"Turn: {state.turn}")
        print_state(state)

        player = state.current_player
        print(f"Turn for {player.value}: ")

        is_computer_turn = computer_opponent and ((player == Color.Red and player_one_first) or
                                                  (player == Color.Green and not player_one_first))

        move: Point
        if is_computer_turn:
            print("\nComputer is thinking...")
            move = get_computer_move(state, depth=difficulty, verbose=True)
        else:
            letter, number, good_move = get_move(state.graph)
            while not good_move:
                print('Wrong move!', end= ' ')
                letter, number, good_move = get_move(state.graph)
            move = Point(letter, number)

        # graph = set_new_state(graph, Point(letter, number), player)
        set_new_state(state, move)

        if (player == Color.Green):
            island_points = green_island_points
        else:
            island_points = red_island_points

        if (has_winning_bridges(state.graph, player, island_points)):
            print(f"\n{'='*50}")
            print(f"Player {player.value} has a winning bridge !!!")
            print(f"{'='*50}\n")
            print_state(state)
            break

        # moves = get_available_moves(graph)

        # Prikaz heuristike za oba igraca na svakih 5 poteza
        if state.turn % 5 == 0:
            green_heuristic = determine_heuristic_for(state, Color.Green)
            red_heuristic = determine_heuristic_for(state, Color.Red)
            print(f"Heuristic - Green: {green_heuristic}, Red: {red_heuristic}")

        state.next_turn()
    print("\n" + "=" * 50)

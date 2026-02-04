from bridges import bridges_for_color, get_green_island_points, get_red_island_points, has_winning_bridges
from data_types import Color, Point, Node
from graph import create_starting_graph 
# from moves import get_available_moves
from printer import print_graph
from src.heuristics import get_segments, distances_from_islands
from src.states import determine_heuristic, min_state
from states import set_new_state
import heuristics
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

if __name__ == "__main__":
    size = get_size("Enter size: ")
    valid_sizes = [5, 7, 9]
    while size not in valid_sizes:
        size = get_size(f"Wrong size! (Avalable {valid_sizes}):\nEnter size: ")
    graph = create_starting_graph(size)

    computer_opponent: bool = get_yn("Do you want to play againts a computer? [Y/n]")
    player_one_first: bool = get_yn("Should player one go first? [Y/n]")

    green_island_points = get_green_island_points(size)
    red_island_points = get_red_island_points(size)
    # print(f'Green island points {green_island_points}')
    # print(f'Red island points {red_island_points}')

    for turn in range(0, 999):
        if ((turn + int(player_one_first)) % 2 == 1): player = Color.Green
        else: player = Color.Red

        print(f"Turn: {turn}")
        print_graph(graph, size)
        print(f"Turn for {player.value}: ")

        letter, number, good_move = get_move(graph)
        while not good_move:
            print('Wrong move!', end= ' ')
            letter, number, good_move = get_move(graph)

        graph = set_new_state(graph, letter, number, player)

        if (player == Color.Green):
            island_points = green_island_points
        else:
            island_points = red_island_points

        if (has_winning_bridges(graph, player, island_points)):
            print(f"Player {player.value} has a winning bridge !!!")
            print_graph(graph, size)
            break


        #moves = get_available_moves(graph)
        #print(f"Available moves {moves} ")

        # if ((turn + int(player_one_first)) % 2 == 1):
        #     other_player = Color.Red
        # else:
        #     other_player = Color.Green
        # states = get_new_states(graph, other_player)
        # for state in states:
        #     print_graph(state, size)

        # distances = distances_from_islands(graph, Color.Green.value, size)
        # for distance in distances:
        #     print(distance)
        # print("heuristic", determine_heuristic(graph,Color.Green,size))

        # min_pair = min_state(graph, Color.Green, size)
        # print_graph(min_pair[0], size)
        # print("min heuristic", min_pair[1])
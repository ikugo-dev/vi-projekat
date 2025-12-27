from data_types import Color, Point, Node
from graph import create_starting_graph 
from printer import print_graph

def get_move(graph: dict[Point, Node]) -> tuple[str, int, bool]:
    try:
        move = input('Field: ').replace(" ", "")
        if len(move) != 2:
            raise(Exception)
        letter, number = move[0].upper(), int(move[1])
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

        graph[Point(letter, number)].symbol = str(player.value)

from bridges import get_green_island_points, get_red_island_points, has_winning_bridges
from data_types import Color, Point, Node
from graph import create_starting_graph 
from moves import get_available_moves
from printer import print_graph
from states import set_new_state
from minmax import get_computer_move

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
        depth = int(input("Unesite težinu računara (1-5, preporučeno 3): "))
        if 1 <= depth <= 5:
            return depth
        return 3
    except:
        return 3

if __name__ == "__main__":
    size = get_size("Unesite veličinu table: ")
    valid_sizes = [5, 7, 9]
    while size not in valid_sizes:
        size = get_size(f"Pogrešna veličina! (Dostupne: {valid_sizes}):\nUnesite veličinu: ")
    
    graph = create_starting_graph(size)

    computer_opponent: bool = get_yn("Da li želite da igrate protiv računara? [Y/n] ")
    
    if computer_opponent:
        difficulty = get_difficulty()
        print(f"\nRačunar će koristiti dubinu pretraživanja: {difficulty}")
        print("Što je veći broj, računar je pametniji (ali i sporiji)\n")
    
    player_one_first: bool = get_yn("Da li prvi igrač (Zeleni) počinje prvi? [Y/n] ")

    green_island_points = get_green_island_points(size)
    red_island_points = get_red_island_points(size)

    print("\n" + "=" * 50)
    print("Početak igre")
    print("=" * 50 + "\n")

    for turn in range(0, 999):
        # Odredjivanje trenutnog igraca
        if ((turn + int(player_one_first)) % 2 == 1): 
            player = Color.Green
        else: 
            player = Color.Red

        print(f"\n{'='*50}")
        print(f"Potez broj: {turn + 1}")
        print(f"{'='*50}")
        print_graph(graph, size)
        print(f"\nNa potezu je: {player.value} ({player.name})")

        # Provera da li je kompjuter na potezu
        is_computer_turn = computer_opponent and ((player == Color.Red and player_one_first) or
                                                   (player == Color.Green and not player_one_first))
        
        if is_computer_turn:
            print("\nRačunar razmišlja...")
            letter, number = get_computer_move(graph, player, size, depth=difficulty, verbose=True)
        else:
            # Covek igra
            letter, number, good_move = get_move(graph)
            while not good_move:
                print('Pogrešan potez!', end=' ')
                letter, number, good_move = get_move(graph)

        # Postavi novi potez
        graph = set_new_state(graph, letter, number, player)

        # Odredjivanje island points za trenutnog igraca
        if (player == Color.Green):
            island_points = green_island_points
        else:
            island_points = red_island_points

        # Provera pobede
        if (has_winning_bridges(graph, player, island_points)):
            print(f"\n{'='*50}")
            print(f"Kraj igre, igrač {player.value} ({player.name}) je pobedio!")
            print(f"{'='*50}\n")
            print_graph(graph, size)
            break

        moves = get_available_moves(graph)
        print(f"\nPreostalo poteza: {len(moves)}")

        # Prikaz heuristike za oba igraca na svakih 5 poteza
        if turn % 5 == 0:
            green_heuristic = 0
            red_heuristic = 0
            from states import determine_heuristic
            try:
                green_heuristic = determine_heuristic(graph, Color.Green, size)
                red_heuristic = determine_heuristic(graph, Color.Red, size)
                print(f"Heuristika - Zeleni: {green_heuristic}, Crveni: {red_heuristic}")
            except:
                pass

    print("\n" + "=" * 50)

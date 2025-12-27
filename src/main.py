import string

from numpy.f2py.auxfuncs import throw_error

from data_types import Color, Point, Node
import printer


HEX_DIRECTIONS = [
    (0, -1),
    (0,  1),
    (-1,  0),
    (1,  0),
    (-1,  -1),
    (1, 1)
]

def build_grid(size: int) -> dict[str, list[int]]:
    grid : dict[str, list[int]] = {string.ascii_uppercase[x] : []  for x in range(size*2-1)}
    low_end = 0
    high_end = size

    for x in range(size*2-1):

        #print(low_end, high_end)
        for y in range(low_end, high_end):
            grid[string.ascii_uppercase[y]].append(x+1)
        if x < size-1 : high_end += 1
        else: low_end += 1

        #print(grid)
    return grid



def build_graph(points: list[Point]) -> dict[Point, Node]:
    nodes : dict[Point, Node] = {}
    for point in points:
        nodes[point] = Node()
        nodes[point].point = point

    for point, node in nodes.items():
        for dir in HEX_DIRECTIONS:
            neighbor_point = Point(
                string.ascii_uppercase[ord(point.L)- ord('A') + dir[0]],
                point.N + dir[1]
            )
            if neighbor_point in points:
                node.neighbours.append(nodes[neighbor_point])
    return nodes

def generate_points(size: int, grid: dict[str, list[int]]) -> list[Point]:
    points : list[Point] = []
    for x in range(size*2-1):
        letter = string.ascii_uppercase[x]
        for y in grid[letter]:
            points.append(Point(letter, y))
    return points

def get_move(graph: dict[Point, Node]) -> tuple[str, int, bool]:
    try:
        letter, number = input('Field: ').split(" ")
        node = graph[Point(L = letter, N = int(number))]
        if node.symbol != str(Color.White.value):
            raise(Exception)
        else:
            return letter, int(number), True
    except Exception as e:
        return '', 0, False

def get_size() -> int:
    try:
        size = int(input("Enter size: "))
        return size
    except Exception as e:
        return -1


if __name__ == "__main__":

    size = get_size()
    while size not in [5, 7, 9]:
        size = int(input("Wrong size! Enter size: "))

    hex_points = generate_points(size, build_grid(size))
    graph = build_graph(hex_points)

    #printer.debug(graph)
    #printer.graph(graph, size)

    for turn in range(1, 999):
        if (turn % 2 == 1): player = Color.Green
        else: player = Color.Red

        print(f"Turn: {turn}")
        printer.graph(graph, size)
        print(f"Turn for {player.value}: ")


        letter, number, good_move = get_move(graph)
        while not good_move:
            print('Wrong move!', end= ' ')
            letter, number, good_move = get_move(graph)

        graph[Point(L=letter, N=int(number))].symbol = str(player.value)

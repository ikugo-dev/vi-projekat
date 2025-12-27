import string

from data_types import Point, Node

HEX_DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
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

def generate_points(size: int, grid: dict[str, list[int]]) -> list[Point]:
    points : list[Point] = []
    for x in range(size*2-1):
        letter = string.ascii_uppercase[x]
        for y in grid[letter]:
            points.append(Point(letter, y))
    return points

def build_graph(points: list[Point]) -> dict[Point, Node]:
    nodes : dict[Point, Node] = {}
    for point in points:
        nodes[point] = Node()

    for point, node in nodes.items():
        for dir in HEX_DIRECTIONS:
            neighbor_point = Point(
                string.ascii_uppercase[ord(point.letter)-ord('A') + dir[0]],
                point.number + dir[1]
            )
            if neighbor_point in points:
                node.neighbours.append(nodes[neighbor_point])
    return nodes


def create_starting_graph(size: int) ->  dict[Point, Node]:
    grid = build_grid(size)
    hex_points = generate_points(size, grid)
    graph = build_graph(hex_points)
    return graph

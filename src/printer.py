from data_types import Point, Node

def graph(graph: dict[Point, Node], radius: int) -> None:
    diameter = (radius - 1) * 2
    width  = diameter * 2 + 1
    height = diameter + 1

    projected = [(p.x - p.z, p.y, n.symbol) for p, n in graph.items()]
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for x, y, symbol in projected:
        gx = x + diameter
        gy = diameter // 2 - y
        grid[gy][gx] = symbol

    print("\n".join("".join(row) for row in grid))

def debug(graph: dict[Point, Node]) -> None:
    for point, node in graph.items():
        print(f"{point}: {node}")
        for neighbour in node.neighbours:
            print(f"-> {neighbour}, ")
        print("\n")

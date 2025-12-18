from data_types import Point, Node

def points(points: list[Point], radius: int) -> None:
    diameter = (radius - 1) * 2
    width  = diameter * 2 + 1
    height = diameter + 1

    projected = [(p.x - p.z, p.y) for p in points]
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for x, y in projected:
        gx = x + diameter
        gy = diameter // 2 - y
        grid[gy][gx] = "X"

    print("\n".join("".join(row) for row in grid))

def graph(graph: dict[Point, Node]) -> None:
    for _, node in graph.items():
        print(f"{node.point}: ")
        for neighbour in node.neighbours:
            print(f"-> {neighbour.point}, ")
        print("\n")

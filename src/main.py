from data_types import Point, Node
import printer

HEX_DIRECTIONS = [
    Point( 1, -1,  0),
    Point( 1,  0, -1),
    Point( 0,  1, -1),
    Point(-1,  1,  0),
    Point(-1,  0,  1),
    Point( 0, -1,  1),
]

def build_graph(points: list[Point]) -> dict[Point, Node]:
    nodes = {point: Node() for point in points}
    for point, node in nodes.items():
        for dir in HEX_DIRECTIONS:
            neighbor_point = Point(
                point.x + dir.x,
                point.y + dir.y,
                point.z + dir.z
            )
            if neighbor_point in nodes:
                node.neighbours.append(nodes[neighbor_point])
    return nodes

def generate_hex_points(radius: int) -> list[Point]:
    points = []
    for x in range(-(radius-1), radius):
        for y in range(-(radius-1), radius):
            z = -(x + y)
            if -radius < z < radius:
                points.append(Point(x, y, z))
    return points


if __name__ == "__main__":
    radius = int(input("Enter radius: "))
    hex_points = generate_hex_points(radius)
    graph = build_graph(hex_points)

    printer.debug(graph)
    printer.graph(graph, radius)

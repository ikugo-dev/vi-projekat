from data_types import Color, Node, Point
import string

def has_path_same_color(start_node: Node, target_node: Node) -> bool:
        
    target_color = start_node.symbol
    
    if target_node.symbol != target_color: return False

    visited : set[Node] = set()
    stack = [start_node]

    while stack:
        current = stack.pop()

        if current == target_node: return True

        if current not in visited:
            visited.add(current)
            
            for neighbor in current.neighbours:
                if neighbor.symbol == target_color and neighbor not in visited:
                    stack.append(neighbor)

    return False

def get_green_island_points(size: int) -> list[list[Point]]:

    center_left : list[Point] = []
    for i in range (size // 2 + 1):
        center_left.append(Point('A', i + 1))

    top_left : list[Point] = []
    for i in range(size // 2, size):
        letter = string.ascii_uppercase[i]
        top_left.append(Point(letter, 1))

    bottom_left : list[Point] = []
    for i in range(size // 2 + 1):
        letter = string.ascii_uppercase[i]
        bottom_left.append(Point(letter, size + i))

    top_right : list[Point] = []
    for i in range(size // 2 - 1, size - 1):
        letter = string.ascii_uppercase[size + i]
        top_right.append(Point(letter, i + 2))

    bottom_right : list[Point] = []
    for i in range(size // 2 + 1):
        letter = string.ascii_uppercase[size + i - 1]
        bottom_right.append(Point(letter, size * 2 - 1))

    center_right : list[Point] = []
    for i in range (size + size // 2, size * 2):
        last_letter = string.ascii_uppercase[size * 2 - 2]
        center_right.append(Point(last_letter, i))

    return [ center_left, top_left, top_right, center_right, bottom_right, bottom_left]
    
def get_red_island_points(size: int) -> list[list[Point]]:

    center_left : list[Point] = []
    for i in range (size // 2, size):
        center_left.append(Point('A', i + 1))

    top_left : list[Point] = []
    for i in range(size // 2 + 1):
        letter = string.ascii_uppercase[i]
        top_left.append(Point(letter, 1))

    bottom_left : list[Point] = []
    for i in range(size // 2, size):
        letter = string.ascii_uppercase[i]
        bottom_left.append(Point(letter, size + i))

    top_right : list[Point] = []
    for i in range(size // 2 + 1):
        letter = string.ascii_uppercase[size + i - 1]
        top_right.append(Point(letter, i + 1))

    bottom_right : list[Point] = []
    for i in range(size // 2, size):
        letter = string.ascii_uppercase[size + i - 1]
        bottom_right.append(Point(letter, size * 2 - 1))

    center_right : list[Point] = []
    for i in range (size, size + size // 2 + 1):
        last_letter = string.ascii_uppercase[size * 2 - 2]
        center_right.append(Point(last_letter, i))

    return [ center_left, top_left, top_right, center_right, bottom_right, bottom_left]

def opposite_sides(island_points: list[list[Point]], side_index: int) -> list[list[Point]]:
    opposite_indices = [
        (side_index + 2) % 6,
        (side_index + 3) % 6,
        (side_index + 4) % 6,
    ]
    return [island_points[i] for i in opposite_indices]

def has_winning_bridges(
    graph: dict[Point, Node],
    color : Color,
    island_points: list[list[Point]],
) -> bool:

    def are_islands_connected(island1: list[Point], island2: list[Point]) -> bool:
        for p1 in island1:
            for p2 in island2:
                node1, node2 = graph[p1], graph[p2]

                if node1.symbol != color.value: continue 
                if node1.symbol != node2.symbol: continue
                if not has_path_same_color(node1, node2): continue
                return True # minimalna duzina za most sa susedne strane je sama po sebi 7
        return False 

    for i, island in enumerate(island_points):
        #Win case 1: Opposing island
        opp_island = island_points[(i + 3) % 6]
        if (are_islands_connected(island, opp_island)): return True

        #Win case 2: Both of the sides of the opposing island
        opp_side1 = island_points[(i + 2) % 6]
        if not are_islands_connected(island, opp_side1): continue

        opp_side2 = island_points[(i + 4) % 6]
        if not are_islands_connected(island, opp_side2): continue 

        return True

    return False

def bridges_for_color(graph: dict[Point, Node], color : Color, island_points: list[list[Point]]):
    results : list[tuple[Point, Point]] = []
    for i in range(len(island_points)):
        island1 = island_points[i]
        for j in range(i + 1, len(island_points)):
            island2 = island_points[j]
            for p1 in island1:
                for p2 in island2:
                    node1, node2 = graph[p1], graph[p2]
                    
                    if node1.symbol != color.value: continue 
                    if node1.symbol != node2.symbol: continue
                    if not has_path_same_color(node1, node2): continue

                    results.append((p1, p2))
    return results

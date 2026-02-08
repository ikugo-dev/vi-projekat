from data_types import Color, GameState, Node, Point
from bridges import get_green_island_points, get_red_island_points

def distances_from_islands(state: GameState, player: Color) -> list[dict[int, list[int]]]:
    segments = get_segments(state, player)

    islands = get_islands_for(player, state.board_size)

    distances, _ = init_distances_from_segments(islands, player.value, segments)
    return distances

def get_islands_for(player: Color, board_size: int) -> list[list[Point]]:
    islands :list[list[Point]]
    if player == Color.Red:
        islands = get_red_island_points(board_size)
    else:
        islands = get_green_island_points(board_size)
    return [list(island) for island in islands]

def minimal_distances_from_islands(state: GameState, player: Color) -> list[dict[int, int]]:
    segments = get_segments(state, player)

    islands = get_islands_for(player, state.board_size)

    distances, minimal_distances = init_distances_from_segments(islands, player.value, segments)
    minimal_distances = determine_distances_from_segment(islands, player.value, segments, distances, minimal_distances)

    return minimal_distances

def get_segments(state: GameState, player: Color) -> list[list[Node]]:
    segments: list[list[Node]] = []
    visited: set[Point] = set()
    for point, node in state.graph.items():
        if point in visited:
            continue
        if node.symbol != player:
            continue

        segment: list[Node] = []
        stack: list[Node] = [node]
        visited.add(point)
        while stack:
            current = stack.pop()
            segment.append(current)

            for neighbour in current.neighbours:
                neighbour_point = neighbour.point
                if neighbour_point in visited:
                    continue
                if neighbour.symbol == player:
                    visited.add(neighbour_point)
                    stack.append(neighbour)
        segments.append(segment)
    return segments

def segment_connected_to_island(segment: list[Node], island: list[Point], color:str) -> bool:
    for node in segment:
        if (node.symbol == color or node.symbol == Color.White.value) and node.point in island:
            return True
    return False

def init_distances_from_segments(islands: list[list[Point]], color: str, segments: list[list[Node]]) -> tuple[list[dict[int, list[int]]], list[dict[int, int]]]:
    distances = []
    minimal_distances = []
    for _ in range(len(segments)):
        d = dict()
        for i in range(6):
            d[i] = 100
        minimal_distances.append(d)
    #each element in distances[] corresponds to one segment and is a dict.
    #each dict key is distance to an island from the segment and value is a list of the island indexes
    #distance is 0 => segment is connected to the island.
    for segment_index, segment in enumerate(segments):
        segment_distance = dict()
        for island_index in range(6):
            island = islands[island_index]
            if segment_connected_to_island(segment, island, color):
                segment_distance.setdefault(0, []).append(island_index)

                minimal_distances[segment_index][island_index] = 0
                #all segment points and their neighbours are added to the island
                #this is used to check if a stone is directly next to the island or the segment connected to the island
                #so essentially we are expanding the island up until its borders

                for node in segment:
                    if node.point not in island:
                        island.append(node.point)

                    for neighbour in node.neighbours:
                        if neighbour.point not in island:
                            island.append(neighbour.point)

        distances.append(segment_distance)
    return distances, minimal_distances

def determine_distances_from_segment(islands: list[list[Point]], color: str, segments: list[list[Node]], distances: list[dict[int, list[int]]], minimal_distances: list[dict[int, int]]) ->  list[dict[int, int]]:
    #searching by breadth if segment is connected to island
    for segment_index, segment in enumerate(segments):
        visited = set()
        segment_distance = distances[segment_index]
        neighbour_segment = []

        #the belt around the segment is treated like its own segment.
        #this belt is distant from the segment by 1 stone
        for node in segment:
            for neighbour in node.neighbours:
                if neighbour.point not in visited and (neighbour.symbol == Color.White.value):
                    neighbour_segment.append(neighbour)
                    visited.add(neighbour.point)

        distance = 1
        while neighbour_segment:
            #print ("-----------distance " + str(distance) + "---------------")
            #print("neighbour segment", list(map(lambda x: x.point, neighbour_segment)))

            for island_index in range(6):
                island = islands[island_index]

                if distance < minimal_distances[segment_index][island_index] and segment_connected_to_island(neighbour_segment, island, color):
                    segment_distance.setdefault(distance, []).append(island_index)

                    minimal_distances[segment_index][island_index] = distance

            next_neighbour_segment = []
            # the belt around the segment is treated like its own segment.
            # this belt is distant from the segment by int(distance) amount of stones
            for node in neighbour_segment:
                for neighbour in node.neighbours:

                    if neighbour.point not in visited and (neighbour.symbol == Color.White.value):
                        next_neighbour_segment.append(neighbour)
                        visited.add(neighbour.point)

            neighbour_segment = next_neighbour_segment
            distance += 1
    return minimal_distances

#issue: too broad in endgame
#numbers should be tweaked to encourage going forward in one direction rather than broadening in endgame

def determine_heuristic_for(state: GameState, player: Color) -> int:
    # if has_winning_bridges(graph, player, get_green_island_points(size)):
    #     heuristic = 0
    #     return heuristic

    distances = distances_from_islands(state, player)
    if not distances:
        return 1000

    heuristics = []
    for distance in distances:
        segment_islands = distance.get(0, [])
        if segment_islands == []:
            heuristic = unconnected_heuristic(distance)
        else:
            heuristic = connected_heuristic(distance, segment_islands)
        heuristics.append(heuristic)
    return min(heuristics)

def unconnected_heuristic(distance: dict[int, list[int]]) -> int:
    heuristic = 0
    for key in distance.keys():
        heuristic += key * len(distance[key])
    return heuristic

def connected_heuristic(distance: dict[int, list[int]], segment_islands: list[int]) -> int:
    heuristic = 0
    for segment in segment_islands:
        opposites = [(segment + 2) % 6, (segment + 3) % 6, (segment + 4) % 6]
        while opposites:
            opposite = opposites.pop()
            found = False
            for key in distance.keys():
                if opposite in distance[key]:
                    found = True
                    heuristic += key
            if not found:
                heuristic += 10
    heuristic += 6 - len(segment_islands)
    return heuristic

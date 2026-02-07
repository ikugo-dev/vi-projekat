from data_types import Color, Node, Point
from bridges import get_green_island_points, get_red_island_points

def distances_from_islands(graph: dict[Point, Node], color: str, size:int) -> list[dict[int, list[int]]]:
    segments = get_segments(graph, color)
    distances : list[dict[int, list[int]]] = []
    #each element in distances[] corresponds to one segment and is a dict.
    #each dict key is distance to an island from the segment and value is a list of the island indexes
    #distance is 0 => segment is connected to the island.

    if color == Color.Red.value:
        islands = get_red_island_points(size)
    elif color == Color.Green.value:
        islands = get_green_island_points(size)
    else: return []

    minimal_distances : list[dict[int, int]] = []
    for j in range(len(segments)):
        d : dict[int, int] = dict()
        for i in range(6):
            d[i] = 100
        minimal_distances.append(d)

    segment_index = 0
    for segment in segments:
        segment_distance : dict[int, list[int]] = dict()

        for island_index in range(6):

            island = islands[island_index]

            if segment_connected_to_island(segment, island, color):

                try:
                    segment_distance[0].append(island_index)
                except KeyError:
                    segment_distance[0] = [island_index]

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
        segment_index+=1



    #searching by breadth if segment is connected to island

    segment_index = 0
    for segment in segments:

        visited : set[Point] = set()
        segment_distance = distances[segment_index]
        neighbour_segment : list[Node] = []

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

                    try:
                        segment_distance[distance].append(island_index)
                    except KeyError:
                        segment_distance[distance] = [island_index]

                    minimal_distances[segment_index][island_index] = distance

            next_neighbour_segment : list[Node] = []
            # the belt around the segment is treated like its own segment.
            # this belt is distant from the segment by int(distance) amount of stones
            for node in neighbour_segment:
                for neighbour in node.neighbours:

                    if neighbour.point not in visited and (neighbour.symbol == Color.White.value):
                        next_neighbour_segment.append(neighbour)
                        visited.add(neighbour.point)

            neighbour_segment = next_neighbour_segment
            distance += 1
        segment_index +=1


    return distances






def get_segments(graph: dict[Point, Node], color:str) -> list[list[Node]]:
    segments : list[list[Node]] = []
    visited : set[Node] = set()

    for point in graph:
        node = graph[point]
        if node in visited:
            continue
        if node.symbol == color:
            segment = [node]
            stack = [node]
            while stack:
                current = stack.pop()
                for neighbor in current.neighbours:
                    if neighbor in visited:
                        continue
                    if neighbor.symbol == color:
                        stack.append(neighbor)
                        segment.append(neighbor)
                visited.add(current)
            segments.append(segment)

    return segments

def segment_connected_to_island(segment: list[Node], island: list[Point], color:str) -> bool:

    for node in segment:
        if (node.symbol == color or node.symbol == Color.White.value) and node.point in island:
            return True
    return False








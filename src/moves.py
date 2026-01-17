from data_types import Node, Point

def get_available_moves(graph: dict[Point, Node]) -> list[Point]:
    available_moves : list[Point] = []
    
    for point, node in graph.items():
        if not node.has_value():
            available_moves.append(point)
            
    return available_moves
           

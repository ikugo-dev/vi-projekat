import string
from data_types import Point, Node


def graph(graph: dict[Point, Node], size: int) -> None:
    table_matrix : list[list[str]] = [];
    columns = size * 2 - 1
    table_y_offset = size - 3
    table_matrix_height = size * 4 - 3

    #Popuni praznim
    for row in range(table_matrix_height):
        table_matrix.append([])
        for col in range(columns):
            table_matrix[-1].append('  ')

    #Popuni tackicama
    for col in range(columns):
        letter = string.ascii_uppercase[col]
        rng = range(1, size + col + 1)
        if col >= size: rng = range(col - columns // 2 + 1, columns + 1)

        for number in rng:
            table_y = number * 2 + table_y_offset - col
            node = graph[Point(L = letter, N = number)]
            table_matrix[table_y][col] = node.symbol

    #Printuj tablu
    for row in range(table_matrix_height):
        for col in range(columns):
            print(table_matrix[row][col], end = " ")
        print("")

def debug(graph: dict[Point, Node]) -> None:
    for point, node in graph.items():
        print(f"{point}: {node}")
        for neighbour in node.neighbours:
            print(f"-> {neighbour.point}, ")
        print("\n")

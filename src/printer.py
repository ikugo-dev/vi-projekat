import string
from data_types import Color, Point, Node


def create_table(graph: dict[Point, Node]) -> list[list[str]]:
    table : list[list[str]] = [] 
    table_height = size * 4 - 3

    #Popuni praznim
    for row in range(table_height):
        table.append([])
        for col in range(columns):
            table[-1].append('  ')

    #Popuni tackicama
    for col in range(columns):
        letter = string.ascii_uppercase[col]

        #Raspon brojki u odnosu na deo table
        if col < size: rng = range(1, size + col + 1)
        else: rng = range(col - columns // 2 + 1, columns + 1)

        for number in rng:
            table_y = number * 2 + table_y_offset - col
            node = graph[Point(letter, number)]
            table[table_y][col] = node.symbol
    return table

def create_island_table(table: list[list[str]]) -> list[list[str]]:
    islands : list[Color] = [ ]

    for _ in range(size // 2): islands.append(Color.Red)
    for _ in range(size // 2): islands.append(Color.Green)

    island_columns = size * 2 + 2
    island_table_height = size * 4 - 1
    island_table : list[list[str]] = [] 

    for row in range(island_table_height):
        island_table.append([])
        for col in range(island_columns):
            island_table[-1].append('  ')

    #Inject matrix 
    for row in range(table_height):
        for col in range(columns):
            island_table[row+1][col+1] = table[row][col]

    side_x = size ; side_y = -1

    def inc_side(side: int, side_y: int, side_x: int):
        match side:
            case 0: side_y += 1; side_x += 1
            case 1: side_y += 2;
            case 2: side_y += 1; side_x -= 1
            case 3: side_y -= 1; side_x -= 1
            case 4: side_y -= 2;
            case 5: side_y -= 1; side_x += 1
        return side_y, side_x

    for side in range(6):
        for island in islands:
            side_y, side_x = inc_side(side, side_y, side_x)
            island_table[side_y][side_x] = island.value

        side_y, side_x = inc_side(side, side_y, side_x)
    return island_table

def create_legend_table(island_table: list[list[str]]) -> tuple[list[list[str]], int, int]:
    island_columns = size * 2 + 2
    island_table_height = size * 4 - 1

    legend_columns = island_columns + 2
    legend_table_height = island_table_height + 4
    legend_table : list[list[str]] = []

    for row in range(legend_table_height):
        legend_table.append([])
        for col in range(legend_columns):
            legend_table[-1].append('  ')


    for col in range(columns):
        letter = string.ascii_uppercase[col]
        legend_table[0][col + 2] = f"{letter} "
        legend_table[legend_table_height - 1][col + 2] = f"{letter} "

    #Levi brojevi
    for num in range(1, size + 1):
        legend_table[num * 2 + table_y_offset + 5][0] = f"{num} "

    #Desni brojevi
    for num in range(size, columns + 1):
        legend_table[num * 2 + table_y_offset + 2 - (size * 2 - 1)][legend_columns - 1] = f"{num} "

    #Inject matrix 
    for row in range(island_table_height):
        for col in range(island_columns):
            legend_table[row+2][col+1] = island_table[row][col]
    return legend_table, legend_columns, legend_table_height

def print_graph(graph: dict[Point, Node], graph_size: int) -> None:
    global size
    global table_y_offset
    global columns
    global table_height
    size = graph_size
    table_y_offset = size - 3
    columns = size * 2 - 1
    table_height = size * 4 - 3

    table = create_table(graph)
    island_table = create_island_table(table)
    legend_table, width, height = create_legend_table(island_table)

    #Printuj celu tablu
    for row in range(height):
        for col in range(width):
            print(legend_table[row][col], end = " ")
        print("")

# def debug(graph: dict[Point, Node]) -> None:
#     for point, node in graph.items():
#         print(f"{point}: {node}")
#         for neighbour in node.neighbours:
#             print(f"-> {neighbour}, ")
#         print("\n")

import string
from data_types import Color, Point, Node


def graph(graph: dict[Point, Node], size: int) -> None:

    islands : list[Color] = [ ]

    for _ in range(size // 2): islands.append(Color.Red)
    for _ in range(size // 2): islands.append(Color.Green)

    columns = size * 2 - 1

    ##########Tackice############

    table_matrix : list[list[str]] = [] 
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

        #Raspon brojki u odnosu na deo table
        if col < size: rng = range(1, size + col + 1)
        else: rng = range(col - columns // 2 + 1, columns + 1)

        for number in rng:
            table_y = number * 2 + table_y_offset - col
            node = graph[Point(L = letter, N = number)]
            table_matrix[table_y][col] = node.symbol


    ##########Ostrva############

    isl_columns = size * 2 + 2
    isl_table_matrix_height = size * 4 - 1
    isl_table_matrix : list[list[str]] = [] 

    for row in range(isl_table_matrix_height):
        isl_table_matrix.append([])
        for col in range(isl_columns):
            isl_table_matrix[-1].append('  ')

    #Inject matrix 
    for row in range(table_matrix_height):
        for col in range(columns):
            isl_table_matrix[row+1][col+1] = table_matrix[row][col]

    side_x = size ; side_y = -1

    def inc_side(side: int, side_y: int, side_x: int):
        if   side == 0: side_y += 1; side_x += 1
        elif side == 1: side_y += 2;
        elif side == 2: side_y += 1; side_x -= 1
        elif side == 3: side_y -= 1; side_x -= 1
        elif side == 4: side_y -= 2;
        elif side == 5: side_y -= 1; side_x += 1
        return side_y, side_x

    for side in range(6):
        for island in islands:
            side_y, side_x = inc_side(side, side_y, side_x)
            isl_table_matrix[side_y][side_x] = island.value

        side_y, side_x = inc_side(side, side_y, side_x)


    ###########Legenda###########

    leg_columns = isl_columns + 2
    leg_table_matrix_height = size * 4 + 3
    leg_table_matrix : list[list[str]] = []

    for row in range(leg_table_matrix_height):
        leg_table_matrix.append([])
        for col in range(leg_columns):
            leg_table_matrix[-1].append('  ')

    #Inject matrix 
    for row in range(isl_table_matrix_height):
        for col in range(isl_columns):
            leg_table_matrix[row+2][col+1] = isl_table_matrix[row][col]


    for col in range(columns):
        letter = string.ascii_uppercase[col]
        leg_table_matrix[0][col + 2] = f"{letter} "
        leg_table_matrix[leg_table_matrix_height - 1][col + 2] = f"{letter} "

    #Levi brojevi
    for num in range(1, size + 1):
        leg_table_matrix[num * 2 + table_y_offset + 5][0] = f"{num} "

    #Desni brojevi
    for num in range(size, columns + 1):
        leg_table_matrix[num * 2 + table_y_offset + 2 - (size * 2 - 1)][leg_columns - 1] = f"{num} "

    #Printuj legendu
    for row in range(leg_table_matrix_height):
        for col in range(leg_columns):
            print(leg_table_matrix[row][col], end = " ")
        print("")

def debug(graph: dict[Point, Node]) -> None:
    for point, node in graph.items():
        print(f"{point}: {node}")
        for neighbour in node.neighbours:
            print(f"-> {neighbour.point}, ")
        print("\n")

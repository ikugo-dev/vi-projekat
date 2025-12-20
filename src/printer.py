import string
import itertools as it
from data_types import Point, Node


def graph(graph: dict[Point, Node], size: int) -> None:
    start = [(size*2-1)//2, 1]
    table = []
    row = []

    for i in range((size-1)):
        number = start[1]
        for j in range(start[0] - i, start[0] + i+1, 2):
            letter = string.ascii_uppercase[j]
            row.append(graph[Point(L=letter, N=number )].symbol)
            number+=1
        table.append(row)
        row=[]

    low  = 1
    high = size+low
    for j in range(low, high):
        number = j
        if (high-low) == size: l = 0
        else: l = 1
        for i in range(l, size*2-1, 2):
            letter = string.ascii_uppercase[i]
            row.append(graph[Point(L=letter, N=number)].symbol)
            number+=1
        table.append(row)
        if l == 0: low+=1
        else: high+=1
        row = []

    start = [(size*2-1)//2, 6]

    for i in range(size-2, -1, -1):
        number = start[1]
        for j in range(start[0] - i, start[0] + i+1, 2):
            letter = string.ascii_uppercase[j]
            row.append(graph[Point(L=letter, N=number)].symbol)
            number+=1
        start[1]+=1
        table.append(row)

        row=[]

    for row in table:
        outp = "".join(row)
        print(outp.center(size, ' '))


def debug(graph: dict[Point, Node]) -> None:
    for point, node in graph.items():
        print(f"{point}: {node}")
        for neighbour in node.neighbours:
            print(f"-> {neighbour.point}, ")
        print("\n")

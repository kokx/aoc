import sys
import math
import random
import re
from collections import Counter, deque
import networkx as nx
import itertools

grid = []

for line in sys.stdin:
    grid.append(list(line))

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

G = nx.Graph()

portals = {}
invportals = {}
edges = []

# find all portals
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if 'A' <= grid[y][x] <= 'Z':
            # check if there is a '.' nearby
            nearby = False
            letter = ''
            lloc = (0, 0)
            for dx, dy in dirs:
                cx, cy = (x+dx, y+dy)

                if cy >=0 and cy < len(grid) and cx >= 0 and cx < len(grid[cy]):
                    if grid[cy][cx] == '.':
                        edges.append(((x, y), (cx, cy), 0))
                        nearby = True
                    if 'A' <= grid[cy][cx] <= 'Z':
                        letter = grid[cy][cx]
                        lloc = (cx, cy)
            if nearby:
                if (x, y) < lloc:
                    name = grid[y][x] + letter
                else:
                    name = letter + grid[y][x]
                #name = ''.join(sorted([grid[y][x], letter]))
                #print(name, (x, y))
                if not name in portals:
                    portals[name] = []
                portals[name].append((x, y))
                invportals[(x, y)] = name
        if grid[y][x] == '.':
            # verify above and to the left
            if y > 0 and grid[y-1][x] == '.':
                edges.append(((x, y), (x, y-1), 1))
            if x > 0 and grid[y][x-1] == '.':
                edges.append(((x, y), (x-1, y), 1))

#print(portals)
#print(G.nodes())

def is_outer(loc):
    x, y = loc
    if x <= 4 or x >= len(grid[0]) - 4:
        return True
    if y <= 4 or y >= len(grid) - 4:
        return True
    return False

# add 100 levels
for level in range(100):
    for a, b, w in edges:
        G.add_edge((level, a[0], a[1]), (level, b[0], b[1]), weight=w)


    for name, locs in portals.items():
        if len(locs) > 2:
            print("Shit, probably wrong type of portal!")
            print(name, locs)
            sys.exit(1)
        if len(locs) == 2:
            # determine if loc is in inner or outer ring
            l0 = locs[0]
            l1 = locs[1]
            if is_outer(locs[0]) == is_outer(locs[1]):
                print("Should not happen!")
                sys.exit(1)
            if is_outer(locs[0]):
                G.add_edge((level, l0[0], l0[1]), (level-1, l1[0], l1[1]), weight=1)
            else:
                G.add_edge((level, l1[0], l1[1]), (level-1, l0[0], l0[1]), weight=1)
        # for len == 1, we don't need to do anything, its the start


start = portals['AA'][0]
start = (0, start[0], start[1])
target = portals['ZZ'][0]
target = (0, target[0], target[1])

#path = nx.dijkstra_path(G, start, target)

#for l, x, y in path:
#    if (x, y) in invportals:
#        print((l, x, y), '--', invportals[(x, y)])
#    else:
#        print((l, x, y))


print(nx.dijkstra_path_length(G, start, target))

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
                        G.add_edge((x, y), (cx, cy), weight=0)
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
        if grid[y][x] == '.':
            # verify above and to the left
            if y > 0 and grid[y-1][x] == '.':
                G.add_edge((x, y), (x, y-1), weight=1)
            if x > 0 and grid[y][x-1] == '.':
                G.add_edge((x, y), (x-1, y), weight=1)

#print(portals)
#print(G.nodes())

for name, locs in portals.items():
    if len(locs) > 2:
        print("Shit, probably wrong type of portal!")
        print(name, locs)
    if len(locs) == 2:
        G.add_edge(locs[0], locs[1], weight=1)
    # for len == 1, we don't need to do anything, its the start


start = portals['AA'][0]
target = portals['ZZ'][0]

print(nx.dijkstra_path_length(G, start, target))

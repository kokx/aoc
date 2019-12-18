import sys
import math
import random
import re
from collections import Counter, deque
import networkx as nx
import itertools

grid = []

for line in sys.stdin:
    grid.append(list(line.strip()))

gridrows = len(grid)
gridcols = len(grid[0])

dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]

queue = deque()

possible_keys = set()

for y in range(gridrows):
    for x in range(gridcols):
        if grid[y][x] == '@':
            # set as BFS start
            queue.append((x, y, set(), 0))
        if 'a' <= grid[y][x] <= 'z':
            possible_keys.add(grid[y][x])

seen = set()

while len(queue) > 0:
    x, y, keys, dist = queue.popleft()
    key = (x, y, tuple(sorted(keys)))

    if key in seen:
        # we have seen this before
        continue

    seen.add(key)

    # do keep some progress if slow
    if len(seen) % 1000000 == 0:
        print(len(seen))

    # out of bounds or wall
    if not (0 <= y < gridrows and 0 <= x <= gridcols and grid[y][x] != '#'):
        continue

    # if door, check if we have key
    if 'A' <= grid[y][x] <= 'Z' and grid[y][x].lower() not in keys:
        continue

    newkeys = set(keys)

    if 'a' <= grid[y][x] <= 'z':
        newkeys.add(grid[y][x])
        if newkeys == possible_keys:
            print('Part one:', dist)
            sys.exit(0)
    for dirx, diry in dirs:
        nx = x + dirx
        ny = y + diry

        queue.append((nx, ny, newkeys, dist + 1))

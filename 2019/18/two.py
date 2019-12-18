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

starts = []
door_locs = {}
key_locs = {}

for y in range(gridrows):
    for x in range(gridcols):
        if grid[y][x] == '@':
            # set as BFS start
            starts.append((x, y))
        if 'a' <= grid[y][x] <= 'z':
            key_locs[grid[y][x]] = (x, y)
        if 'A' <= grid[y][x] <= 'A':
            door_locs[grid[y][x]] = (x, y)

queue.append((starts, set(), 0))
seen = {}
most = 9999999999999
bot_num = len(starts) # should be 4

while len(queue) > 0:
    bots, keys, dist = queue.popleft()
    key = (x, y, tuple(sorted(keys)))

    if key in seen and dist >= seen[key]:
        # we have seen this before
        continue

    seen[key] = dist

    # do keep some progress if slow
    if len(seen) % 100000 == 0:
        print(len(seen))


    # verify if we are in a valid state (no bot in a wall or unopened door)
    valid = True
    for x, y in bots:
        # out of bounds or wall
        if not (0 <= y < gridrows and 0 <= x <= gridcols and grid[y][x] != '#'):
            valid = False
            break
        # if door, check if we have key
        if 'A' <= grid[y][x] <= 'Z' and grid[y][x].lower() not in keys:
            valid = False
            break
    if not valid:
        continue

    botqueue = deque()
    botdists = {}

    for i in range(bot_num):
        botqueue.append((i, bots[i], 0))

    while len(botqueue) > 0:
        botid, bot, botdist = botqueue.popleft()
        x, y = bot

        # out of bounds or wall
        if not (0 <= y < gridrows and 0 <= x <= gridcols and grid[y][x] != '#'):
            continue
        # if door, check if we have key
        if 'A' <= grid[y][x] <= 'Z' and grid[y][x].lower() not in keys:
            continue

        if bot in botdists:
            continue

        botdists[bot] = (botdist, botid)

        for dirx, diry in dirs:
            newbot = (x + dirx, y + diry)
            botqueue.append((botid, newbot, botdist + 1))

    for key in key_locs:
        if key not in keys and key_locs[key] in botdists:
            botdist, botid = botdists[key_locs[key]]
            newbots = list(bots)
            newbots[botid] = key_locs[key]
            newkeys = set(keys)
            newkeys.add(key)
            newdist = dist + botdist

            if len(newkeys) == len(key_locs):
                if newdist < most:
                    most = newdist
            queue.append((newbots, newkeys, newdist))

print(most)

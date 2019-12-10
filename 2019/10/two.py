import sys
import math
import random
from collections import Counter

asteroids = []

ilines = []

y = 0

for line in sys.stdin:
    # todo do processing, uncomment split for splitting on comma and fix
    ilines.append(line.strip())
    x = 0
    for c in line:
        if c == '#':
            asteroids.append((x, y))
        x += 1
    y += 1

# for interpreting everything as integer
#ilines = list(map(int, ilines))

most = 0
best = (0, 0)

# do a search for every asteroid
for asteroid in asteroids:
    reachable = set()
    for test in asteroids:
        if test == asteroid:
            continue
        res = math.atan2(test[0] - asteroid[0], test[1] - asteroid[1])
        res = int(res * 1000000)
        reachable.add(res)
    if most < len(reachable):
        most = len(reachable)
        best = asteroid
print(most)

startangle = int(math.atan2(0, -1) * 1000000)
print(startangle)

# do a new reachability search, obtain lists this time
reachable = {}
for test in asteroids:
    if test == asteroid:
        continue
    res = math.atan2(test[0] - best[0], test[1] - best[1])
    res = int(res * 1000000)
    if not res in reachable:
        reachable[res] = []
    reachable[res].append(test)

#print(reachable)

curangle = startangle
keys = reversed(sorted(reachable.keys()))

print(reachable[curangle])
print(best)

for i in range(200):
    #print(curangle, keys)
    if i == 199:
        # 200-th angle
        print(i+1, reachable[curangle])
        # TODO: find closest
    print(i+1, reachable[curangle])

    # find next curangle
    nx = curangle
    for k in keys:
        if k >= nx:
            continue
        else:
            nx = k
            break
    if nx == curangle:
        nx = keys[0]
        print(keys[0])
    curangle = nx

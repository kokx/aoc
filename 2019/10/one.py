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
#print(best)

startangle = int(math.atan2(0, -1) * 1000000)
#print(startangle)

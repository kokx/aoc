import sys
import re

p = re.compile('pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=(-?[0-9]+)$')

nanobots = []

for line in sys.stdin:
    line = line.strip()
    m = p.match(line)

    coord = [m.group(1), m.group(2), m.group(3)]
    coord = map(int, coord)

    nanobots.append((tuple(coord), int(m.group(4))))

best = 0
mx = 0

for i in range(0, len(nanobots)):
    bot = nanobots[i]
    if bot[1] > mx:
        best = i
        mx = bot[1]

def manhattan(coorda, coordb):
    ax, ay, az = coorda
    bx, by, bz = coordb

    return abs(ax - bx) + abs(ay - by) + abs(az - bz)

def bot_distance(bota, botb):
    ac, ar = bota
    bc, br = botb
    return manhattan(ac, bc)


total = 0

for bot in nanobots:
    dist = bot_distance(nanobots[best], bot)

    if dist <= nanobots[best][1]:
        total += 1

print(total)

from z3 import *

def zabs(x):
    return If(x >= 0,x,-x)

(x, y, z) = (Int('x'), Int('y'), Int('z'))
inrange = []
for i in range(0, len(nanobots)):
    inrange.append(Int('inrange_' + str(i)))

o = Optimize()

rcount = Int('rangesum')

for i in range(0, len(nanobots)):
    (bx, by, bz), br = nanobots[i]
    o.add(inrange[i] == If(zabs(x - bx) + zabs(y - by) + zabs(z - bz) <= br, 1, 0))

o.add(rcount == sum(inrange))

# also add constraint for distance from 0
zerodist = Int('zerodist')

o.add(zerodist == zabs(x) + zabs(y) + zabs(z))

res1 = o.maximize(rcount)
res2 = o.minimize(zerodist)

print(o.check())

print(res2)
print(o.lower(res2), o.upper(res2))

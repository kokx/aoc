# 370707 too low

import sys
from math import floor

points = set()

for line in sys.stdin:
    line = line.strip()

    if line == '':
        break

    [x, y] = line.split(',')

    points.add((int(x), int(y)))

first = True

for line in sys.stdin:
    line = line.strip()
    (_, _, ins) = line.split(' ')
    (along, num) = ins.split('=')
    num = int(num)

    newpoints = set()

    for (x, y) in points:
        if along == 'y' and y > num:
            newpoints.add((x, num - (y - num)))
        elif along == 'x' and x > num:
            newpoints.add((num - (x - num), y))
        else:
            newpoints.add((x, y))

    points = newpoints

    if first:
        first = False
        print(len(points))

# display points as grid
mxx = 0
mxy = 0
mix = 9999999999999
miy = 9999999999999
for x, y in points:
    if mxx < x:
        mxx = x
    if mxy < y:
        mxy = y
    if mix > x:
        mix = x
    if miy > y:
        miy = y


mxx += 1
mxy += 1

for y in range(miy, mxy):
    line = ''
    for x in range(mix, mxx):
        if (x, y) in points:
            line += '#'
        else:
            line += ' '
    print(line)


print(mix, mxx)
print(miy, mxy)

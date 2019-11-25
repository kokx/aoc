import sys
import re

p = re.compile('position=\< ?(-?[0-9]+),  ?(-?[0-9]+)\> velocity=\< ?(-?[0-9]+),  ?(-?[0-9]+)\>')

pixels = []

for line in sys.stdin:
    m = p.match(line)
    px = int(m.group(1))
    py = int(m.group(2))
    vx = int(m.group(3))
    vy = int(m.group(4))

    pixels.append((px, py, vx, vy))

def display(pixels, sec):
    grid = []

    rows = 15
    cols = 70

    for i in range(0, rows):
        grid.append([])
        for j in range(0, cols):
            grid[i].append(0)

    minx = 99999999999
    maxx = -99999999999
    miny = 99999999999
    maxy = -99999999999
    for px, py, vx, vy in pixels:
        x = px + sec * vx
        y = py + sec * vy

        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x, maxx)
        maxy = max(y, maxx)

    if maxx - minx > cols or maxy - miny > rows:
        #print('too big')
        return False

    print(sec)

    print(minx)
    print(miny)

    for px, py, vx, vy in pixels:
        x = px + sec * vx + minx * -1
        y = py + sec * vy + miny * -1
        grid[y][x] += 1

    for row in grid:
        pr = ''
        for col in row:
            if col >= 1:
                pr += '#'
            else:
                pr += '.'
        print(pr)
    print(sec)
    print()
    return True

for i in range(10800, 100000):
    if display(pixels, i):
        break

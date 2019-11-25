import sys
import re

# guess 50213
# guess 50209 too low
# guess 54686 too high
# 528000 - correct
# part2:
# 45210 - correct

p = re.compile('^(y|x)=([0-9]+), (x|y)=([0-9]+)..([0-9]+)$')

source = (500, 0)

datalist = []

maxx = 0
maxy = 0
minx = 9999999999
miny = 9999999999

for line in sys.stdin:
    m = p.match(line)

    if m.group(1) == 'x':
        x = int(m.group(2))
        y = (int(m.group(4)), int(m.group(5))+1)
        maxx = max(x, maxx)
        maxy = max(max(y), maxy)
        minx = min(x, minx)
        miny = min(min(y), miny)
    else:
        y = int(m.group(2))
        x = (int(m.group(4)), int(m.group(5))+1)
        maxx = max(max(x), maxx)
        maxy = max(y, maxy)
        minx = min(min(x), minx)
        miny = min(y, miny)

    datalist.append((x, y))

grid = []

minx -= 2
origminy = miny
miny = 0
maxx += 2
origmaxy = maxy
maxy += 2

for i in range(0, maxy - miny + 2):
    grid.append([])
    for j in range(0, maxx - minx + 2):
        grid[i].append('.')

for x, y in datalist:
    if type(x) == tuple:
        for nx in range(x[0], x[1]):
            grid[y-miny][nx-minx] = '#'
    else:
        for ny in range(y[0], y[1]):
            grid[ny-miny][x-minx] = '#'

grid[source[1]][source[0]-minx] = '+'

def printgrid():
    for line in grid:
        ln = ''
        for c in line:
            ln += c
        print(ln)
    print()

def fgrid(tup):
    x, y = tup
    return grid[y-miny][x-minx]

def sgrid(tup, val):
    x, y = tup
    grid[y-miny][x-minx] = val

for y in range(miny, maxy+2):
    sgrid((maxx+1, y), '#')
    sgrid((minx, y), '#')

activeflow = [source]

while len(activeflow) > 0:
    activeflow.sort()
    next = activeflow.pop(0)

    if next[1] > maxy:
        continue

    # check one below
    if fgrid((next[0], next[1]+1)) == '.':
        sgrid((next[0], next[1]+1), '|')
        activeflow.append((next[0], next[1]+1))
    elif fgrid((next[0], next[1]+1)) == '#' or fgrid((next[0], next[1]+1)) == '~':
        # passiveflow instead, fill current level
        # first to the left
        passiveleft = []
        passiveright = []
        nextleft = next
        while fgrid(nextleft) == '.' or fgrid(nextleft) == '|':
            passiveleft.append(nextleft)
            nextleft = (nextleft[0]-1, nextleft[1])
        # then to the right
        nextleft = (next[0]+1, next[1])
        while fgrid(nextleft) == '.' or fgrid(nextleft) == '|':
            passiveright.append(nextleft)
            nextleft = (nextleft[0]+1, nextleft[1])

        # now verify if we can move lower on any
        activeleft = None
        for tile in passiveleft:
            if fgrid((tile[0], tile[1]+1)) == '.' or fgrid((tile[0], tile[1]+1)) == '|':
                activeleft = tile
                break
        activeright = None
        for tile in passiveright:
            if fgrid((tile[0], tile[1]+1)) == '.' or fgrid((tile[0], tile[1]+1)) == '|':
                activeright = tile
                break

        if activeleft is None and activeright is None:
            for tile in passiveleft:
                sgrid(tile, '~')
            for tile in passiveright:
                sgrid(tile, '~')
                # move active flow one up
            if next[1] > 0:
                activeflow.append((next[0], next[1]-1))
        else:
            for tile in passiveleft:
                sgrid(tile, '|')
                if tile == activeleft:
                    activeflow.append(activeleft)
                    break
            for tile in passiveright:
                sgrid(tile, '|')
                if tile == activeright:
                    activeflow.append(activeright)
                    break
    #printgrid()
printgrid()

# count all
count = 0
count2 = 0
for x in range(minx, maxx):
    for y in range(origminy, origmaxy):
        if fgrid((x, y)) == '~' or fgrid((x, y)) == '|':
            count += 1
        if fgrid((x, y)) == '~':
            count2 += 1

print(count)
print(count2)

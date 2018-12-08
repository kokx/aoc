import sys
import collections

maxx = 0
maxy = 0

coords = []

for line in sys.stdin:
    data = line.split(',')
    x = int(data[0].strip())
    y = int(data[1].strip())
    coords.append((x, y))

    maxx = max(x, maxx)
    maxy = max(y, maxy)

maxx +=1
maxy +=1

grid = []

for x in range(0, maxx):
    grid.append([])
    for y in range(0, maxy):
        grid[x].append({})

def neighbours(coord):
    x, y = coord
    ret = []
    if x - 1 >= 0:
        ret.append((x-1, y))
    if y - 1 >= 0:
        ret.append((x, y-1))
    if x + 1 < maxx:
        ret.append((x+1, y))
    if y + 1 < maxy:
        ret.append((x, y+1))
    return ret

# floodfill for each

for i in range(0, len(coords)):
    x, y = coords[i]
    # TODO floodfill from x, y
    queue = collections.deque()
    queue.appendleft(coords[i])
    done = set()
    done.add(coords[i])
    grid[x][y][i] = 0
    while len(queue) > 0:
        coord = queue.pop()
        cx, cy = coord
        for nb in neighbours(coord):
            if not nb in done:
                nx, ny = nb
                queue.appendleft(nb)
                done.add(nb)
                grid[nx][ny][i] = grid[cx][cy][i] + 1


total = 0
wanted = 10000

for x in range(0, maxx):
    for y in range(0, maxy):
        sum = 0
        for k, v in grid[x][y].items():
            sum += v

        if sum < wanted:
            total += 1

print(total)

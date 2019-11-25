# guess

depth = 7863
target = (14, 760)

# for sample:
#depth = 510
#target = (10, 10)

maxx = target[0] + 10
maxy = target[1] + 10

grid = []
rgrid = []

for y in range(0, maxy):
    grid.append([])
    rgrid.append([])
    for x in range(0, maxx):
        if x == 0 and y == 0:
            geo = 0
        elif x == target[0] and y == target[1]:
            geo = 0
        elif y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = grid[y][x-1] * grid[y-1][x]

        grid[y].append((geo + depth) % 20183)
        rgrid[y].append(grid[y][x] % 3)

def printgrid(grid):
    for line in grid:
        ln = ''
        for ch in line:
            if ch == 0:
                ln += '.'
            elif ch == 1:
                ln += '='
            elif ch == 2:
                ln += '|'
        print(ln)

def riskLevel(grid, target):
    maxx, maxy = target
    level = 0
    for y in range(0, maxy + 1):
        for x in range(0, maxx + 1):
            level += grid[y][x]
    return level

print('y')

printgrid(rgrid)

print(riskLevel(rgrid, target))

import sys

#guess 221900
#guess 223728 too high
#guess 217064 too high
#guess 215404

grid = []

for line in sys.stdin:
    grid.append(list(line.strip()))


lgrid = []
for i in range(0, 200):
    if i == 100:
        lgrid.append(grid)
    else:
        lgrid.append([['.' for col in range(len(grid[row]))] for row in range(len(grid))])

#print(lgrid)

def valid(grid, loc):
    row, col = loc
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[row])

def countneighbors(lgrid, level, loc, tp):
    grid = lgrid[level]
    row, col = loc
    count = 0
    neighbors = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    for rowd, cold in neighbors:
        rd, cd = (row + rowd, col + cold)

        if rd == 2 and cd == 2 and level < len(lgrid) - 1:
            # TODO: special case, count neighbors of 'inner' +1
            ngrid = lgrid[level+1]
            if row == 1 and col == 2:
                for i in range(len(ngrid[0])):
                    if ngrid[0][i] == tp:
                        count += 1
            elif row == 2 and col == 1:
                for i in range(len(ngrid)):
                    if ngrid[i][0] == tp:
                        count += 1
            elif row == 3 and col == 2:
                for i in range(len(ngrid[len(ngrid)-1])):
                    if ngrid[len(ngrid)-1][i] == tp:
                        count += 1
            elif row == 2 and col == 3:
                for i in range(len(ngrid)-1):
                    if ngrid[i][len(ngrid[i])-1] == tp:
                        count += 1
            continue


        if valid(grid, (rd, cd)):
            #count += 10
            if grid[rd][cd] == tp:
                count += 1
        elif level > 0:
            # TODO: count neighbors of 'outer' -1
            nc = 0
            nrd, ncd = (2 + rowd, 2 + cold)
            if lgrid[level-1][nrd][ncd] == tp:
                count += 1
                nc += 1
    return count

def printgrid(grid):
    for line in grid:
        ln = ''
        for c in line:
            ln += str(c)
        print(ln)
    print()

def sim(lgrid):
    newlgrid = [[list(line) for line in grid] for grid in lgrid]

    for level in range(0, len(lgrid)):
        for row in range(0, len(lgrid[level])):
            for col in range(0, len(lgrid[level][row])):
                if row == 2 and col == 2:
                    # there is no field here, actually
                    newlgrid[level][row][col] = '?'
                    continue
                if lgrid[level][row][col] == '.':
                    if 1 <= countneighbors(lgrid, level, (row, col), '#') <= 2:
                        newlgrid[level][row][col] = '#'
                elif lgrid[level][row][col] == '#':
                    if countneighbors(lgrid, level, (row, col), '#') == 1:
                        newlgrid[level][row][col] = '#'
                    else:
                        newlgrid[level][row][col] = '.'
    #printgrid(shadow)
    return newlgrid

for j in range(200):
    for i in range(95, 105):
        print(i - 100)
        printgrid(lgrid[i])
    lgrid = sim(lgrid)
    print('--', j, '--------------')

for i in range(95, 105):
    print(i - 100)
    printgrid(lgrid[i])

bugs = 0

for grid in lgrid:
    for row in grid:
        for c in row:
            if c == '#':
                bugs += 1
print(bugs)

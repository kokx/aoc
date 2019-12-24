import sys

#guess 221900
#guess 223728 too high
#guess 217064 too high
#guess 215404

grid = []

for line in sys.stdin:
    grid.append(list(line.strip()))

def valid(grid, loc):
    row, col = loc
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[row])

def countneighbors(grid, loc, tp):
    row, col = loc
    count = 0
    neighbors = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    for rowd, cold in neighbors:
        if valid(grid, (row + rowd, col + cold)):
            #count += 10
            if grid[row+rowd][col+cold] == tp:
                count += 1
    return count

def printgrid(grid):
    for line in grid:
        ln = ''
        for c in line:
            ln += str(c)
        print(ln)
    print()

def sim(grid):
    newgrid = []
    #shadow = []
    for line in grid:
        newgrid.append(list(line))
        #shadow.append(list(line))

    for row in range(0, len(grid)):
        for col in range(0, len(grid)):
            if grid[row][col] == '.':
                #shadow[row][col] = countneighbors(grid, (row, col), '#')
                if 1 <= countneighbors(grid, (row, col), '#') <= 2:
                    newgrid[row][col] = '#'
            elif grid[row][col] == '#':
                #shadow[row][col] = countneighbors(grid, (row, col), '|')
                if countneighbors(grid, (row, col), '#') == 1:
                    newgrid[row][col] = '#'
                else:
                    newgrid[row][col] = '.'
    #printgrid(shadow)
    return newgrid

#printgrid(grid)

def biodiv(grid):
    biodiv = 0
    mul = 1
    for row in grid:
        for col in row:
            if col == '#':
                biodiv += mul
            mul *= 2
    return biodiv


def tuplegrid(grid):
    newgrid = []
    for row in grid:
        newgrid.append(tuple(row))
    return tuple(newgrid)

oldgrids = set()

oldgrids.add(tuplegrid(grid))

for i in range(1000):
    #print(i+1)
    grid = sim(grid)
    #printgrid(grid)
    tgrid = tuplegrid(grid)
    if tgrid in oldgrids:
        print("Found it")
        printgrid(grid)
        print(biodiv(grid))
        break
    oldgrids.add(tgrid)

import sys

#guess 221900
#guess 223728 too high
#guess 217064 too high

grid = []

for line in sys.stdin:
    line = line.strip()
    last = []
    for c in line:
        last.append(c)
    grid.append(last)

def valid(grid, loc):
    row, col = loc
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[row])

def countneighbors(grid, loc, tp):
    row, col = loc
    count = 0
    neighbors = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
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
                #shadow[row][col] = countneighbors(grid, (row, col), '|')
                if countneighbors(grid, (row, col), '|') >= 3:
                    newgrid[row][col] = '|'
            elif grid[row][col] == '|':
                #shadow[row][col] = countneighbors(grid, (row, col), '#')
                if countneighbors(grid, (row, col), '#') >= 3:
                    newgrid[row][col] = '#'
            elif grid[row][col] == '#':
                #shadow[row][col] = countneighbors(grid, (row, col), '|')
                if countneighbors(grid, (row, col), '#') >= 1 and countneighbors(grid, (row, col), '|') >= 1:
                    newgrid[row][col] = '#'
                else:
                    newgrid[row][col] = '.'
    #printgrid(shadow)
    return newgrid

printgrid(grid)

def gcount(grid):
    lumber = 0
    trees = 0
    for line in grid:
        for c in line:
            if c == '#':
                lumber += 1
            elif c == '|':
                trees += 1

    #print('%d * %d = %d' % (trees, lumber, (trees * lumber)))
    return trees * lumber

gcounts = []
for i in range(0, 1000):
    grid = sim(grid)

    last = gcount(grid)
    gcounts.append(last)
    if len(gcounts) > 50:
        gcounts.pop(0)
    #if i > 600:
    #    # try to find period
    #    for j in range(0, len(gcounts) - 1):
    #        if last == gcounts[j]:
    #            print(len(gcounts) - j - 1)
    #print(gcounts)
    #printgrid(grid)

# period = 28
print(gcounts)

print(gcounts[0], gcounts[28])

# gcounts[0] = it 1000
print(gcounts[((1000000000 - 1001) % 28) + (50-28)])

for i in range(0, 30):
    if gcounts[i] < 217064:
        print('--', gcounts[i])

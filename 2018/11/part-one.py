serial = 2694

# TODO remove
#serial = 42

grid = []
for i in range(0, 300):
    grid.append([])
    for j in range(0, 300):
        grid[i].append(None)

def get_digit(number, n):
    return number // 10**n % 10

def calcCell(x, y):
    if grid[x][y] is None:
        rackId = x + 10
        powerLevel = rackId * y
        powerLevel += serial
        powerLevel *= rackId
        powerLevel = get_digit(powerLevel, 2)
        grid[x][y] = powerLevel - 5
    return grid[x][y]

def getSquare(x, y, size):
    power = 0
    for xi in range(0, size):
        for yi in range(0, size):
            power += calcCell(x + xi, y + yi)
    return power

memo = []

for i in range(0, 300):
    memo.append([])
    for j in range(0, 300):
        memo[i].append([])
        for k in range(0, 300):
            memo[i][j].append(None)

memo[1] = grid

def memoSquare(x, y, size):
    if memo[size][x][y] is None:
        if not memo[size-1][x][y] is None:
            # calculate with smaller size
            level = memo[size-1][x][y]
            for i in range(0, size):
                level += calcCell(x+size-1, y+i)
            for i in range(0, size-1):
                level += calcCell(xi, y+size-1)
            memo[size][x][y] = level
        else:
            memo[size][x][y] = getSquare(x, y, size)
    return memo[size][x][y]

largest = (-1, -1, -1)
maxNum = -1000

# find largest square
for i in range(1, 32):
    for x in range(0, 300 - i + 1):
        for y in range(0, 300 - i + 1):
            if getSquare(x, y, i) > maxNum:
                maxNum = getSquare(x, y, i)
                largest = (x, y, i)

print(largest, maxNum)

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

sumAreaTable = []

for x in range(0, 300):
    sumAreaTable.append([])
    for y in range(0, 300):
        sumAreaTable[x].append(-1)

for x in range(0, 300):
    for y in range(0, 300):
        sum = calcCell(x, y)
        if x > 0:
            sum += sumAreaTable[x-1][y]
        if y > 0:
            sum += sumAreaTable[x][y-1]
        if x > 0 and y > 0:
            sum -= sumAreaTable[x-1][y-1]
        sumAreaTable[x][y] = sum

def getSquare(x, y, size):
    x, y, xend, yend = (x, y, x+size-1, y+size-1)
    return sumAreaTable[xend][yend] + sumAreaTable[x][y] - sumAreaTable[x][yend] - sumAreaTable[xend][y]

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

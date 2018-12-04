import sys
import re

grid = []

for i in range(0, 1010):
    grid.append([])
    for j in range(0, 1010):
        grid[i].append(0)

p = re.compile('\#([0-9]+) @ ([0-9]+)\,([0-9]+): ([0-9]+)x([0-9]+)')

queries = []

for line in sys.stdin:
    m = p.match(line)
    #print(m.group(0), line, m.group(1), m.group(2), m.group(3), m.group(4))
    num = int(m.group(1))
    top = int(m.group(2))
    left = int(m.group(3))
    topnum = int(m.group(4))
    leftnum = int(m.group(5))

    queries.append((num, top, left, topnum, leftnum))

    for i in range(0, topnum):
        for j in range(0, leftnum):
            grid[top + i][left + j] += 1

total = 0
for i in range(0, 1010):
    for j in range(0, 1010):
        if grid[i][j] >= 2:
            total += 1

print(total)

for q in queries:
    num, top, left, topnum, leftnum = q

    works = True

    for i in range(0, topnum):
        for j in range(0, leftnum):
            if grid[top + i][left + j] != 1:
                works = False
    if works:
        print(num)

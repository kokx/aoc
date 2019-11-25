import sys
import re

grid = []

for i in range(0, 1010):
    grid.append([])
    for j in range(0, 1010):
        grid[i].append(0)

p = re.compile('\#[0-9]+ @ ([0-9]+)\,([0-9]+): ([0-9]+)x([0-9]+)')

for line in sys.stdin:
    m = p.match(line)
    #print(m.group(0), line, m.group(1), m.group(2), m.group(3), m.group(4))
    top = int(m.group(1))
    left = int(m.group(2))
    topnum = int(m.group(3))
    leftnum = int(m.group(4))

    for i in range(0, topnum):
        for j in range(0, leftnum):
            grid[top + i][left + j] += 1

total = 0
for i in range(0, 1010):
    for j in range(0, 1010):
        if grid[i][j] >= 2:
            total += 1

print(total)

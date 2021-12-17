import sys

hor = 0
depth = 0
depth2 = 0
aim = 0

for line in sys.stdin:
    line = line.strip().split(' ')
    if line[0] == 'forward':
        hor += int(line[1])
        depth2 += aim * int(line[1])
    if line[0] == 'down':
        depth += int(line[1])
        aim += int(line[1])
    if line[0] == 'up':
        depth -= int(line[1])
        aim -= int(line[1])

print(hor*depth)
print(hor*depth2)

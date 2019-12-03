import sys
import math

wires = []

for line in sys.stdin:
    wires.append(line.strip().split(','))

dx = {'L': -1, 'R': 1, 'U': 0, 'D': 0}
dy = {'L': 0, 'R': 0, 'U': -1, 'D': 1}

def find_points(wire):
    x = 0
    y = 0
    points = {}
    ln = 0
    for cmd in wire:
        dir = cmd[0]
        num = int(cmd[1:])

        for i in range(num):
            x += dx[dir]
            y += dy[dir]
            ln += 1
            if (x, y) not in points:
                points[(x, y)] = ln
    return points

pointsa = find_points(wires[0])
pointsb = find_points(wires[1])

combined = set(pointsa.keys()) & set(pointsb.keys())
combinedone = [abs(x) + abs(y) for (x, y) in combined]

print(min(combinedone))

# for all intersections, minimum length of the wire between the intersections
print(min([pointsa[p]+pointsb[p] for p in combined]))

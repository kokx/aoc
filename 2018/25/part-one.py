import sys
import re

p = re.compile('(-?[0-9]+),(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)')

constellations = []
ignore = set()

def manhattan(a, b):
    dist = 0
    for i in range(0, len(a)):
        dist += abs(a[i] - b[i])
    return dist

for line in sys.stdin:
    m = p.match(line.strip())
    point = [m.group(1), m.group(2), m.group(3), m.group(4)]
    point = tuple(map(int, point))

    belongs = []

    for i in range(0, len(constellations)):
        cons = constellations[i]
        # see if there is a point within 3 of any constellation point
        for po in cons:
            if manhattan(point, po) <= 3:
                belongs.append(i)
                break

    if len(belongs) >= 2:
        new = []
        for b in belongs:
            new.extend(constellations[b])
            ignore.add(b)
        new.append(point)
        constellations.append(new)
    elif len(belongs) == 1:
        constellations[belongs[0]].append(point)
    else:
        constellations.append([point])

#print(constellations)
print(len(constellations) - len(ignore))

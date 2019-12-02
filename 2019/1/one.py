import sys
import math

total = 0

total2 = 0

for line in sys.stdin:
    mass = int(line)
    fuel = math.floor(mass / 3) - 2
    print(fuel)
    total += fuel

    localtotal = 0

    # keep going until we also have enough fuel for fuel
    while fuel > 0:
        localtotal += fuel
        fuel = math.floor(fuel / 3) - 2
    print('lt', localtotal)
    total2 += localtotal


print(total)
print('p2', total2)

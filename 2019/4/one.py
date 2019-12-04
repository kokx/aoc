import sys
import math
import random
from collections import Counter

#ilines = []
#
#for line in sys.stdin:
#    # todo do processing, uncomment split for splitting on comma and fix
#    ilines.append(line.strip()) #.split(',')

# for interpreting everything as integer
#ilines = list(map(int, ilines))

start = 356261
end = 846303

total = 0
total2 = 0

for i in range(start, end):
    st = str(i)

    checks = True
    repeated = False

    # check
    last = 0
    for c in st:
        if int(c) < last:
            checks = False
        if int(c) == last:
            repeated = True
        last = int(c)

    if checks and repeated:
        # one digit must occur exactly twice
        twice = False
        for k, v in Counter(list(st)).items():
            if v == 2:
                twice = True
        if twice:
            total2 += 1

        total += 1


print(total)
print(total2)

import sys
import math
import random
import re
from collections import Counter, deque
import networkx as nx
import itertools

# set to 10007
#size = 10
# fortunately, both are prime (otherwise this would be nearly impossible)
size = 119315717514047
#size = 10007

query = 2020

# we're going to keep an offset (how much we have shifted or 'cut')
# and an inc, how much (mod size) have we moved stuff around
off = 0
inc = 1

for line in sys.stdin:
    line = line.strip()
    if line == 'deal into new stack':
        inc *= -1
        off += inc
    if line[0:3] == 'cut':
        num = int(line[4:])
        off += inc * num
    if line[0:19] == 'deal with increment':
        num = int(line[20:])

        # use fast exponentiation (square and multiply likely)
        inc *= pow(num, size-2, size)


# and now, way too many times
times = 101741582076661

total_inc = pow(inc, times, size)
# wait what, the offset total would be a geometric series! <3
# Thanks wikipedia! https://en.wikipedia.org/wiki/Geometric_series
total_off = off * (1 - total_inc) * pow(1 - inc, size -2, size)


print((total_off + total_inc * query) % size)

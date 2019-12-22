import sys
import math
import random
import re
from collections import Counter, deque
import networkx as nx
import itertools

# set to 10007
#size = 10
size = 10007

output = []

for i in range(size):
    output.append(i)

for line in sys.stdin:
    line = line.strip()
    if line == 'deal into new stack':
        output = list(reversed(output))
    if line[0:3] == 'cut':
        num = int(line[4:])
        output = output[num:] + output[:num]
    if line[0:19] == 'deal with increment':
        num = int(line[20:])

        oldout = deque(output)

        pos = 0
        while len(oldout) > 0:
            output[pos] = oldout.popleft()
            pos = (pos + num) % size

#print(list(output))
#3284 high
#937 low
for i in range(len(output)):
    if output[i] == 2019:
        print(i)

print('2020', output[2020])

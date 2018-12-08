import sys
import re
from functools import reduce



graph = {}

allchars = set()

p = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

for line in sys.stdin:
    m = p.match(line)
    to = m.group(1)
    fro = m.group(2)

    allchars.add(to)
    allchars.add(fro)

    if not fro in graph:
        graph[fro] = set()
   # if not to in graph:
   #     graph[to] = set()

    graph[fro].add(to)

satisfied = set()

ready = ''

#print(graph, allchars)

while len(satisfied) < 26:
    for chr in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if chr in satisfied:
            continue
        if not chr in graph:
            satisfied.add(chr)
            if chr in allchars:
                #print(chr)
                ready += chr
            break
        # check if deps are satisfied
        sat = True
        for dep in graph[chr]:
            if not dep in satisfied:
                sat = False
                break
        if not sat:
            continue
        # all satisfied
        ready += chr
        #print(chr)
        satisfied.add(chr)
        break

print(ready)

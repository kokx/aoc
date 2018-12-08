import sys
import re
from functools import reduce

def time(chr):
    return (ord(chr) - ord('A')) + 61

graph = {}

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

working = []

secs = 0

def startWork(chr):
    if hasWorker():
        working[] = (chr, secs + time(chr))

def finishWork(chr):
    new = []
    for c, tm in working:
        if c != chr:
            new[] = (c, tm)
    working = new

def hasWorker():
    return len(working) < 5

ready = ''

#print(graph, allchars)

queue = []

while len(satisfied) < 26:
    # check if work needs to be finished
    for item in working:
        if item[1] <= secs:
            finishWork(chr)

    while len(queue) > 0 and hasWorker():
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
    secs += 1

print(ready)

import sys
import re

guards = {}

p = re.compile("\[[0-9]+\-[0-9]+\-[0-9]+ ([0-9]+):([0-9]+)\] (.*)$")

pg = re.compile("Guard \#([0-9]+) begins shift")

guard = -1
startmin = -1
asleep = False

for line in sys.stdin:
    #print(line)
    m = p.match(line)
    hour = int(m.group(1))
    min = int(m.group(2))
    event = m.group(3)

    if 'wakes up' in event:
        if asleep:
            for i in range(startmin, min):
                guards[guard][i] += 1
            asleep = False
    elif 'falls asleep' in event:
        if not asleep and guard != -1:
            asleep = True
            startmin = min
    elif 'Guard' in event:
        mg = pg.match(event)
        num = int(mg.group(1))
        guard = num
        if guard not in guards:
            guards[guard] = []
            for i in range(0, 60):
                guards[guard].append(0)


print(guards)

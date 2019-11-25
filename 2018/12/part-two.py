import sys
import re

line = sys.stdin.readline()

pinit = re.compile('initial state: ([#.]*)$')
minit = pinit.match(line)

initial = minit.group(1)

sys.stdin.readline()

p = re.compile('^([#.]{5}) => ([#.])$')

rules = []

for line in sys.stdin:
    m = p.match(line)
    rules.append((m.group(1), m.group(2)))


offset = 5000
state = '.' * offset + initial + offset * '.'


state = list(state)

def applyRule(x):
    x = ''.join(x)
    for rule, result in rules:
        if rule == x:
            return result
    return '.'

def printState(st):
    print(''.join(st))

def calcNum(st, off):
    st = ''.join(st)
    num = 0
    for i in range(0, len(st)):
        if st[i] == '#':
            num += i - off
    return(num)

states = []

states.append(state)

printState(states[0])

prevRes = 0
curRes = calcNum(states[0], offset)

#for i in range(0, 50000000000):
for i in range(0, 300):
    states.append(list(states[i]))
    for j in range(2, len(states[i]) - 2):
        #printState(states[i])
        #print(j, states[i][j-2:j+3])
        result = applyRule(states[i][j-2:j+3])

        #printState(states[i])
        if not result is None:
            states[i+1][j] = result
        #printState(states[i])

    printState(states[i+1])
    prevRes = curRes
    curRes = calcNum(states[i+1], offset)

print(calcNum(states[20], offset))
#print(calcNum(list('.#....##....#####...#######....#.#..##.'), 3))
print(curRes + (50000000000 - 300) * (curRes - prevRes))

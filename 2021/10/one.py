# 370707 too low

import sys
from math import floor

score = 0

points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

incompoints = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

incomscores = []

for line in sys.stdin:
    line = line.strip()
    stack = []
    failed = False
    for c in line:
        if c == '(':
            stack.append(')')
        elif c == '[':
            stack.append(']')
        elif c == '{':
            stack.append('}')
        elif c == '<':
            stack.append('>')
        else:
            top = stack.pop()
            if top != c:
                score += points[c]
                failed = True
                break
    if not failed:
        # incomplete, show me the stack
        stack = reversed(stack)
        linescore = 0
        for c in stack:
            linescore *= 5
            linescore += incompoints[c]
        incomscores.append(linescore)

print(score)

incomscores = sorted(incomscores)

print(incomscores[floor(len(incomscores)/2)])

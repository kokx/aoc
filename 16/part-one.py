import sys
import re

def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]

def addi(regs, a, b, c):
    regs[c] = regs[a] + b

def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]

def muli(regs, a, b, c):
    regs[c] = regs[a] * b

def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]

def bani(regs, a, b, c):
    regs[c] = regs[a] & b

def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]

def bori(regs, a, b, c):
    regs[c] = regs[a] | b

def setr(regs, a, b, c):
    regs[c] = regs[a]

def seti(regs, a, b, c):
    regs[c] = a

def gtir(regs, a, b, c):
    if a > regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def gtri(regs, a, b, c):
    if regs[a] > b:
        regs[c] = 1
    else:
        regs[c] = 0

def gtrr(regs, a, b, c):
    if regs[a] > regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def eqir(regs, a, b, c):
    if a == regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def eqri(regs, a, b, c):
    if regs[a] == b:
        regs[c] = 1
    else:
        regs[c] = 0

def eqrr(regs, a, b, c):
    if regs[a] == regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

operations = [addr, addi, mulr, muli,
              banr, bani, borr, bori,
              setr, seti,
              gtir, gtri, gtrr,
              eqir, eqri, eqrr]

#print(operations)

lines = sys.stdin.readlines()

pbef = re.compile('Before: \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]')
pdur = re.compile('([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)')
paft = re.compile('After:  \[([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+)\]')

total = 0

for i in range(0, len(lines), 4):
    mbefore = pbef.match(lines[i].strip())
    mop = pdur.match(lines[i+1].strip())
    mafter = paft.match(lines[i+2].strip())

    before = [int(mbefore.group(1)), int(mbefore.group(2)), int(mbefore.group(3)), int(mbefore.group(4))]
    op = [int(mop.group(1)), int(mop.group(2)), int(mop.group(3)), int(mop.group(4))]
    after = [int(mafter.group(1)), int(mafter.group(2)), int(mafter.group(3)), int(mafter.group(4))]

    num = 0

    for attempt in operations:
        test = list(before)
        attempt(test, op[1], op[2], op[3])
        if test == after:
            num += 1

    if num >= 3:
        total += 1
print(total)

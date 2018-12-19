import sys
import re

# guess 2913930 too low
# guess 8189644 too low
# guess 26930716 too high
# guess 18741072 correct

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

opsmap = {}

for op in operations:
    opsmap[op.__name__] = op

#print(opsmap)


ir = 0

program = []

for line in sys.stdin:
    line = line.strip().split(' ')

    if line[0] == '#ip':
        ir = int(line[1])
    else:
        inst = line[0]
        a = int(line[1])
        b = int(line[2])
        c = int(line[3])
        program.append((inst, a, b, c))

print(program)

registers = [1, 0, 0, 0, 0, 0]

while registers[ir] < len(program):
    pc = registers[ir]
    opname, a, b, c = program[pc]
    op = opsmap[opname]

    prevregs = list(registers)

    if pc == 3:
        if registers[2] % registers[1] == 0:
            registers[0] += registers[1]
        registers[5] = 11
    else:
        op(registers, a, b, c)

    #print(prevregs, program[pc], registers)

    registers[ir] += 1

print(registers)

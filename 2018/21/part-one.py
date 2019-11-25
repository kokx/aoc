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

#print(program)

#minnum = 9999999999999

for i in range(3173685, 100000000):
    registers = [i, 0, 0, 0, 0, 0]

    num = 0

    found = {}

    while registers[ir] < len(program):
        pc = registers[ir]
        opname, a, b, c = program[pc]
        op = opsmap[opname]

        #prevregs = list(registers)

        op(registers, a, b, c)

        #print(prevregs, program[pc], registers, '--', num)

        num += 1
        registers[ir] += 1
        if pc == 29:
            if registers[3] in found:
                print('Repeat!')
                break
            if not registers[3] in found:
                found[registers[3]] = num
            #print('Check', i, 'm3:', found)
            #print(registers)
            #print('r0: %d, r3: %d, r4: %d, r5: %d' % (registers[0], registers[3], registers[4], registers[5]))
            #print('----------')
        if pc == 29 and registers[ir] > 30:
            print(i, 'finished', registers[ir])
            sys.exit(0)
        if num > 100000000000:
            break
    print(found)
    sys.exit(1)

#print(registers)

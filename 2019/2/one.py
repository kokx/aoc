import sys
import math

program = []

for line in sys.stdin:
    program += line.strip().split(',')

program = list(map(int, program))

# for first star, gravity assist
#program[1] = 12
#program[2] = 2
program[1] = 86
program[2] = 9

pc = 0

while True:
    op = program[pc]

    if op == 99:
        print('Exit')
        break

    first = program[pc+1]
    second = program[pc+2]
    out = program[pc+3]

    if op == 1:
        program[out] = program[first] + program[second]
    elif op == 2:
        program[out] = program[first] * program[second]

    print(op, first, second, out)

    pc += 4

print(program)
print(program[0])

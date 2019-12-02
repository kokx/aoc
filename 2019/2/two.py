import sys
import math

program = []

for line in sys.stdin:
    program += line.strip().split(',')

program = list(map(int, program))

oldprogram = program.copy()

for i in range(0, 1000):
    for j in range(0, 1000):
        program = oldprogram.copy()

        # for first star, gravity assist
        program[1] = i
        program[2] = j

        pc = 0
        error = False

        while True:
            op = program[pc]

            if op == 99:
                #print('Exit')
                break

            first = program[pc+1]
            second = program[pc+2]
            out = program[pc+3]

            if first >= len(program) or second >= len(program) or out >= len(program):
                error = True
                break

            if op == 1:
                program[out] = program[first] + program[second]
            elif op == 2:
                program[out] = program[first] * program[second]

            #print(op, first, second, out)

            pc += 4
        if program[0] == 19690720 and not error:
            print(i, j)
            print(100*i + j)

        #print(program)
        #print(program[0])

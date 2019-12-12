import sys
import math
import random
from collections import Counter

bodies = [
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]
]
bodies = [
    [-8, -10, 0],
    [5, 5, 10],
    [2, -7, 3],
    [9, -8, -3],
]
bodies = [
    [-8, -18, 6],
    [-11, -14, 4],
    [8, -3, -10],
    [-2, -16, 1]
]

velocities = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

def lcm(x, y):
    return x // math.gcd(x, y) * y

seen = [set(), set(), set()]
rep = [None, None, None]

print(0, bodies, velocities)

# we will never reach this amount of repetitions, was chosen by the first sample input
for step in range(4686774924):
    # apply gravity
    for num1 in range(len(bodies)):
        for num2 in range(num1, len(bodies)):
            if num1 == num2:
                continue

            body1 = bodies[num1]
            body2 = bodies[num2]

            for i in range(3):
                if body1[i] > body2[i]:
                    velocities[num1][i] -= 1
                    velocities[num2][i] += 1
                elif body1[i] < body2[i]:
                    velocities[num1][i] += 1
                    velocities[num2][i] -= 1

    # apply velocity
    for num1 in range(len(bodies)):
        for i in range(3):
            bodies[num1][i] += velocities[num1][i]

    if step % 10000 == 0:
        print(step+1, bodies, velocities)
    #print(step+1, bodies, velocities)

    # find a repetition in every dimension
    for i in range(3):
        if rep[i]:
            continue
        k = []
        for num1 in range(len(bodies)):
            k.append((bodies[num1][i], velocities[num1][i]))
        k = tuple(k)
        if k in seen[i]:
            rep[i] = step
        seen[i].add(k)

    if rep[0] and rep[1] and rep[2]:
        break;

# calculate energy
energy = 0
for num1 in range(len(bodies)):
    a = 0
    b = 0
    for i in range(3):
        a += abs(bodies[num1][i])
        b += abs(velocities[num1][i])
    energy += a * b
print(energy)

print(rep[0], rep[1], rep[2])
print(lcm(lcm(rep[0], rep[1]), rep[2]))

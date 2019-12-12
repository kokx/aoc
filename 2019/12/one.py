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

print(0, bodies, velocities)

for step in range(1000):
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

    print(step+1, bodies, velocities)

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

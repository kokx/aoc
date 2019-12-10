import sys
import math
import random
from collections import Counter

ilines = ""

for line in sys.stdin:
    # todo do processing, uncomment split for splitting on comma and fix
    ilines += line.strip()

#wide = 3
#tall = 2
wide = 25
tall = 6

layers = []

pos = 0

print(len(ilines))
print(len(ilines)/(25*6))

while len(layers)*wide*tall < len(ilines):
    layer = []
    for i in range(tall):
        line = []
        for j in range(wide):
            line.append(ilines[pos])
            pos += 1
        layer.append(line)
    print(len(layer), layer)
    layers.append(layer)

leastzeroes = 99999999999999999999999999999
numberones = 0
numbertwos = 0

for layer in layers:
    zeroes = 0
    ones = 0
    twos = 0
    for line in layer:
        zeroes += line.count('0')
        ones += line.count('1')
        twos += line.count('2')
    if zeroes < leastzeroes:
            leastzeroes = zeroes
            numberones = ones
            numbertwos = twos

# 1340
print(numberones*numbertwos)

grid = layers[0]

for layer in layers:
    for i in range(0,len(layer)):
        for j in range(0, len(layer[i])):
            if grid[i][j] != 'W' and grid[i][j] != ' ':
                if layer[i][j] == '1':
                    grid[i][j] = 'W'
                elif layer[i][j] == '0':
                    grid[i][j] = ' '
                # otherwise 2, keep it this way

for line in grid:
    print(''.join(line))

import sys
import math
import random
import re
from collections import Counter

input_nums = []

for line in sys.stdin:
    input_nums = input_nums + list(line.strip())

input_nums = list(map(lambda x : int(x), input_nums))

# copy input numbers
numbers = input_nums[:]

length = len(numbers)

for phase in range(100):
    prev = numbers[:]

    for i in range(length):
        j = i
        step = i + 1
        nusum = 0

        while j < length:
            nusum += sum(prev[j:j + step])
            j += 2 * step
            nusum -= sum(prev[j:j + step])
            j += 2 * step

        numbers[i] = abs(nusum) % 10

toprint = ""
for i in range(8):
    toprint += str(numbers[i])

print(toprint)

offset = int(''.join(map(str, input_nums[:7])))

numbers = (input_nums * 10000)[offset:]
length = len(numbers)

for step in range(100):
    for i in range(length - 2, -1, -1):
        numbers[i] += numbers[i + 1]
        numbers[i] %= 10

toprint = ""
for i in range(8):
    toprint += str(numbers[i])

print(toprint)

import sys
import numpy as np

p1 = 0

def get_map(patterns):
    one = np.array(list(list(filter(lambda x: len(x)==2, patterns))[0]))
    seven = np.array(list(list(filter(lambda x: len(x)==3, patterns))[0]))
    four = np.array(list(list(filter(lambda x: len(x)==4, patterns))[0]))
    lights = {}
    for reading in patterns:
        for seglight in list(reading):
            if seglight not in lights:
                lights[seglight] = 0
            lights[seglight] += 1
    for k, v in lights.items():
        if v == 9:
            lights[k] = 'f'
        elif v == 4:
            lights[k] = 'e'
        elif v == 6:
            lights[k] = 'b'
        elif v == 8:
            if k in seven and k in one:
                lights[k] = 'c'
            else:
                lights[k] = 'a'
        elif v == 7:
            if k in four:
                lights[k] = 'd'
            else:
                lights[k] = 'g'

    return lights

for line in sys.stdin:
    [inp, output] = line.strip().split(' | ')

    patterns = inp.split(' ') + output.split(' ')

    print(get_map(patterns))

    for word in output.split(' '):
        if len(word) == 2:
            p1 += 1
        elif len(word) == 4:
            p1 += 1
        elif len(word) == 3:
            p1 += 1
        elif len(word) == 7:
            p1 += 1

print(p1)

import sys
import math
import random
import re
from collections import Counter

reactions = {}

resp = re.compile('^([0-9]+) ([A-Z]+)$')

for line in sys.stdin:
    ingredients, result = line.strip().split('=>')
    ingredients = map(lambda x: x.strip(), ingredients.strip().split(','))
    ingredients = map(lambda x: resp.match(x).groups(), ingredients)
    ingredients = map(lambda x: (int(x[0]), x[1]), ingredients)
    result = resp.match(result.strip()).groups()

    if result[1] in reactions:
        print('WAIT THIS MIGHT GO WRONG')

    reactions[result[1]] = (int(result[0]), list(ingredients))


leftovers = {}

def get_ore(typ, num):
    if typ == 'ORE':
        return num

    if typ in leftovers:
        if num <= leftovers[typ]:
            leftovers[typ] -= num
            return 0
        else:
            num -= leftovers[typ]
            leftovers[typ] = 0

    req = reactions[typ]
    if req[0] < num:
        fac = math.ceil(num / req[0])

        newneeded = []
        for ing in req[1]:
            newneeded.append((ing[0]*fac, ing[1]))
        # scale req to new size
        req = (req[0]*fac, newneeded)

    if req[0] > num:
        if not typ in leftovers:
            leftovers[typ] = 0
        leftovers[typ] += req[0] - num
        num = req[0]

    total = 0

    for ing in req[1]:
        # fix each ingredient
        total += get_ore(ing[1], ing[0])

    return total

# TODO: calculate for fuewl
print(get_ore('FUEL', 1))

searchfor = 1000000000000
#            999999790958
mx = 1000000000000
mn = 1

last = (mx, mn)

# high: 3756878

while True:
    halfway = (mx + mn) // 2
    num = get_ore('FUEL', halfway)

    if num == searchfor:
        print(halfway)
        break

    if num > searchfor:
        mx = halfway
    if num < searchfor:
        mn = halfway

    if (mx, mn) == last:
        print(mn)
        break
    last = (mx, mn)

import sys
from collections import defaultdict
from math import floor

orig_template = sys.stdin.readline().strip()
template = orig_template

sys.stdin.readline()

rules = {}

for line in sys.stdin:
    line = line.strip().split(' -> ')
    rules[line[0]] = line[1]

def get_pairs(template):
    return [a + b for a, b in zip(template[:-1], template[1:])]

def expand(template):
    pairs = get_pairs(template)
    new = template[0]
    for pair in pairs:
        new += rules[pair] + pair[1]
    return new


for i in range(10):
    template = expand(template)

counts = {}

for c in template:
    if not c in counts:
        counts[c] = 0
    counts[c] += 1

most = 0
least = 99999999999999999

for c, v in counts.items():
    if v > most:
        most = v
    if v < least:
        least = v

print(most - least)

# yeah not working for part 2, lets do that differently

pairs = {}

for pair in get_pairs(orig_template):
    if not pair in pairs:
        pairs[pair] = 0
    pairs[pair] += 1

for _ in range(40):
    new_pairs = {}
    for pair, v in pairs.items():
        p1 = pair[0] + rules[pair]
        p2 = rules[pair] + pair[1]

        if not p1 in new_pairs:
            new_pairs[p1] = 0
        new_pairs[p1] += v
        if not p2 in new_pairs:
            new_pairs[p2] = 0
        new_pairs[p2] += v

    pairs = new_pairs

counts = defaultdict(int)

for p, v in pairs.items():
    counts[p[0]] += v
    counts[p[1]] += v

counts[orig_template[-1]] += 1

most = 0
least = 99999999999999999

for c, v in counts.items():
    if v > most:
        most = v
    if v < least:
        least = v

most = floor(most / 2)
least = floor(least / 2)

print(most - least)

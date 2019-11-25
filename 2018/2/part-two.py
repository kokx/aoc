import sys

def diff(a, b):
    d = 0
    for i in range(0, len(a)):
        if a[i] != b[i]:
            d += 1
    return d

lines = []

for line in sys.stdin:
    lines.append(line)

for i in range(0, len(lines) - 1):
    for j in range(i+1, len(lines)):
        if diff(lines[i], lines[j]) == 1:
            print(lines[i], lines[j])

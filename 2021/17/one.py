import sys

for line in sys.stdin:
    line = line.strip().split(' ')
    x = line[2].strip(',x=')
    y = line[3].strip(',y=')
    x1, x2 = [int(a) for a in x.split('..')]
    y1, y2 = [int(a) for a in y.split('..')]

    print(x1, x2)
    print(y1, y2)

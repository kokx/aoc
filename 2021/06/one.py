import sys

fishes = [int(x) for x in sys.stdin.readline().strip().split(',')]
#for line in sys.stdin:
#    line = line.strip()

invfishes = {}

for fish in fishes:
    if not fish in invfishes:
        invfishes[fish] = 0
    invfishes[fish] += 1

for i in range(80):
    newfishes = []
    append = []

    for fish in fishes:
        if fish == 0:
            append.append(8)
            newfishes.append(6)
        else:
            newfishes.append(fish-1)

    fishes = newfishes + append

print(len(fishes))

for i in range(256):
    newinvfishes = {}

    for days, num in invfishes.items():
        if days == 0:
            newinvfishes[8] = num

            if not 6 in newinvfishes:
                newinvfishes[6] = 0
            newinvfishes[6] += num
        else:
            nday = days - 1
            if not nday in newinvfishes:
                newinvfishes[nday] = 0
            newinvfishes[nday] += num

    invfishes = newinvfishes

total = 0

for days, num in invfishes.items():
    total += num

print(total)

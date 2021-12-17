import sys

crabs = [int(x) for x in sys.stdin.readline().strip().split(',')]

best = 99999999999999999
best2 = 999999999999999999

for i in range(min(crabs), max(crabs)):
    cost = 0
    for crab in crabs:
        cost += abs(crab - i)

    if cost < best:
        best = cost

    cost2 = 0
    for crab in crabs:
        diff = abs(crab - i)
        # OK, this is just n(n+1)/2 :D
        #for j in range(0, diff):
        #    usage += j + 1
        cost2 += (diff*(diff+1))/2

    if cost2 < best2:
        best2 = cost2

print(best)
print(best2)

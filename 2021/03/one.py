import sys

init = False
gamma0 = []
gamma1 = []

allnums = []

for line in sys.stdin:
    line = line.strip()

    if not init:
        for c in line:
            gamma0.append(0);
            gamma1.append(0);
        init = True

    num = 0
    for c in line:
        if c == '0':
            gamma0[num] += 1
        else:
            gamma1[num] += 1
        num += 1

    allnums.append(line)

gamma_bin = []
for (g0, g1) in zip(gamma0, gamma1):
    if g0 > g1:
        gamma_bin.append(0)
    else:
        gamma_bin.append(1)

gamma = 0
epsilon = 0

for b in gamma_bin:
    gamma = gamma * 2 + b
    epsilon = epsilon * 2 + abs(b-1)

print(gamma*epsilon)

oxynums = [x for x in allnums]

for i in range(0, len(oxynums[0])):
    if len(oxynums) == 1:
        break

    oxy_gamma_bin = []
    for j in range(0, len(gamma_bin)):
        g0 = 0
        g1 = 0
        for ln in oxynums:
            if ln[j] == '0':
                g0 += 1
            else:
                g1 += 1
        if g0 > g1:
            oxy_gamma_bin.append(0)
        else:
            oxy_gamma_bin.append(1)

    oxynums = [x for x in oxynums if int(x[i]) == oxy_gamma_bin[i]]

co2nums = [x for x in allnums]

for i in range(0, len(co2nums[0])):
    if len(co2nums) == 1:
        break

    co2_gamma_bin = []
    for j in range(0, len(gamma_bin)):
        g0 = 0
        g1 = 0
        for ln in co2nums:
            if ln[j] == '0':
                g0 += 1
            else:
                g1 += 1
        if g0 > g1:
            co2_gamma_bin.append(0)
        else:
            co2_gamma_bin.append(1)

    co2nums = [x for x in co2nums if int(x[i]) != co2_gamma_bin[i]]

oxy = 0
co2 = 0

for b in oxynums[0]:
    oxy = oxy * 2 + int(b)

for b in co2nums[0]:
    co2 = co2 * 2 + int(b)

print(oxy * co2)

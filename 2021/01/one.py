import sys

prev = 9999999999999999999999999999999999999999999999999999999
total = 0
total2 = 0

last3 = [prev, prev, prev]

for line in sys.stdin:
    num = int(line)
    if num > prev:
        total += 1
    prev = num

    if num + last3[1] + last3[2] > last3[0] + last3[1] + last3[2]:
        total2 += 1

    last3.pop(0)
    last3.append(num)
        

print(total)
print(total2)

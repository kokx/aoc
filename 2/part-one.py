import sys

twos = 0
threes = 0

for line in sys.stdin:
    chars = {}
    for char in line:
        if char not in chars:
            chars[char] = 0
        chars[char] += 1

    two = 0
    three = 0

    for k, v in chars.items():
        if v == 2:
            two = 1
        if v == 3:
            three = 1

    twos += two
    threes += three

print(twos * threes)

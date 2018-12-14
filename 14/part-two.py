import sys

ainput = 681901
#ainput = 92510

input = 37

inlist = []

def getDigits(num):
    ret = []
    while num > 0:
        ret.append(num % 10)
        num //= 10
    ret.reverse()
    return ret

def printList(lst, e1, e2):
    toprint = ''
    for i in range(0, len(lst)):
        if i == e1 and i == e2:
            toprint += '{%d}' % lst[i]
        elif i == e1:
            toprint += '(%d)' % lst[i]
        elif i == e2:
            toprint += '[%d]' % lst[i]
        else:
            toprint += ' %d ' % lst[i]
    print(toprint)

def getNum(lst, after):
    res = ''
    for i in range(after, after + 10):
        res += str(inlist[i])
    return res

inlist = getDigits(input)


elf1 = 0
elf2 = 1

printList(inlist, elf1, elf2)

dgts = getDigits(ainput)

for i in range(0, 2000*ainput):
    new = inlist[elf1] + inlist[elf2]
    if new > 0:
        inlist.extend(getDigits(new))
    else:
        inlist.append(0)

    elf1 = (elf1 + 1 + inlist[elf1]) % len(inlist)
    elf2 = (elf2 + 1 + inlist[elf2]) % len(inlist)
    #if elf1 == elf2:
    #    print('same', i)

    #printList(inlist, elf1, elf2)

    if i > 5:
        start = i - len(dgts)
        found = True
        for j in range(0, len(dgts)):
            if inlist[start + j] != dgts[j]:
                found = False
                break
        if found:
            print(start)
            break

#guess: 1459101223
sys.exit(0)

print(6, getNum(inlist, 6))
print(9, getNum(inlist, 9))
print(5, getNum(inlist, 5))
print(18, getNum(inlist, 18))
print(2018, getNum(inlist, 2018))
print(ainput, getNum(inlist, ainput))

print()

dgts = getDigits(ainput)
for i in range(0, len(inlist)):
    found = True
    for j in range(0, len(dgts)):
        if inlist[i+j] != dgts[j]:
            found = False
            break
    if found:
        print(i)
        break

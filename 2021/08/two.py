def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def sevseg2(arr):
    total = 0
    numbers = [0]*10
    for L in arr:
        # correct = ['abcefg','cf','acdeg','acdfg','bcdf','abdfg','abdefg','acf','abcdefg','abcdfg']
        s =["".join(sorted(x)) for x in L]
        numbers[1] = next(filter(lambda s: len(s) == 2, s), None)
        numbers[4] = next(filter(lambda s: len(s) == 4, s), None)
        numbers[7] = next(filter(lambda s: len(s) == 3, s), None)
        numbers[8] = next(filter(lambda s: len(s) == 7, s), None)
        for item in s:
            if len(item) == 6:
                if numbers[1][0] in item and numbers[1][1] in item:
                    if len(intersection(item, numbers[4])) == 3:
                        numbers[0] = item
                    else:
                        numbers[9] = item
                else:
                    numbers[6] = item
            elif len(item) == 5:
                if numbers[1][0] in item and numbers[1][1] in item:
                    numbers[3] = item
                elif len([_ for _ in item if _ in numbers[4]]) == 2:
                    numbers[2] = item
                else:
                    numbers[5] = item
        this_line = []
        for x in s[11::]:
            this_line.append(numbers.index(x))
        total += int("".join([str(i) for i in this_line]))
    return(total)

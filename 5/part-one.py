import sys

for line in sys.stdin:

    prev = ''

    nextLine = ''

    line = line.strip()

    while True:
        #print(line, len(line), len(nextLine))
        nextLine = line
        for i in range(0, len(line)):
            if prev != line[i] and (prev == line[i].lower() or prev == line[i].upper()):
                # remove two chars from nextLine
                print('Removing %s (%s, %s)' % (nextLine[i-1:i+1], prev, line[i]))
                nextLine = nextLine[:i-1] + nextLine[i+1:]
                prev = ''
                break

            prev = line[i]

        if len(nextLine) == len(line):
            break
        line = nextLine

print(len(line))


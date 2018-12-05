import sys

for line in sys.stdin:

    prev = ''

    nextLine = ''

    origline = line.strip()

    lowestLine = ''
    lowestLen = 999999999999999

    for c in 'abcdefghijklmnopqrstuvwxyz':
        line = origline

        # remove all c and c.upper()
        bline = line.replace(c, '').replace(c.upper(), '')
        line = bline

        while True:
            #print(line, len(line), len(nextLine))
            nextLine = line
            prev = ''
            for i in range(0, len(line)):
                if prev != line[i] and (prev == line[i].lower() or prev == line[i].upper()):
                    # remove two chars from nextLine
                    #print('Removing %s (%s, %s) (%d, %d) %s' % (nextLine[i-1:i+1], prev, line[i], i-1, i, nextLine[:i-1] + nextLine[i+1:]))
                    nextLine = nextLine[:i-1] + nextLine[i+1:]
                    prev = ''
                    break

                prev = line[i]

            if len(nextLine) == len(line):
                break
            line = nextLine

        print(c, len(line))

        if len(line) < lowestLen:
            lowestLine = line
            lowestLen = len(line)
    print(lowestLen)


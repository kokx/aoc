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

            for chr in 'abcdefghijklmnopqrstuvwxyz':
                nextLine = nextLine.replace(chr + chr.upper(), '').replace(chr.upper() + chr, '')

            if len(nextLine) == len(line):
                break
            line = nextLine

        print(c, len(line))

        if len(line) < lowestLen:
            lowestLine = line
            lowestLen = len(line)
    print(lowestLen)


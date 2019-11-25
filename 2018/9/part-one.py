import sys
import re
import collections

p = re.compile('^([0-9]+) players; last marble is worth ([0-9]+) points')


for line in sys.stdin:
    m = p.match(line)
    nPlayers = int(m.group(1))
    nMarbles = int(m.group(2))

    circle = []
    balls = [x for x in range(0, nMarbles+1)]

    points = [0 for i in range(0, nPlayers)]
    curPlayer = 0
    curPos = 0

    # before first player starts, ball 0 is placed
    circle.append(balls.pop(0))

    while len(balls) > 0:
        ball = balls.pop(0)
        # current player places ball
        if ball % 23 == 0:
            newPos = (curPos - 7) % len(circle)
            remov = circle[newPos]
            circle = circle[:newPos] + circle[newPos+1:]
            curPos = newPos
            #print('shitshit:', remov, circle)
            points[curPlayer] += ball + remov
        else:
            newPos = ((curPos + 1) % len(circle)) + 1
            circle = circle[:newPos] + [ball] + circle[newPos:]
            curPos = newPos
            #print('otherwise', ball, circle)
        curPlayer = (curPlayer + 1) % nPlayers

    high = max(points)
    print(high)

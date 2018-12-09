import sys
import re
import collections

p = re.compile('^([0-9]+) players; last marble is worth ([0-9]+) points')


for line in sys.stdin:
    m = p.match(line)
    nPlayers = int(m.group(1))
    nMarbles = int(m.group(2)) * 100

    circle = collections.deque()
    balls = collections.deque([x for x in range(0, nMarbles+1)])

    points = [0 for i in range(0, nPlayers)]
    curPlayer = 0
    curPos = 0

    # before first player starts, ball 0 is placed
    circle.append(balls.popleft())

    while len(balls) > 0:
        ball = balls.popleft()
        # current player places ball
        if ball % 23 == 0:
            circle.rotate(7)
            remov = circle.popleft()
            #print('shitshit:', remov, circle)
            points[curPlayer] += ball + remov
        else:
            circle.rotate(-2)
            circle.appendleft(ball)
            #print('otherwise', ball, circle)
        curPlayer = (curPlayer + 1) % nPlayers

    high = max(points)
    print(high)

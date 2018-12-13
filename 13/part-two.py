import sys

grid = []
carts = {}

lnum = 0
for line in sys.stdin:
    grid.append([])
    cnum = 0
    for c in line:
        if c == '\n':
            break
        if c == 'v' or c == '^':
            carts[(lnum, cnum)] = (0, c)
            grid[lnum].append('|')
        elif c == '<' or c == '>':
            carts[(lnum, cnum)] = (0, c)
            grid[lnum].append('-')
        else:
            grid[lnum].append(c)
        cnum += 1
    lnum += 1

def printGrid(dat):
    for line in dat:
        ln = ''
        for ch in line:
            ln += ch
        print(ln)

def printCartsGrid(dat, carts):
    lnum = 0
    for line in dat:
        ln = ''
        cnum = 0
        for ch in line:
            if (lnum, cnum) in carts:
                ln += carts[(lnum, cnum)][1]
            else:
                ln += ch
            cnum += 1
        print(ln)
        lnum += 1

def getNext(cart, state):
    if state[1] == '>':
        return (cart[0], cart[1] + 1)
    elif state[1] == '<':
        return (cart[0], cart[1] - 1)
    elif state[1] == '^':
        return (cart[0] - 1, cart[1])
    elif state[1] == 'v':
        return (cart[0] + 1, cart[1])
    return (-1, -1)

def turn(state):
    if state[0] == 0:
        #left
        if state[1] == '^':
            return (1, '<')
        if state[1] == '>':
            return (1, '^')
        if state[1] == 'v':
            return (1, '>')
        if state[1] == '<':
            return (1, 'v')
    elif state[0] == 1:
        return (2, state[1])
    elif state[0] == 2:
        # right
        if state[1] == '^':
            return (0, '>')
        if state[1] == '>':
            return (0, 'v')
        if state[1] == 'v':
            return (0, '<')
        if state[1] == '<':
            return (0, '^')
    else:
        print('Wrong state')

def corner(state, corner):
    if corner == '/':
        if state[1] == '^':
            return (state[0], '>')
        if state[1] == '>':
            return (state[0], '^')
        if state[1] == 'v':
            return (state[0], '<')
        if state[1] == '<':
            return (state[0], 'v')
    elif corner == '\\':
        if state[1] == '^':
            return (state[0], '<')
        if state[1] == '>':
            return (state[0], 'v')
        if state[1] == 'v':
            return (state[0], '>')
        if state[1] == '<':
            return (state[0], '^')
    else:
        print('Wrong call to corner')

def sim(grid, carts, i):
    ckeys = sorted(carts.keys())

    newCarts = {}

    maybec = set()

    collisions = set()

    for cart in ckeys:
        # move all carts one forward
        next = getNext(cart, carts[cart])
        #print(next)
        if grid[next[0]][next[1]] == '+':
            nextState = turn(carts[cart])
            #print(next, nextState)
        elif grid[next[0]][next[1]] == '/' or grid[next[0]][next[1]] == '\\':
            nextState = corner(carts[cart], grid[next[0]][next[1]])
        else:
            nextState = carts[cart]
        if next in newCarts:
            print('COLLISION!!!! (%d,%d)' % (next[1], next[0]))
            collisions.add(next)
            # remove the other cart, and the current one
            del newCarts[next]
        elif next in collisions:
            print('TRIPLE COLLISION!!!! (%d,%d)' % (next[1], next[0]))
            # do not do anything, don't add to next state
        else:
            if next in carts:
                if cart in maybec:
                    print('DEFCOL (%d,%d)' % (next[1], next[0]))
                    del[newCarts[cart]]
                    continue
                maybec.add(next)
                print('MAYBECOLLISION?')
                #printCartsGrid(grid, carts)
            #print(next, nextState)
            newCarts[next] = nextState
    if len(collisions) > 0:
        print(len(carts), len(newCarts))
    if len(newCarts) == 1:
        cart = list(newCarts.keys())[0]
        print(newCarts, 'ans: (%d,%d)' % (cart[1], cart[0]))
        sys.exit(0)

    return newCarts

for i in range(0, 150000):
    carts = sim(grid, carts, i)

    #printCartsGrid(grid, carts)

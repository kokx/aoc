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
    occupied = set(carts.keys())

    newCarts = {}

    for cart in ckeys:
        if not cart in occupied:
            print('COLLISION INTO ME!!!!', cart)
            continue
        occupied.remove(cart)

        # determine state
        next = getNext(cart, carts[cart])
        if grid[next[0]][next[1]] == '+':
            nextState = turn(carts[cart])
        elif grid[next[0]][next[1]] == '/' or grid[next[0]][next[1]] == '\\':
            nextState = corner(carts[cart], grid[next[0]][next[1]])
        else:
            nextState = carts[cart]
        newCarts[next] = nextState

        if next in occupied:
            print('COLLISION INTO OTHER CART', next)
            occupied.remove(next)
        else:
            occupied.add(next)
            newCarts[cart] = next

    nextCarts = {}

    for cart, state in newCarts.items():
        if cart in occupied:
            nextCarts[cart] = state

    return nextCarts

for i in range(0, 150000):
    carts = sim(grid, carts, i)

    if len(carts) == 1:
        last = list(carts)[0]
        print("Last one: (%d,%d)" % (last[1], last[0]))
        break

    #printCartsGrid(grid, carts)

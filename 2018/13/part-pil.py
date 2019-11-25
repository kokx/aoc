import sys
from PIL import Image, ImageDraw

def gridImage(grid, cycle, carts):
    scale = 7
    half = scale // 2
    img_height = len(grid) * scale
    img_width = len(grid[0]) * scale

    track_size = 1
    cart_size = 2

    img = Image.new('RGBA', (img_width, img_height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # draw the grid
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            top = scale * i
            left = scale * j
            ch = grid[i][j]
            if ch == '|':
                draw.line(((left + half, top), (left + half, top + scale)), 'black', track_size)
            elif ch == '-':
                draw.line(((left, top + half), (left + scale, top + half)), 'black', track_size)
            elif ch == '+':
                # draw both
                draw.line(((left + half, top), (left + half, top + scale)), 'black', track_size)
                draw.line(((left, top + half), (left + scale, top + half)), 'black', track_size)
            elif ch == '/':
                draw.line(((left, top + scale), (left + scale, top)), 'black', track_size)
            elif ch == '\\':
                draw.line(((left, top), (left + scale, top + scale)), 'black', track_size)

    # draw the carts
    for cart, state in carts.items():
        top = cart[0] * scale
        left = cart[1] * scale
        if state[1] == '>':
            draw.line(((left, top), (left + scale, top + half)), 'red', cart_size)
            draw.line(((left, top + scale), (left + scale, top + half)), 'red', cart_size)
        elif state[1] == '<':
            draw.line(((left, top + half), (left + scale, top)), 'red', cart_size)
            draw.line(((left, top + half), (left + scale, top + scale)), 'red', cart_size)
        elif state[1] == '^':
            draw.line(((left, top + scale), (left + half, top)), 'red', cart_size)
            draw.line(((left + scale, top + scale), (left + half, top)), 'red', cart_size)
        elif state[1] == 'v':
            draw.line(((left, top), (left + half, top + scale)), 'red', cart_size)
            draw.line(((left + scale, top), (left + half, top + scale)), 'red', cart_size)

    del draw
    img.save('imgs/%05d.png' % cycle)

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

gridImage(grid, 0, carts)

for i in range(0, 150000):
    carts = sim(grid, carts, i)

    gridImage(grid, i+1, carts)

    if len(carts) == 1:
        last = list(carts)[0]
        print("Last one: (%d,%d)" % (last[1], last[0]))
        break
    #printCartsGrid(grid, carts)


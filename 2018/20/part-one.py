import sys
import networkx

grid = networkx.Graph()

paths = sys.stdin.read()

pos = {0}
stack = []
starts, ends = {0}, set()

for c in paths:
    if c == '^':
        print('Start reading maze')
    elif c == '$':
        print('Finished reading maze')
    elif c == '|':
        ends.update(pos)
        pos = starts
    elif c in 'NESW':
        # we'll use complex numbers to denote vertices in the grid,
        # normal part for N/S direction and imaginary part for EW direction
        direction = 0
        if c == 'N':
            direction = 1
        elif c == 'E':
            direction = 1j
        elif c == 'S':
            direction = -1
        elif c == 'W':
            direction = -1j
        grid.add_edges_from((p, p + direction) for p in pos)
        pos = {p + direction for p in pos}
    elif c == '(':
        stack.append((starts, ends))
        starts, ends = pos, set()
    elif c == ')':
        starts, ends = stack.pop()
        ends.update(pos)

# find the shortest path lengths from the starting room to all other rooms
lengths = networkx.algorithms.shortest_path_length(grid, 0)

print(max(lengths.values()))
print(sum(1 for length in lengths.values() if length >= 1000))

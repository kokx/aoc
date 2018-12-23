import networkx as nx
# guess


depth = 7863
target = (14, 760)

# for sample:
#depth = 510
#target = (10, 10)

maxx = target[0] + 100
maxy = target[1] + 100

grid = []
rgrid = []

for y in range(0, maxy):
    grid.append([])
    rgrid.append([])
    for x in range(0, maxx):
        if x == 0 and y == 0:
            geo = 0
        elif x == target[0] and y == target[1]:
            geo = 0
        elif y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            geo = grid[y][x-1] * grid[y-1][x]

        grid[y].append((geo + depth) % 20183)
        rgrid[y].append(grid[y][x] % 3)

def printgrid(grid):
    for line in grid:
        ln = ''
        for ch in line:
            if ch == 0:
                ln += '.'
            elif ch == 1:
                ln += '='
            elif ch == 2:
                ln += '|'
        print(ln)

def riskLevel(grid, target):
    maxx, maxy = target
    level = 0
    for y in range(0, maxy + 1):
        for x in range(0, maxx + 1):
            level += grid[y][x]
    return level

printgrid(rgrid)

print(riskLevel(rgrid, target))

G = nx.Graph()

def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]

def get_types(num):
    if num == 0:
        return [0, 1]
    if num == 1:
        return [1, 2]
    if num == 2:
        return [0, 2]
    else:
        print(num)
        return -1

def grid_types(grid, location):
    x, y = location
    return get_types(grid[y][x])

def add_neighbor_edges(G, grid, source, target):
    types = intersection(grid_types(grid, source), grid_types(grid, target))
    for tp in types:
        G.add_edge((tp, source[0], source[1]), (tp, target[0], target[1]), weight=1)

def add_cross_edges(G, grid, source):
    types = grid_types(grid, source)
    G.add_edge((types[0], source[0], source[1]), (types[1], source[0], source[1]), weight=7)

# build the graph
# the graph has 3 layers:
# 0. torch, where you use the torch tool
# 1. climbing, where you use the climbing gear
# 2. neither, where you use no tool
# both the start and end are at the torch layer
#
# edges are bidirectional, thus we only add edges to the
# vertices one down and one to the right. This makes us miss
# the last column and row partially, but that is not a problem
# (we'll just make the margin one bigger)
for y in range(0, maxy - 1):
    for x in range(0, maxx - 1):
        add_neighbor_edges(G, rgrid, (x, y), (x+1, y))
        add_neighbor_edges(G, rgrid, (x, y), (x, y+1))

        add_cross_edges(G, rgrid, (x, y))

print(nx.dijkstra_path_length(G, (0, 0, 0), (0, target[0], target[1])))

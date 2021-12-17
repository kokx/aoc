import sys
import networkx as nx

grid = []

for line in sys.stdin:
    grid.append([int(x) for x in line.strip()])

G = nx.DiGraph()

for i in range(len(grid)):
    for j in range(len(grid[i])):
        G.add_edge((i, j, 0), (i, j, 1), weight=grid[i][j])
        if i > 0:
            G.add_edge((i - 1, j, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i - 1, j, 0), weight=0)
        if i < len(grid) - 1:
            G.add_edge((i + 1, j, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i + 1, j, 0), weight=0)
        if j > 0:
            G.add_edge((i, j - 1, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i, j - 1, 0), weight=0)
        if j < len(grid[i]) - 1:
            G.add_edge((i, j + 1, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i, j + 1, 0), weight=0)

source = (0, 0, 1)
target = (len(grid) - 1, len(grid[len(grid) - 1]) - 1, 1)

result = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, source, target)

print(result[0])

def calcweight(a, b, w):
    return (((w - 1) + (a + b)) % 9) + 1

ngrid = []

for a in range(5):
    for i in range(len(grid)):
        gline = []
        for b in range(5):
            for j in range(len(grid[i])):
                gline.append(calcweight(a, b, grid[i][j]))
            #gline.append(' ')
        ngrid.append(gline)
    #ngrid.append([' ' for x in ngrid[len(ngrid)-1]])

def printgrid(g):
    for row in g:
        print(''.join(str(x) for x in row))

#printgrid(ngrid)
#sys.exit(1)

for i in range(len(ngrid)):
    for j in range(len(ngrid[i])):
        G.add_edge((i, j, 0), (i, j, 1), weight=ngrid[i][j])
        if i > 0:
            G.add_edge((i - 1, j, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i - 1, j, 0), weight=0)
        if i < len(ngrid) - 1:
            G.add_edge((i + 1, j, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i + 1, j, 0), weight=0)
        if j > 0:
            G.add_edge((i, j - 1, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i, j - 1, 0), weight=0)
        if j < len(ngrid[i]) - 1:
            G.add_edge((i, j + 1, 1), (i, j, 0), weight=0)
            G.add_edge((i, j, 1), (i, j + 1, 0), weight=0)

source = (0, 0, 1)
target = (len(ngrid) - 1, len(ngrid[len(ngrid) - 1]) - 1, 1)

result = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, source, target)

print(result[0])

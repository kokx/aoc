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

G = nx.DiGraph()

def calcweight(a, b, w):
    return (((w - 1) + a + b) % 9) + 1

for a in range(5):
    for b in range(5):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                G.add_edge((a, b, i, j, 0), (a, b, i, j, 1), weight=calcweight(a, b, grid[i][j]))
                if i > 0:
                    G.add_edge((a, b, i - 1, j, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a, b, i - 1, j, 0), weight=0)
                if i < len(grid) - 1:
                    G.add_edge((a, b, i + 1, j, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a, b, i + 1, j, 0), weight=0)
                if j > 0:
                    G.add_edge((a, b, i, j - 1, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a, b, i, j - 1, 0), weight=0)
                if j < len(grid[i]) - 1:
                    G.add_edge((a, b, i, j + 1, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a, b, i, j + 1, 0), weight=0)

                # also for cross-edges
                if i == 0 and a > 0:
                    G.add_edge((a - 1, b, len(grid) - 1, j, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a - 1, b, len(grid) - 1, j, 0), weight=0)
                if j == 0 and b > 0:
                    G.add_edge((a, b - 1, i, len(grid[i]) - 1, 1), (a, b, i, j, 0), weight=0)
                    G.add_edge((a, b, i, j, 1), (a, b - 1, i, len(grid[i]) - 1, 0), weight=0)

source = (0, 0, 0, 0, 1)
target = (4, 4, len(grid) - 1, len(grid[len(grid) - 1]) - 1, 1)

result = nx.algorithms.shortest_paths.weighted.single_source_dijkstra(G, source, target)

print(result[0])

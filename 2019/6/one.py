import sys
import math
import networkx as nx

data = {'COM': 0}

G = nx.DiGraph()
G.add_node('COM')

prev = {'COM': ''}

for line in sys.stdin:
    orbit = line.strip().split(')')

    if not orbit[0] in G.nodes():
        G.add_node(orbit[0])
    if not orbit[1] in G.nodes():
        G.add_node(orbit[1])
    G.add_edge(orbit[1], orbit[0])
    prev[orbit[1]] = orbit[0]

sorted = reversed(list(nx.topological_sort(G)))

for node in sorted:
    if node == 'COM':
        continue

    data[node] = data[prev[node]] + 1

print(sum(data.values()))

H = G.to_undirected()

print(len(nx.shortest_path(H, 'SAN', 'YOU')) - 3)

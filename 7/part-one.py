import sys
import re
from functools import reduce

def toposort2(data):
    """Dependencies are expressed as a dictionary whose keys are items
and whose values are a set of dependent items. Output is a list of
sets in topological order. The first set consists of items with no
dependences, each subsequent set consists of items that depend upon
items in the preceeding sets.

>>> print '\\n'.join(repr(sorted(x)) for x in toposort2({
...     2: set([11]),
...     9: set([11,8]),
...     10: set([11,3]),
...     11: set([7,5]),
...     8: set([7,3]),
...     }) )
[3, 5, 7]
[8, 11]
[2, 9, 10]

"""

    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.values()) - set(data.keys())
    # Add empty dependences where needed
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.items() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.items()
                    if item not in ordered}
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.items())


graph = {}

p = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

for line in sys.stdin:
    m = p.match(line)
    fro = m.group(1)
    to = m.group(2)

    if not fro in graph:
        graph[fro] = set()

    graph[fro].add(to)

sorted = [next for next in toposort2(graph)]
sorted.reverse()

print(graph)
print(sorted)

answer = ''

for st in sorted:
    all = list(st)
    all.sort()
    for item in all:
        answer += item
print(answer)

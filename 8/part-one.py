import sys

def parseRec(l):
    nc = data.pop(0)
    nm = data.pop(0)

    #print(l, nc, nm)

    children = []
    metadata = []

    for i in range(0, nc):
        children.append(parseRec(l+1))

    for i in range(0, nm):
        metadata.append(data.pop(0))

    return (nc, nm, children, metadata)

def sum(node):
    sm = 0
    children = node[2]
    metadata = node[3]
    for m in metadata:
        sm += m
    for c in children:
        sm += sum(c)
    return sm

def advSum(node):
    nc, nm, children, metadata = node
    if nc == 0:
        return sum(node)
    sm = 0
    for m in metadata:
        if m <= nc:
            sm += advSum(children[m-1])
    return sm

for line in sys.stdin:
    data = line.split(' ')
    data = [int(x) for x in data]

    tree = parseRec(0)

    print(sum(tree))
    print(advSum(tree))

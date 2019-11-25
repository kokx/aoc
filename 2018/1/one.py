from z3 import *
import sys

s = Solver()

num = 0

formula = []

freq = 0

yprev = Int('y_' + str(num))
s.add(yprev == 0)

inputs = []

for line in sys.stdin:
    num += 1
    xval = int(line)
    x = Int('x_' + str(num))
    y = Int('y_' + str(num))
    formula.append(x)
    s.add(x == xval)
    s.add(y == yprev + x)
    yprev = y

    inputs.append(xval)





s.check()

m = s.model()

seen = set()

num = 0
freq = 0

for i in range(0, 99999999999):
    inp = inputs[i % len(inputs)]
    print('-- %d, %d' % (inp, freq))
    freq += inp
    if freq in seen:
        print(freq)
        break
    seen.add(freq)


#for d in m.decls():
#    if d.name()[0] == 'y':
#        print(m[d])
#        if m[d].as_string() in seen:
#            print("%s -- %s" % (d.name(), m[d]))
#        else:
#            #print("%s = %s added" % (d.name(), m[d].as_string()))
#            seen.add(m[d].as_string())

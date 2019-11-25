num = 10551428

res = 0

for i in range(1, num+5):
    if num % i == 0:
        print('res = %d + %d' % (res, i))
        res += i

print(res)

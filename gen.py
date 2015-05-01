import random

n = input('')
a = [[0 for _ in range(n*2)] for _ in range(n*2)]

print n*2
for i in range(n*2):
    for j in range(i+1, n*2):
        if i == j:
            a[i][j] = 0
        else:
            a[i][j] = a[j][i] = random.randint(0,101)

for x in a:
    out = ''
    for y in x:
        out += '%i ' % y
    print out

print 'RB'*n

import random

opt = list(range(50))
random.shuffle(opt)

print 50

a = [[random.randint(74,100) for _ in range(50)] for _ in range(50)]

for x in range(50):
    a[x][x] = 0
    for y in range(x+1,50):
        a[x][y] = a[y][x]

for i in range(49):
    if i % 3 == 0: 
        a[opt[i]][opt[i+1]] = a[opt[i+1]][opt[i]] = random.randint(24, 29)
    elif i % 3 == 1:
        a[opt[i]][opt[i+1]] = a[opt[i+1]][opt[i]] = random.randint(17, 23)
    else:
        a[opt[i]][opt[i+1]] = a[opt[i+1]][opt[i]] = random.randint(30, 35)

i = 0
while i < 48:
    a[opt[i+2]][opt[i]] = a[opt[i]][opt[i+2]] = random.randint(10,16)
    i += 3


for x in a:
    out = ''
    for y in x:
        out += '%s ' % y
    print out

s = ['a' for _ in range(50)]
for i in range(25):
    s[opt[2*i]] = 'R'
    s[opt[1+2*i]] = 'B'

print ''.join(s)


out = ''
for x in opt:
    out += '%s ' %(x+1)
print out

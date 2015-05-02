import random

a = [[0 for _ in range(50)] for _ in range(50)]

lowest_path = [random.randint(30,45) for i in range(50)]
"""
def path(n):
    ret_path = [R]*25+[B]*25
    random.shuffle(ret_path)
    while(not_valid(ret_path)):
        random.shuffle(ret_path)
    return ret_path

def not_valid(path):
    r = 0
    b = 0
    temp =''
    for i in path:
        if(i == 'R'):
            r += 1
            b = 0
            if r >= 3:
                return False
        else:
            r = 0
            b += 1
            if b >= 3:
                return False
    return True
"""
#valid_path = path(1)
for i in range(50):
    for j in range(i+1,50):
        if i == j:
            a[i][j] = 0
        else:
            a[i][j] = a[j][i] = random.randint(23,100)

for i in range(50):
    j = (i+1)%50
    a[i][j] = a[j][i] = lowest_path[i]

print 50

for x in a:
    out = ''
    for y in x:
        out += '%i ' % y
    print out

print 'RB'*25
#print ''.join(valid_path)

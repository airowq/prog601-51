from itertools import product
k=0
for x in product('ABCDXYZ', repeat=4):
    a = x.count('X') + x.count('Y') + x.count('Z')
    if (x[0] == 'X' or x[0] == 'Y' or x[0] == 'Z') and a == 1: k+=1
print(k)
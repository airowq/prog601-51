a, k = 9**8 + 3**5 - 9, 0
while a >= 1:
    if a%3 == 2: k+=1
    a //= 3
print(k)
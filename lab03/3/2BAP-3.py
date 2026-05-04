s = []
def f(x):
    for i in range(2, int(x**0.5)+1):
        if x%i ==0: return False
    return True
for p in range(1, 85, 2):
    if f(p): s.append(p)
for p in s:
    for k in range(0, 26):
        a = (2**k) * (p**4)
        if a>45_000_000 and a<50_000_000: print(a)
                
def f(s):
    if s == 1: return 1
    ap = f(s-1)
    return 0.5*(1**0.5 + 0.5*(ap**0.5))
print(f(2))
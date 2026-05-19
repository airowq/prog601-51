a = [1, [2, [3, 4, [5]]]]
# рекурсия
def f(s):
    k = 0
    for i in s: 
        if type(i) is int: k += i
        else: k += f(i)
    return k
print(f(a))
# без рекурсии
def f(s):
    k = 0
    lst = [s]
    while lst:
        с = lst.pop()
        for i in с:
            if isinstance(i, list): lst.append(i)
            else: k += i
    return k
print(f(a))
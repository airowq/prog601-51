"""Модуль на основе ЛР №4: сумма вложенных списков и рекурсивная последовательность"""

import math

# ========== Задача 1: Сумма вложенных списков ==========

def sum_nested_recursive(lst):
    """Рекурсивная версия суммы элементов вложенных списков"""
    total = 0
    for item in lst:
        if isinstance(item, list):
            total += sum_nested_recursive(item)
        elif isinstance(item, (int, float)):
            total += item
    return total

def sum_nested_iterative(lst):
    """Итеративная версия (стек) суммы элементов вложенных списков"""
    stack = list(lst)
    total = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        elif isinstance(item, (int, float)):
            total += item
    return total

# ========== Задача 2: Рекурсивная последовательность ==========

def sequence_recursive(k):
    """
    Рекурсивное вычисление последовательности:
    a1 = 1, b1 = 1
    a_k = 0.5 * (sqrt(b_(k-1)) + 0.5 * sqrt(a_(k-1)))
    Возвращает (a_k, b_(k-1))
    """
    if k == 1:
        return 1.0, 1.0
    a_prev, b_prev = sequence_recursive(k - 1)
    a_k = 0.5 * (math.sqrt(b_prev) + 0.5 * math.sqrt(a_prev))
    return a_k, b_prev

def sequence_iterative(k):
    """Итеративная версия (возвращает только a_k)"""
    if k == 1:
        return 1.0
    a = 1.0
    b = 1.0
    for _ in range(2, k + 1):
        a_new = 0.5 * (math.sqrt(b) + 0.5 * math.sqrt(a))
        a, b = a_new, a
    return a
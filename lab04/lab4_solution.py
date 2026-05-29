# ============================================
# Лабораторная работа №4 (уровень Medium)
# Рекурсия + pytest тесты
# ============================================

# ---------- ФУНКЦИИ ----------
def rec_fib(n):
    """Рекурсивное вычисление числа Фибоначчи"""
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return rec_fib(n-1) + rec_fib(n-2)


def iter_fib(n):
    """Итеративное вычисление числа Фибоначчи"""
    if n <= 0:
        return 0
    if n == 1 or n == 2:
        return 1
    a, b = 1, 1
    for i in range(3, n + 1):
        a, b = b, a + b
    return b


# ---------- ТЕСТЫ (без pytest, на случай если не установлен) ----------
def test_rec_fib():
    print("Тестируем rec_fib...")
    assert rec_fib(1) == 1, "rec_fib(1) должно быть 1"
    assert rec_fib(2) == 1, "rec_fib(2) должно быть 1"
    assert rec_fib(3) == 2, "rec_fib(3) должно быть 2"
    assert rec_fib(5) == 5, "rec_fib(5) должно быть 5"
    assert rec_fib(10) == 55, "rec_fib(10) должно быть 55"
    print("  rec_fib: OK")


def test_iter_fib():
    print("Тестируем iter_fib...")
    assert iter_fib(1) == 1, "iter_fib(1) должно быть 1"
    assert iter_fib(2) == 1, "iter_fib(2) должно быть 1"
    assert iter_fib(3) == 2, "iter_fib(3) должно быть 2"
    assert iter_fib(5) == 5, "iter_fib(5) должно быть 5"
    assert iter_fib(10) == 55, "iter_fib(10) должно быть 55"
    print("  iter_fib: OK")


def test_both_match():
    print("Тестируем, что функции совпадают...")
    for n in range(1, 15):
        assert rec_fib(n) == iter_fib(n), f"Ошибка при n={n}"
    print("  Функции совпадают: OK")


def run_all_tests():
    print("\n" + "="*50)
    print("ЗАПУСК ТЕСТОВ")
    print("="*50)
    test_rec_fib()
    test_iter_fib()
    test_both_match()
    print("\n" + "="*50)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("="*50)


# ---------- ОСНОВНАЯ ПРОГРАММА ----------
def main():
    print("\n" + "="*50)
    print("ВЫЧИСЛЕНИЕ ЧИСЕЛ ФИБОНАЧЧИ")
    print("="*50)
    
    for n in [1, 2, 5, 10, 15, 20]:
        r = rec_fib(n)
        i = iter_fib(n)
        print(f"fib({n:2d}) = {r:8d} (рекурсия) | {i:8d} (итерация)")


# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    main()
    run_all_tests()
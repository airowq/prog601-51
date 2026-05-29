"""
Найти числа из [45_000_000; 50_000_000], у которых ровно 5 различных нечётных делителей.
Число имеет вид 2^k * p^4, где p — нечётное простое.
"""

import math

def is_prime(n: int) -> bool:
    """
    Проверка числа на простоту.
    
    Примеры:
    >>> is_prime(2)
    True
    >>> is_prime(3)
    True
    >>> is_prime(4)
    False
    >>> is_prime(5)
    True
    >>> is_prime(9)
    False
    >>> is_prime(17)
    True
    >>> is_prime(1)
    False
    >>> is_prime(0)
    False
    >>> is_prime(97)
    True
    >>> is_prime(100)
    False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_odd_divisors(n: int) -> int:
    """
    Подсчет количества нечетных делителей числа.
    
    Примеры:
    >>> count_odd_divisors(1)
    1
    >>> count_odd_divisors(2)
    1
    >>> count_odd_divisors(3)
    2
    >>> count_odd_divisors(9)
    3
    >>> count_odd_divisors(15)
    4
    >>> count_odd_divisors(45)
    6
    >>> count_odd_divisors(81)
    5
    """
    # Убираем все степени двойки
    while n % 2 == 0:
        n //= 2
    
    # Считаем делители нечетной части
    count = 0
    for d in range(1, int(math.sqrt(n)) + 1):
        if n % d == 0:
            count += 1
            if d != n // d:
                count += 1
    return count

def find_numbers_with_5_odd_divisors(low: int, high: int) -> list:
    """
    Поиск чисел с 5 нечетными делителями в заданном диапазоне.
    Числа имеют вид 2^k * p^4, где p - нечетное простое.
    
    Примеры:
    >>> find_numbers_with_5_odd_divisors(1, 100)
    []
    >>> len(find_numbers_with_5_odd_divisors(45000000, 50000000))
    4
    >>> find_numbers_with_5_odd_divisors(81, 81)
    [81]
    """
    result = []
    max_p = int(round(high ** 0.25)) + 2
    
    for p in range(3, max_p + 1, 2):
        if not is_prime(p):
            continue
        
        p4 = p ** 4
        if p4 > high:
            break
        
        k = 0
        while True:
            num = (2 ** k) * p4
            if num > high:
                break
            if num >= low:
                result.append(num)
            k += 1
    
    result.sort()
    return result

def solve_task3():
    """
    Основная функция решения задачи 3.
    
    Пример:
    >>> solve_task3()
    Найдено чисел: 4
    """
    LOW = 45_000_000
    HIGH = 50_000_000
    result = find_numbers_with_5_odd_divisors(LOW, HIGH)
    
    print(f"Найдено чисел: {len(result)}")
    print("Числа в порядке возрастания:")
    for num in result:
        odd_div_count = count_odd_divisors(num)
        print(f"{num} (нечетных делителей: {odd_div_count})")
    
    # Проверка для первого числа
    if result:
        print("\nПроверка первого числа:")
        test_num = result[0]
        # Находим нечётную часть
        odd_part = test_num
        while odd_part % 2 == 0:
            odd_part //= 2
        print(f"Число: {test_num}")
        print(f"Нечётная часть: {odd_part}")
        # Находим делители нечётной части
        divisors = [d for d in range(1, odd_part + 1) if odd_part % d == 0]
        odd_divisors = [d for d in divisors if d % 2 == 1]
        print(f"Нечётные делители: {odd_divisors}")
        print(f"Их количество: {len(odd_divisors)}")

if __name__ == "__main__":
    import doctest
    print("="*50)
    print("ЗАПУСК ДОКТЕСТОВ ДЛЯ ЗАДАЧИ 3")
    print("="*50)
    doctest.testmod(verbose=True)
    print("\n" + "="*50)
    print("ВЫПОЛНЕНИЕ ПРОГРАММЫ")
    print("="*50)
    solve_task3()
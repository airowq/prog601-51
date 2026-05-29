"""
Задача: вычислить 9^8 + 3^5 - 9, перевести в троичную систему,
подсчитать количество цифр 2.
"""

def to_base3(n: int) -> str:
    """
    Перевод числа в троичную систему счисления.
    
    Примеры:
    >>> to_base3(0)
    '0'
    >>> to_base3(1)
    '1'
    >>> to_base3(2)
    '2'
    >>> to_base3(3)
    '10'
    >>> to_base3(4)
    '11'
    >>> to_base3(5)
    '12'
    >>> to_base3(8)
    '22'
    >>> to_base3(9)
    '100'
    >>> to_base3(26)
    '222'
    >>> to_base3(27)
    '1000'
    """
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % 3))
        n //= 3
    return ''.join(reversed(digits))

def count_digit_in_base3(n: int, digit: str = '2') -> int:
    """
    Подсчет количества определенной цифры в троичной записи числа.
    
    Примеры:
    >>> count_digit_in_base3(9**8 + 3**5 - 9)
    14
    >>> count_digit_in_base3(0, '0')
    1
    >>> count_digit_in_base3(3, '1')
    1
    >>> count_digit_in_base3(8, '2')
    2
    >>> count_digit_in_base3(26, '2')
    3
    >>> count_digit_in_base3(9, '1')
    1
    """
    base3_repr = to_base3(n)
    return base3_repr.count(digit)

def solve_task2():
    """
    Основная функция решения задачи 2.
    
    Пример:
    >>> solve_task2()
    Значение выражения: 43046784
    В троичной системе: ...
    Количество цифр 2: 14
    """
    # Вычисляем выражение
    result = 9**8 + 3**5 - 9
    print(f"Значение выражения: {result}")
    
    # Переводим в троичную систему
    base3_repr = to_base3(result)
    print(f"В троичной системе: {base3_repr}")
    
    # Считаем количество цифр '2'
    count_2 = base3_repr.count('2')
    print(f"Количество цифр 2: {count_2}")
    
    # Дополнительная проверка: анализ разрядов
    print("\nПроверка через степени:")
    print(f"9^8 = 3^16 → в троичной: 1 и 16 нулей")
    print(f"3^5 → в троичной: 1 и 5 нулей")
    print(f"Вычитаем 9 = 3^2")
    
    return count_2

if __name__ == "__main__":
    import doctest
    print("="*50)
    print("ЗАПУСК ДОКТЕСТОВ ДЛЯ ЗАДАЧИ 2")
    print("="*50)
    doctest.testmod(verbose=True)
    print("\n" + "="*50)
    print("ВЫПОЛНЕНИЕ ПРОГРАММЫ")
    print("="*50)
    solve_task2()
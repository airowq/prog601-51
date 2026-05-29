"""
Задача: сколько 4-буквенных слов из букв A,B,C,D,X,Y,Z,
если первая буква X,Y,Z, а далее X,Y,Z не встречаются.
"""

def solve_task1():
    """
    Решение задачи о количестве кодовых слов.
    
    Примеры:
    >>> solve_task1()
    Аналитически: 3 × 4^3 = 192
    Перебором: 192
    Ответ: 192 различных кодовых слов
    """
    # Аналитическое решение
    first_letter_options = 3  # X, Y, Z
    other_letter_options = 4  # A, B, C, D
    positions_after_first = 3  # 2-я, 3-я, 4-я позиции
    
    total = first_letter_options * (other_letter_options ** positions_after_first)
    print(f"Аналитически: {first_letter_options} × {other_letter_options}^{positions_after_first} = {total}")
    
    # Проверка перебором (для демонстрации)
    alphabet = ['A', 'B', 'C', 'D', 'X', 'Y', 'Z']
    first_letters = ['X', 'Y', 'Z']
    rest_letters = ['A', 'B', 'C', 'D']
    
    count = 0
    for first in first_letters:
        for second in rest_letters:
            for third in rest_letters:
                for fourth in rest_letters:
                    count += 1
    
    print(f"Перебором: {count}")
    print(f"Ответ: {count} различных кодовых слов")

def count_words_analytical(first_count: int, rest_count: int, positions: int) -> int:
    """
    Аналитический подсчет количества слов.
    
    Примеры:
    >>> count_words_analytical(3, 4, 3)
    192
    >>> count_words_analytical(2, 3, 2)
    18
    >>> count_words_analytical(1, 10, 1)
    10
    >>> count_words_analytical(5, 2, 4)
    80
    """
    return first_count * (rest_count ** positions)

def count_words_bruteforce(first_letters: list, rest_letters: list, length: int) -> int:
    """
    Подсчет слов методом перебора.
    
    Примеры:
    >>> count_words_bruteforce(['X','Y','Z'], ['A','B','C','D'], 4)
    192
    >>> count_words_bruteforce(['A'], ['B'], 2)
    1
    >>> count_words_bruteforce(['X','Y'], ['A'], 3)
    2
    """
    def generate(pos, current, first, rest, word_len):
        if pos == 0:
            for letter in first:
                generate(1, current + letter, first, rest, word_len)
        elif pos < word_len:
            for letter in rest:
                generate(pos + 1, current + letter, first, rest, word_len)
        else:
            nonlocal cnt
            cnt += 1
    
    cnt = 0
    generate(0, "", first_letters, rest_letters, length)
    return cnt

if __name__ == "__main__":
    import doctest
    print("="*50)
    print("ЗАПУСК ДОКТЕСТОВ ДЛЯ ЗАДАЧИ 1")
    print("="*50)
    doctest.testmod(verbose=True)
    print("\n" + "="*50)
    print("ВЫПОЛНЕНИЕ ПРОГРАММЫ")
    print("="*50)
    solve_task1()
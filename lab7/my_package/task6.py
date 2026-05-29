"""Модуль на основе ЛР №6: генератор для чтения файла с ограничением длины"""

from functools import wraps
import time

# ========== Декоратор (вынесен отдельно для использования) ==========

def timer_decorator(func):
    """Декоратор, выводящий время выполнения функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"[ДЕКОРАТОР] Время выполнения: {end - start:.4f} сек.")
        return result
    return wrapper

# ========== Замыкание для построчного чтения файла ==========

def file_reader(filename, max_length, encoding='utf-8'):
    """
    Создаёт замыкание для чтения файла с ограничением длины строки.
    
    Args:
        filename: путь к файлу
        max_length: максимальная длина строки (количество символов)
        encoding: кодировка файла (по умолчанию utf-8)
    
    Returns:
        функцию, которая при каждом вызове возвращает следующую часть текста,
        или None при ошибке/окончании файла
    """
    if max_length <= 0:
        raise ValueError("Максимальная длина строки должна быть положительным числом")
    
    # Пытаемся открыть файл
    try:
        file = open(filename, 'r', encoding=encoding)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
        return None
    except PermissionError:
        print(f"Ошибка: Нет прав для чтения файла '{filename}'")
        return None
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        try:
            file = open(filename, 'r', encoding='cp1251')
            print(f"[ПРЕДУПРЕЖДЕНИЕ] Использована кодировка cp1251 вместо {encoding}")
        except Exception as e:
            print(f"Ошибка: Не удалось прочитать файл - {e}")
            return None
    
    # Переменные замыкания
    remainder = ""           # остаток от предыдущей длинной строки
    is_exhausted = False     # флаг окончания файла
    
    def read_next():
        nonlocal remainder, is_exhausted
        
        # Если файл уже закончился и нет остатка
        if is_exhausted and not remainder:
            return None
        
        # Если есть остаток от предыдущей длинной строки
        if remainder:
            if len(remainder) <= max_length:
                result = remainder
                remainder = ""
                return result
            else:
                result = remainder[:max_length]
                remainder = remainder[max_length:]
                return result
        
        # Читаем следующую строку из файла
        line = file.readline()
        
        # Если файл закончился
        if not line:
            is_exhausted = True
            file.close()
            return None
        
        # Удаляем символ перевода строки
        line = line.rstrip('\n\r')
        
        # Если строка целиком помещается в лимит
        if len(line) <= max_length:
            return line
        
        # Если строка длиннее лимита - разбиваем
        result = line[:max_length]
        remainder = line[max_length:]
        return result
    
    return read_next

def read_all_blocks(reader_func):
    """Вспомогательная функция: прочитать все блоки из reader'а"""
    blocks = []
    while True:
        block = reader_func()
        if block is None:
            break
        blocks.append(block)
    return blocks
import os
import time
from functools import wraps

# Декоратор для логирования работы генератора
def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[ЛОГ] Запуск генератора: {func.__name__}")
        print(f"[ЛОГ] Аргументы: {args}, {kwargs}")
        
        # Замер времени выполнения
        start_time = time.time()
        
        # Получаем генератор
        gen = func(*args, **kwargs)
        
        # Счётчик выданных фрагментов
        fragment_count = 0
        
        try:
            while True:
                value = next(gen)
                fragment_count += 1
                print(f"[ЛОГ] Выдан фрагмент #{fragment_count}, длина: {len(value)} симв.")
                yield value
        except StopIteration:
            end_time = time.time()
            print(f"[ЛОГ] Генератор завершил работу. Всего фрагментов: {fragment_count}")
            print(f"[ЛОГ] Общее время выполнения: {end_time - start_time:.4f} сек.")
            return
    
    return wrapper


@logger_decorator
def chunked_file_reader(filepath, chunk_size=50, file_encoding='utf-8'):
    """
    Генератор для чтения файла с разбиением длинных строк на части.
    
    Аргументы:
        filepath: путь к файлу
        chunk_size: максимальный размер фрагмента (по умолчанию 50 символов)
        file_encoding: кодировка файла
    
    Возвращает:
        Генератор, выдающий фрагменты строк заданного размера
    """
    # Проверка существования файла
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    # Проверка корректности размера фрагмента
    if chunk_size <= 0:
        raise ValueError(f"Размер фрагмента должен быть положительным, получено: {chunk_size}")
    
    try:
        with open(filepath, 'r', encoding=file_encoding) as file:
            line_number = 0
            
            for line in file:
                line_number += 1
                # Удаляем символ переноса строки
                original_line = line.rstrip('\n\r')
                line_length = len(original_line)
                
                if line_length <= chunk_size:
                    # Короткая строка - выдаём целиком
                    yield f"[{line_number}] {original_line}"
                else:
                    # Длинная строка - разбиваем на части
                    num_parts = (line_length + chunk_size - 1) // chunk_size
                    for part_idx in range(num_parts):
                        start = part_idx * chunk_size
                        end = start + chunk_size
                        part = original_line[start:end]
                        yield f"[{line_number}:{part_idx + 1}/{num_parts}] {part}"
                        
    except PermissionError:
        raise PermissionError(f"Нет прав доступа к файлу: {filepath}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Ошибка декодирования файла (кодировка {file_encoding}): {e}")
    except OSError as e:
        raise OSError(f"Ошибка ввода-вывода при работе с файлом {filepath}: {e}")


# Альтернативная версия генератора с буферизацией
def buffered_line_reader(filepath, max_line_length=30, encoding='utf-8'):
    """
    Альтернативная реализация генератора с накоплением остатка от предыдущей строки.
    """
    if not os.path.isfile(filepath):
        raise Exception(f"Файл отсутствует: {filepath}")
    
    remainder = ""  # Остаток от предыдущей строки
    
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            for raw_line in f:
                # Объединяем остаток с текущей строкой
                full_line = remainder + raw_line.rstrip('\n\r')
                remainder = ""
                
                # Разбиваем строку на фрагменты
                while len(full_line) > max_line_length:
                    fragment = full_line[:max_line_length]
                    yield fragment
                    full_line = full_line[max_line_length:]
                
                # Сохраняем остаток для следующей строки
                remainder = full_line
            
            # Выдаём последний остаток, если есть
            if remainder:
                yield remainder
                
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл '{filepath}' не существует")
        raise
    except PermissionError:
        print(f"[ОШИБКА] Отказано в доступе к файлу '{filepath}'")
        raise


# Функция для демонстрации работы
def demonstrate_generators():
    # Создаём тестовый файл
    test_filename = "test_data.txt"
    
    test_content = """Это короткая строка.
А это очень-очень-очень-очень-очень-очень-очень-очень-очень-очень длинная строка, которая должна быть разбита на несколько фрагментов.
Третья строка средней длины.
Еще одна короткая строка.
И самая последняя строка в файле с некоторым текстом для проверки."""
    
    with open(test_filename, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ГЕНЕРАТОРА (основная версия)")
    print("=" * 60)
    
    try:
        reader = chunked_file_reader(test_filename, chunk_size=40)
        for fragment in reader:
            print(fragment)
    except Exception as e:
        print(f"Ошибка: {e}")
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ГЕНЕРАТОРА (альтернативная версия)")
    print("=" * 60)
    
    try:
        alt_reader = buffered_line_reader(test_filename, max_line_length=30)
        for idx, fragment in enumerate(alt_reader, 1):
            print(f"[Фрагмент {idx}] {fragment}")
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Проверка обработки ошибок
    print("\n" + "=" * 60)
    print("ПРОВЕРКА ОБРАБОТКИ ОШИБОК")
    print("=" * 60)
    
    try:
        # Попытка прочитать несуществующий файл
        bad_reader = chunked_file_reader("nonexistent_file.txt", chunk_size=20)
        next(bad_reader)
    except FileNotFoundError as e:
        print(f"Корректно обработана ошибка: {e}")
    
    try:
        # Попытка с некорректным размером фрагмента
        bad_reader2 = chunked_file_reader(test_filename, chunk_size=0)
        next(bad_reader2)
    except ValueError as e:
        print(f"Корректно обработана ошибка: {e}")
    
    # Удаляем тестовый файл
    os.remove(test_filename)


if __name__ == "__main__":
    demonstrate_generators()
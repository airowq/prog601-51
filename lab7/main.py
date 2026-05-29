#!/usr/bin/env python3
"""CLI для лабораторной работы №7 - Пакеты и модули"""

import typer
import os
from typing import Optional
from pathlib import Path

from my_package import task4 as t4
from my_package import task5 as t5
from my_package import task6 as t6

app = typer.Typer(help="Лабораторная работа №7: Пакеты и модули", no_args_is_help=True)

#ЗАДАЧА 4 

@app.command()
def sum_nested(lst: str, method: str = "recursive"):
    """
    Вычисление суммы элементов вложенного списка.
    
    lst: строка вида "[1, [2, 3], 4]" или просто "1 2 3"
    method: "recursive" или "iterative"
    """
    # Парсинг входных данных
    try:
        if lst.startswith('['):
            # Парсим JSON-подобный список
            import ast
            parsed_list = ast.literal_eval(lst)
        else:
            # Простой список чисел через пробел
            parsed_list = [int(x) if x.lstrip('-').isdigit() else float(x) 
                          for x in lst.split()]
    except Exception as e:
        typer.echo(f"Ошибка парсинга списка: {e}")
        raise typer.Exit(code=1)
    
    if method == "recursive":
        result = t4.sum_nested_recursive(parsed_list)
        typer.echo(f"Сумма (рекурсивно): {result}")
    elif method == "iterative":
        result = t4.sum_nested_iterative(parsed_list)
        typer.echo(f"Сумма (итеративно): {result}")
    else:
        typer.echo("method должен быть 'recursive' или 'iterative'")
        raise typer.Exit(code=1)

@app.command()
def sequence(k: int, method: str = "recursive"):
    """
    Вычисление a_k по рекуррентной формуле.
    
    k: номер элемента последовательности (>=1)
    method: "recursive" или "iterative"
    """
    if k < 1:
        typer.echo("k должно быть >= 1")
        raise typer.Exit(code=1)
    
    if method == "recursive":
        a_k, b_prev = t4.sequence_recursive(k)
        typer.echo(f"a_{k} = {a_k}, b_{k-1} = {b_prev}")
    elif method == "iterative":
        result = t4.sequence_iterative(k)
        typer.echo(f"a_{k} = {result}")
    else:
        typer.echo("method должен быть 'recursive' или 'iterative'")
        raise typer.Exit(code=1)

#ЗАДАЧА 5 

@app.command()
def dog_fact():
    """Получить случайный факт о собаках (через API)"""
    requester = t5.api_requester("https://dogapi.dog/api/v2/facts")
    fact = requester()
    typer.echo(f"Факт о собаках: {fact}")

@app.command()
def cat_fact():
    """Получить случайный факт о кошках (через API)"""
    requester = t5.api_requester("https://catfact.ninja/fact")
    fact = requester()
    typer.echo(f"Факт о кошках: {fact}")

@app.command()
def api_fact(api_name: str = "dog"):
    """Получить факт из указанного API (dog или cat) с декоратором"""
    result = t5.get_fact_from_api(api_name)
    typer.echo(result)

#ЗАДАЧА 6

@app.command()
def read_file(
    filename: str = typer.Argument(..., help="Путь к файлу"),
    max_length: int = typer.Option(30, "--max-length", "-l", help="Максимальная длина строки"),
    encoding: str = typer.Option("utf-8", "--encoding", "-e", help="Кодировка файла"),
    show_timing: bool = typer.Option(False, "--timing", "-t", help="Показать время выполнения")
):
    """
    Чтение файла с разбиением длинных строк на части.
    Использует замыкание file_reader.
    """
    if not os.path.exists(filename):
        typer.echo(f"Ошибка: Файл '{filename}' не найден")
        raise typer.Exit(code=1)
    
    def read_without_timing():
        reader = t6.file_reader(filename, max_length, encoding)
        if reader is None:
            typer.echo("Не удалось создать читатель файла")
            return None
        return t6.read_all_blocks(reader)
    
    if show_timing:
        @t6.timer_decorator
        def read_with_timing():
            return read_without_timing()
        blocks = read_with_timing()
    else:
        blocks = read_without_timing()
    
    if blocks is None:
        raise typer.Exit(code=1)
    
    typer.echo(f"\nРезультат чтения файла '{filename}' (лимит: {max_length} символов):")
    typer.echo("-" * 50)
    for i, block in enumerate(blocks, 1):
        typer.echo(f"Блок {i}: \"{block}\" (длина: {len(block)})")
    typer.echo("-" * 50)
    typer.echo(f"Всего блоков: {len(blocks)}")

@app.command()
def create_test_file(
    filename: str = typer.Argument("test_file.txt"),
    content: Optional[str] = typer.Option(None, "--content", "-c", help="Содержимое файла")
):
    """Создать тестовый файл для демонстрации"""
    if content is None:
        content = """Это короткая строка.
А это очень-очень-очень-очень-очень-очень-очень-очень-очень-очень длинная строка, которая явно превышает лимит в 30 символов.
Третья строка с нормальной длиной.
Последняя строка файла."""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    typer.echo(f"Тестовый файл '{filename}' создан")
    typer.echo(f"Содержимое:\n{content}")

if __name__ == "__main__":
    app()
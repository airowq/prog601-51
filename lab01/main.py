#!/usr/bin/env python3
# main.py - Верхнеуровневый модуль для управления заданиями (уровень Medium)

import sys
import os
import importlib

# Добавляем путь к папке tasks для корректного импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tasks'))

# Список всех заданий в правильном порядке
TASK_MODULES = [
    '00_distance',
    '01_circle',
    '02_operations',
    '03_favorite_movies',
    '04_my_family',
    '05_zoo',
    '06_songs_list',
    '07_secret',
    '08_garden',
    '09_shopping',
    '10_store'
]

def load_task(module_name):
    """Динамическая загрузка модуля задания"""
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        print(f"Ошибка импорта {module_name}: {e}")
        return None
    except Exception as e:
        print(f"Неизвестная ошибка в {module_name}: {e}")
        return None

def show_menu():
    """Отображение меню"""
    print("\n" + "="*50)
    print("ВЕРХНЕУРОВНЕВЫЙ МОДУЛЬ УПРАВЛЕНИЯ ЗАДАНИЯМИ")
    print("="*50)
    
    for i, module_name in enumerate(TASK_MODULES, 1):
        task_name = module_name.replace('_', ' ').title()
        print(f"  {i}. {task_name}")
    
    print("\nСПЕЦИАЛЬНЫЕ КОМАНДЫ:")
    print("  all - Выполнить все задания")
    print("  0   - Выйти")
    print("="*50)

def run_single_task(task_num):
    """Запуск одного задания по номеру"""
    if 1 <= task_num <= len(TASK_MODULES):
        module_name = TASK_MODULES[task_num-1]
        print(f"\nВыполнение задания {task_num}: {module_name}")
        print("-"*40)
        
        module = load_task(module_name)
        if module:
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            else:
                print("В модуле нет функции run() или main()")
        else:
            print(f"Не удалось загрузить задание {task_num}")
        
        print("-"*40)
    else:
        print(f"Неверный номер. Введите число от 1 до {len(TASK_MODULES)}")

def run_all_tasks():
    """Запуск всех заданий последовательно"""
    print("\n" + "="*50)
    print("ЗАПУСК ВСЕХ ЗАДАНИЙ")
    print("="*50)
    
    for i, module_name in enumerate(TASK_MODULES, 1):
        print(f"\n--- Задание {i}: {module_name} ---")
        
        module = load_task(module_name)
        if module:
            if hasattr(module, 'run'):
                module.run()
            elif hasattr(module, 'main'):
                module.main()
            else:
                print("В модуле нет функции run() или main()")
        else:
            print(f"Ошибка загрузки задания {i}")
        
        if i < len(TASK_MODULES):
            input("\nНажмите Enter для продолжения...")
    
    print("\n" + "="*50)
    print("ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ")
    print("="*50)

def clear_screen():
    """Очистка экрана"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Главная функция"""
    print("\nЗагружено заданий:", len(TASK_MODULES))
    print("Путь к заданиям: lab1/tasks/")
    
    while True:
        try:
            show_menu()
            choice = input("\nВаш выбор: ").strip().lower()
            
            if choice == '0':
                print("\nДо свидания!")
                break
            elif choice == 'all':
                run_all_tasks()
            elif choice == 'clear':
                clear_screen()
            elif choice.isdigit():
                run_single_task(int(choice))
            else:
                print("Неверный ввод. Используйте: число, 'all' или '0'")
                
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
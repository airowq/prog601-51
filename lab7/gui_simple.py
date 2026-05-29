"""
GUI приложение для лабораторной работы №7 (автономная версия)
Не требует импорта пакета - все функции внутри
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

# ФУНКЦИИ ИЗ ЛАБОРАТОРНЫХ РАБОТ

# Лаба 4: Рекурсия
def sum_nested_recursive(lst):
    total = 0
    for item in lst:
        if isinstance(item, list):
            total += sum_nested_recursive(item)
        else:
            total += item
    return total

def sum_nested_iterative(lst):
    stack = list(lst)
    total = 0
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(item)
        else:
            total += item
    return total

# Лаба 5: Замыкания
def make_adder(x):
    def adder(y):
        return x + y
    return adder

# Лаба 6: Генераторы
def fibonacci_generator(limit=10):
    a, b = 0, 1
    for _ in range(limit):
        yield a
        a, b = b, a + b

def fact_generator(facts_list):
    while True:
        yield random.choice(facts_list)


# GUI ПРИЛОЖЕНИЕ

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа №7 - Пакеты и модули")
        self.root.geometry("800x600")

        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка 1
        self.create_tab1(notebook)
        # Вкладка 2
        self.create_tab2(notebook)
        # Вкладка 3
        self.create_tab3(notebook)

    def create_tab1(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="1. Рекурсия (лаб4)")

        ttk.Label(tab, text="Введите вложенный список:").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(tab, height=6, width=80)
        self.input_text.insert(tk.END, "[1, [2, 3], [4, [5, 6]], 7, 8]")
        self.input_text.pack(pady=5)

        self.method = tk.StringVar(value="recursive")
        frame = ttk.Frame(tab)
        frame.pack(pady=5)
        ttk.Radiobutton(frame, text="Рекурсивно", variable=self.method, value="recursive").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(frame, text="Итеративно", variable=self.method, value="iterative").pack(side=tk.LEFT, padx=10)

        ttk.Button(tab, text="Вычислить сумму", command=self.calc_sum).pack(pady=10)

        ttk.Label(tab, text="Результат:").pack()
        self.output = tk.Text(tab, height=5, width=80, state=tk.DISABLED)
        self.output.pack(pady=5)

    def create_tab2(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="2. Замыкания (лаб5)")

        frame = ttk.Frame(tab)
        frame.pack(pady=30)

        ttk.Label(frame, text="x = ").grid(row=0, column=0, padx=5, pady=10)
        self.x_entry = tk.Entry(frame, width=15)
        self.x_entry.insert(0, "10")
        self.x_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="y = ").grid(row=1, column=0, padx=5, pady=10)
        self.y_entry = tk.Entry(frame, width=15)
        self.y_entry.insert(0, "5")
        self.y_entry.grid(row=1, column=1, padx=5)

        ttk.Button(frame, text="Вычислить x + y", command=self.calc_closure).grid(row=2, column=0, columnspan=2, pady=20)

        self.closure_out = tk.Text(tab, height=3, width=50, state=tk.DISABLED)
        self.closure_out.pack(pady=20)

    def create_tab3(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="3. Генераторы (лаб6)")

        # Фибоначчи
        fib_frame = ttk.LabelFrame(tab, text="Генератор Фибоначчи")
        fib_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(fib_frame, text="Количество чисел:").pack(side=tk.LEFT, padx=5)
        self.fib_limit = tk.Entry(fib_frame, width=10)
        self.fib_limit.insert(0, "15")
        self.fib_limit.pack(side=tk.LEFT, padx=5)

        ttk.Button(fib_frame, text="Сгенерировать", command=self.gen_fib).pack(side=tk.LEFT, padx=10)

        self.fib_out = tk.Text(fib_frame, height=5, width=70, state=tk.DISABLED)
        self.fib_out.pack(pady=10, padx=10)

        # Факты
        facts_frame = ttk.LabelFrame(tab, text="Генератор случайных фактов")
        facts_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(facts_frame, text="Список фактов (каждый с новой строки):").pack()
        self.facts_input = scrolledtext.ScrolledText(facts_frame, height=4, width=70)
        default = "Собаки видят сны\nНос собаки уникален\nСобаки понимают до 250 слов\nСобаки чувствуют магнитное поле"
        self.facts_input.insert(tk.END, default)
        self.facts_input.pack(pady=5)

        ttk.Button(facts_frame, text="Получить случайный факт", command=self.gen_fact).pack(pady=5)

        self.fact_out = tk.Text(facts_frame, height=3, width=70, state=tk.DISABLED)
        self.fact_out.pack(pady=10)

    def calc_sum(self):
        try:
            text = self.input_text.get("1.0", tk.END).strip()
            lst = eval(text)

            if self.method.get() == "recursive":
                result = sum_nested_recursive(lst)
                method = "рекурсивно"
            else:
                result = sum_nested_iterative(lst)
                method = "итеративно"

            self.output.config(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Список: {lst}\n\nСумма ({method}): {result}")
            self.output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный формат списка: {e}")

    def calc_closure(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            adder = make_adder(x)
            result = adder(y)

            self.closure_out.config(state=tk.NORMAL)
            self.closure_out.delete("1.0", tk.END)
            self.closure_out.insert(tk.END, f"make_adder({x})({y}) = {x} + {y} = {result}")
            self.closure_out.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа")

    def gen_fib(self):
        try:
            limit = int(self.fib_limit.get())
            if limit > 50:
                if not messagebox.askyesno("Предупреждение", f"Сгенерировать {limit} чисел?"):
                    return
            fib_list = list(fibonacci_generator(limit))

            self.fib_out.config(state=tk.NORMAL)
            self.fib_out.delete("1.0", tk.END)
            self.fib_out.insert(tk.END, ", ".join(map(str, fib_list)))
            self.fib_out.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")

    def gen_fact(self):
        try:
            text = self.facts_input.get("1.0", tk.END).strip()
            facts = [f.strip() for f in text.split('\n') if f.strip()]
            if not facts:
                messagebox.showerror("Ошибка", "Введите хотя бы один факт")
                return
            gen = fact_generator(facts)
            fact = next(gen)

            self.fact_out.config(state=tk.NORMAL)
            self.fact_out.delete("1.0", tk.END)
            self.fact_out.insert(tk.END, fact)
            self.fact_out.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
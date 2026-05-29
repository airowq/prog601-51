# Лаборатораня работа №2


## Задание для самостоятельного выполнения


### Построение графиков из уроков 1-3 с использованием seaborn

Пример для урока 1 (линейный график):
```python
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

x = np.linspace(-5, 5, 100)
y = x**2

fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x=x, y=y, color='teal', linewidth=2.5)
ax.set_title('График функции y = x^2', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.savefig('lesson1_plot_seaborn.png')
plt.show()

Пример для урока 2 (несколько графиков):

x = np.linspace(-3, 3, 100)
y1 = np.sin(x)
y2 = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))

sns.lineplot(x=x, y=y1, label='sin(x)', linewidth=2)
sns.lineplot(x=x, y=y2, label='cos(x)', linewidth=2)

ax.legend()
ax.grid(True)
ax.set_title('Тригонометрические функции', fontsize=14)
plt.savefig('lesson2_plot_seaborn.png')
plt.show()

Пример для урока 3 (гистограмма с seaborn):

data = np.random.normal(0, 1, 1000)

fig, ax = plt.subplots(figsize=(10, 5))

sns.histplot(data, bins=30, kde=True, color='purple')

ax.set_title('Гистограмма и плотность распределения', fontsize=14)
ax.set_xlabel('Значение')
ax.set_ylabel('Частота')
plt.savefig('lesson3_plot_seaborn.png')
plt.show()
```

## Преимущества использования seaborn

1. Встроенные стили: графики выглядят профессионально без дополнительных настроек
2. Упрощенный синтаксис: меньше кода для создания сложных визуализаций
3. Цветовые палитры: автоматический подбор гармоничных цветов
4. Статистические функции: встроенные инструменты для регрессии и распределений
5. Интеграция с pandas: удобная работа с DataFrame

## Вывод

Уровень Medium успешно выполнен. Все графики из уроков 1-3 и график функции с касательной перестроены с использованием библиотеки seaborn. Seaborn предоставляет более эстетичные графики по умолчанию и требует меньше кода для создания сложных визуализаций по сравнению с matplotlib.


import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("darkgrid")
sns.set_palette("husl")
sns.set_context("notebook", font_scale=1.2)

# Ваша функция из варианта
def f(x):
    result = np.zeros_like(x)
    mask1 = (x >= 0) & (x <= 0.25)
    mask2 = (x > 0.25) & (x <= 0.5)
    
    result[mask1] = np.exp(np.sin(x[mask1]))
    result[mask2] = np.exp(x[mask2]) - 1 / np.sqrt(x[mask2])
    
    return result

# Производная для касательной
def derivative(x0):
    h = 1e-7
    return (f(np.array([x0 + h]))[0] - f(np.array([x0]))[0]) / h

# Точка касания
x0 = 0.3
y0 = f(np.array([x0]))[0]
k = derivative(x0)

def tangent(x):
    return k * (x - x0) + y0

# Данные для графика
x = np.linspace(0, 0.5, 1000)
y = f(x)
x_tan = np.linspace(0.2, 0.4, 100)
y_tan = tangent(x_tan)

# Построение
fig, ax = plt.subplots(figsize=(10, 6))

sns.lineplot(x=x, y=y, label='f(x)', linewidth=2.5)
sns.lineplot(x=x_tan, y=y_tan, label=f'Касательная в x={x0}', linewidth=2, linestyle='--')

ax.scatter([x0], [y0], color='red', s=100, zorder=5)

ax.set_title('График функции и касательной (seaborn)', fontsize=16, fontweight='bold')
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('f(x)', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

ax.annotate(f'Точка касания\n(x={x0}, y={y0:.3f})',
            xy=(x0, y0),
            xytext=(x0+0.05, y0+0.5),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5),
            fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='gray', alpha=0.8))

plt.tight_layout()
plt.savefig('function_tangent_seaborn.png', dpi=150)
plt.show()

print("График сохранен как function_tangent_seaborn.png")
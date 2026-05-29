import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_style("darkgrid")

x = np.linspace(-2*np.pi, 2*np.pi, 200)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(10, 5))

sns.lineplot(x=x, y=y_sin, label='sin(x)', linewidth=2)
sns.lineplot(x=x, y=y_cos, label='cos(x)', linewidth=2)

ax.set_title('Тригонометрические функции', fontsize=14)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend()
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=0, color='black', linewidth=0.5)

plt.tight_layout()
plt.savefig('lesson2_seaborn.png')
plt.show()

print("График сохранен как lesson2_seaborn.png")
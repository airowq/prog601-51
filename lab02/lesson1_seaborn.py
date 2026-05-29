import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

x = np.linspace(-5, 5, 100)
y1 = x**2
y2 = x**3

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

sns.lineplot(x=x, y=y1, color='teal', linewidth=2, ax=ax1)
ax1.set_title('y = x²')
ax1.set_xlabel('x')
ax1.set_ylabel('y')

sns.lineplot(x=x, y=y2, color='coral', linewidth=2, ax=ax2)
ax2.set_title('y = x³')
ax2.set_xlabel('x')
ax2.set_ylabel('y')

plt.tight_layout()
plt.savefig('lesson1_seaborn.png')
plt.show()

print("График сохранен как lesson1_seaborn.png")
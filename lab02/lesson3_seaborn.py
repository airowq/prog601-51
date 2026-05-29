import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

np.random.seed(42)
data_normal = np.random.normal(0, 1, 1000)
data_uniform = np.random.uniform(-3, 3, 1000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

sns.histplot(data_normal, bins=30, kde=True, color='purple', ax=ax1)
ax1.set_title('Нормальное распределение')
ax1.set_xlabel('Значение')
ax1.set_ylabel('Частота')

sns.histplot(data_uniform, bins=30, kde=True, color='green', ax=ax2)
ax2.set_title('Равномерное распределение')
ax2.set_xlabel('Значение')
ax2.set_ylabel('Частота')

plt.tight_layout()
plt.savefig('lesson3_seaborn.png')
plt.show()

print("График сохранен как lesson3_seaborn.png")
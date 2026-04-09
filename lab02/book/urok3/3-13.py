import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = [i for i in range(10)]
y = [i*2 for i in range(10)]
plt.plot(x, y)
plt.xlabel('Ось X\nНезависимая величина', fontsize=14, fontweight='bold')
plt.ylabel('Ось Y\nЗависимая величина', fontsize=14, fontweight='bold')

plt.show()
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = [i for i in range(10)]
y = [i*2 for i in range(10)]
plt.plot(x, y)
plt.xlabel('Ось X')
plt.ylabel('Ось Y')

plt.show()
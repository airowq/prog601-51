import matplotlib.pyplot as plt
import numpy as np
plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
x = np.linspace(0, 10, 50)
y = x

plt.title('Линейная зависимость y = x')
plt.xlabel('x') 
plt.ylabel('y') 
plt.grid()
plt.plot(x, y) 
plt.show()
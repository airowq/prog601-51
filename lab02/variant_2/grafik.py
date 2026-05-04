import numpy as np
import matplotlib.pyplot as plt

def f1(x):
    return np.exp(np.sin(x))
def f2(x):
    return np.exp(x) - 1 / np.sqrt(x)

x = np.linspace(0.1, 2, 500)
y1 = f1(x)
y2 = f2(x)

plt.figure(figsize=(12, 7))
plt.plot(x, y1, 'b-', linewidth=2, label='$f_1(x) = e^{\\sin x}$')
plt.plot(x, y2, 'g-', linewidth=2, label='$f_2(x) = e^x - \\frac{1}{\\sqrt{x}}$')

plt.title('Графики функций $f_1(x) = e^{\\sin x}$ и $f_2(x) = e^x - \\frac{1}{\\sqrt{x}}$', fontsize=16, fontweight='bold')
plt.xlabel('Ось X', fontsize=14)
plt.ylabel('Ось Y', fontsize=14)
plt.legend(loc='best',fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
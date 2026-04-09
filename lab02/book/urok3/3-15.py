import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

x = [i for i in range(10)]
y = [i*2 for i in range(10)]
bbox_properties=dict(boxstyle='darrow, pad=0.3', ec='k', fc='y', ls='-',
lw=3)
plt.text(2, 7, 'HELLO!', fontsize=15, bbox=bbox_properties)
plt.plot(range(0,10), range(0,10))

plt.show()
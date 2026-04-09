import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import math
from matplotlib.font_manager import FontProperties

plt.title('Title', fontproperties=FontProperties(family='monospace',
style='italic', weight='heavy', size=15))
plt.plot(range(0,10), range(0,10))

plt.show()
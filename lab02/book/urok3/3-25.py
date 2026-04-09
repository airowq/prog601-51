import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

np.random.seed(123)
vals = np.random.randint(10, size=(7, 7))
plt.pcolor(vals, cmap=plt.get_cmap('viridis', 11))
plt.colorbar(orientation='horizontal',
 shrink=0.9, extend='max', extendfrac=0.2,
 extendrect=False, drawedges=False)

plt.show()
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import math
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

np.random.seed(123)
vals = np.random.randint(15, size=(7, 7))
fig, ax = plt.subplots()
gr = ax.pcolor(vals)
axins = inset_axes(ax, width="7%", height="50%", loc='lower left',
bbox_to_anchor=(1.05, 0., 1, 1), bbox_transform=ax.transAxes,
borderpad=0)
plt.colorbar(gr, cax=axins)

plt.show()
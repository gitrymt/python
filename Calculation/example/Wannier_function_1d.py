# -*- coding: utf-8 -*-
"""
Example for calculation of Wannier function: 1D optical lattice

Created on Wed Nov  1 10:47:28 2017
@author: gitrymt
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d

# Lattice depth V_lat = s Er
s = 10

# Calculation
q, Energy, x, Wannier_function = calcBand_1d(s, Wannier_calc=True)

# Plot calculation result
fig = plt.figure(figsize=(8, 10))
plt.rcParams["font.size"] = 14
plt.hold(True)
plt.xlim(-1, 1)

plt.xlabel('Position x ($d$)')
plt.ylabel('$|w(x)|^2$')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.set_xticks(np.arange(-1, 1.5, 0.5))
ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.plot(x, np.abs(Wannier_function[:, 0:3:2])**2, '-', linewidth=2)
plt.plot(x, np.abs(Wannier_function[:, 1:3:2])**2, '--', linewidth=2)

plt.show()

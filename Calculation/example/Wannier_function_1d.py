# -*- coding: utf-8 -*-
"""
Example for calculation of Wannier function: 1D optical lattice

Created on Wed Nov  1 10:47:28 2017
@author: gitrymt
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import time

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

# Lattice depth V_lat = s Er
s = 10

# Calculation
Nloop = 1
start = time.time()

for i in range(Nloop):
    q, Energy, x, Wannier_function, C = calcBand_1d(s, Wannier_calc=True)
    
elapsed_time = time.time() - start
print ("elapsed_time (%d times): %.3f (sec.)" % (Nloop, elapsed_time))
print ("elapsed_time (average): %.3f (msec.)" % (elapsed_time/Nloop * 1e3))

# Plot calculation result
fig = plt.figure(figsize=(8, 10), dpi=100)
plt.xlim(-1, 1)

plt.xlabel('Position x')
plt.ylabel('$|w(x)|^2$')
plt.xticks(np.arange(-1, 1.5, 0.5), ["-$d$","-$d$/2","0","$d$/2","$d$"]) # xlocs：位置の配列　xlabels：ラベルの配列

plt.title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.plot(x, np.abs(Wannier_function[:, 0:3:2])**2, '-', linewidth=2)
plt.plot(x, np.abs(Wannier_function[:, 1:3:2])**2, '--', linewidth=2)

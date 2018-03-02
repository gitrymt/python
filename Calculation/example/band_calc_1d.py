# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: 1D optical lattice

Created on Tue Oct 31 20:15:40 2017
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import time

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d, calcBand_tri
import set_default_params

set_default_params.plot_params()

# Lattice depth V_lat = s Er
s = 17.1

# Calculation
Nloop = 10
start = time.time()

for i in range(Nloop):
    q, Energy = calcBand_1d(s, angle=np.pi * 120 / 180)

elapsed_time = time.time() - start
print ("elapsed_time (%d times): %.3f (sec.)" % (Nloop, elapsed_time))
print ("elapsed_time (average): %.3f (msec.)" % (elapsed_time/Nloop * 1e3))

# Plot calculation result
fig = plt.figure(figsize=(6, 10), dpi=150)
plt.xlim(-1, 1)
plt.ylim(0, 40)

plt.xlabel('$q$ ($d^{-1}$)')
plt.ylabel('Energy $\epsilon_q$ ($E_R$)')
plt.xticks(np.arange(-1, 1.5, 0.5), ["$-\pi$","$-\pi/2$","0","$\pi/2$","$\pi$"]) # xlocs：位置の配列　xlabels：ラベルの配列
plt.title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')

for i in range(0, 5):
    plt.plot(q, Energy[2*i, :], '-', linewidth=2)
    plt.plot(q, Energy[2*i+1, :], '--', linewidth=2)

plt.tight_layout()

#plt.savefig('./hoge.pdf', dpi=200)
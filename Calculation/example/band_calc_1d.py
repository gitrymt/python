# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: 1D optical lattice

Created on Tue Oct 31 20:15:40 2017
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d

# Lattice depth V_lat = s Er
s = 17.1

# Calculation
q, Energy = calcBand_1d(s, angle=np.pi * 120 / 180)

# Plot calculation result
fig = plt.figure(figsize=(6, 10))
plt.rcParams["font.size"] = 14
plt.hold(True)
plt.xlim(-1, 1)
plt.ylim(0, 40)

plt.xlabel('$q$ ($d^{-1}$)')
plt.ylabel('Energy $\epsilon_q$ ($E_R$)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.set_xticklabels(["$-\pi$","$-\pi/2$","0","$\pi/2$","$\pi$"])
ax.set_xticks(np.arange(-1, 1.5, 0.5))
ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
for i in range(0, 5):
    plt.plot(q, Energy[2*i, :], '-', linewidth=2)
    plt.plot(q, Energy[2*i+1, :], '--', linewidth=2)

plt.tight_layout()
#plt.show()

#plt.savefig('./hoge.pdf', dpi=200)
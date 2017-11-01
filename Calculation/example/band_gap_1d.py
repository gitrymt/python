# -*- coding: utf-8 -*-
"""
Example for calculation of band gap: 1D optical lattice

Created on Tue Oct 31 19:39:19 2017
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

# import user library
sys.path.append("../func")
from func_band_calc import calcBand_1d

# Initialization
ds = 0.5
s_array = np.arange(0, 35 + ds, ds)
dEmin = np.zeros([len(s_array), 6])
dEmax = np.zeros([len(s_array), 6])

# Calculation
for i, s in enumerate(s_array):
    q, Eeven, Eodd = calcBand_1d(s)
    
    Eodd = Eodd - np.min(Eeven[0, :])
    Eeven = Eeven - np.min(Eeven[0, :])
    
    for n in range(3):
        dEmin[i, 2 * n] = np.min(Eeven[n, :])
        dEmax[i, 2 * n] = np.max(Eeven[n, :])
        dEmin[i, 2 * n + 1] = np.min(Eodd[n, :])
        dEmax[i, 2 * n + 1] = np.max(Eodd[n, :])

# Plot result
fig = plt.figure(figsize=(12, 8))
plt.rcParams["font.size"] = 14
plt.hold(True)
plt.xlim(0, max(s_array))
plt.ylim(-2.5, 30)
plt.xlabel('Lattice potential $V_{lat}$ ($E_R$)')
plt.ylabel('Energy $\epsilon$ ($E_R$)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)

for n in range(6):
    print(n)
    plt.fill_between(s_array,dEmin[:, n],dEmax[:, n],alpha=0.25)
    plt.plot(s_array, dEmin[:, n], 'k-', linewidth=2, alpha=0.5)
    plt.plot(s_array, dEmax[:, n], 'k-', linewidth=2, alpha=0.5)

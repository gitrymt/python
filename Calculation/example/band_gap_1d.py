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
sys.path.append('../function')
from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

# Initialization
ds = 0.5
s_array = np.arange(0, 35 + ds, ds)
dEmin = np.zeros([len(s_array), 6])
dEmax = np.zeros([len(s_array), 6])

# Calculation
for i, s in enumerate(s_array):
    q, Energy = calcBand_1d(s)
    
    dE = Energy - np.min(Energy[0, :])
    
    for n in range(6):
        dEmin[i, n] = np.min(dE[n, :])
        dEmax[i, n] = np.max(dE[n, :])
        
# Plot result
fig = plt.figure(figsize=(12, 8))
plt.xlim(0, max(s_array))
plt.ylim(-2.5, 30)
plt.xlabel('Lattice potential $V_{lat}$ ($E_R$)')
plt.ylabel('Energy $\epsilon$ ($E_R$)')

for n in range(6):
    plt.fill_between(s_array,dEmin[:, n],dEmax[:, n],alpha=0.25)
    plt.plot(s_array, dEmin[:, n], 'k-', linewidth=2, alpha=0.5)
    plt.plot(s_array, dEmax[:, n], 'k-', linewidth=2, alpha=0.5)

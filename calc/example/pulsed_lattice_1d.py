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
s_array = np.arange(ds, 35 + ds, ds)
dEmin = np.zeros(len(s_array))
dEmax = np.zeros(len(s_array))

# Calculation
for i, s in enumerate(s_array):
    q, Eeven, Eodd = calcBand_1d(s)
    
    dE = Eeven[1] - Eeven[0]
    dEmin[i] = np.min(dE)
    dEmax[i] = np.max(dE)

# Sample parameters
hbar = 1.06e-34
mass = 87 * 1.66e-27
lambda_lat = 1064e-9
k_lat = 2 * np.pi / lambda_lat
Er = (hbar * k_lat)**2 / (2 * mass)

# Result
tau = 2 * np.pi * hbar / (dEmin * Er) * 1e6

# Plot result
fig2 = plt.figure(figsize=(12, 8))
plt.rcParams["font.size"] = 16
plt.hold(True)
plt.xlim(0, max(s_array))
plt.xlabel('Lattice potential $V_{lat}$ ($E_R$)')
plt.ylabel(r'$\tau$ ($\mu$sec.)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)

plt.plot(s_array, tau)

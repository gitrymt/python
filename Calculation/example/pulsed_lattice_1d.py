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

# Initialization
ds = 0.5
s_array = np.arange(ds, 35 + ds, ds)
dEmin = np.zeros(len(s_array))
dEmax = np.zeros(len(s_array))

# Calculation
for i, s in enumerate(s_array):
    q, Energy = calcBand_1d(s, angle=np.pi * 120 / 180)
    
    dE = Energy[2] - Energy[0]
    dEmin[i] = np.min(dE)
    dEmax[i] = np.max(dE)

# Sample parameters
hbar = 1.054571726e-34 # J/Hz
lambda_lat = 1064e-9 # m
k_lat = 2 * np.pi / lambda_lat # m^-1
mass = 86.909180520 * 1.660538782e-27 # kg
Er = (hbar * k_lat)**2 / (2 * mass) # J

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

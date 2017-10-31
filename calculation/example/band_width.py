# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 19:39:19 2017

@author: gitrymt
"""
import sys
import numpy as np

sys.path.append("../func")
from func_band_calc import calcBand_1d
import matplotlib.pyplot as plt

hbar = 1.06e-34
mass = 87 * 1.66e-27
lambda_lat = 1064e-9
k_lat = 2 * np.pi / lambda_lat
Er = (hbar * k_lat)**2 / (2 * mass)

s_array = np.array(range(301))/10
dE = np.zeros(len(s_array))

for i, s in enumerate(s_array):
#    print(i, s)
    
    q, Eeven, Eodd = calcBand_1d(s)
    
    dE[i] = np.min(Eeven[1]) - np.min(Eeven[0])
    
tau = 2 * np.pi * hbar / (dE * Er) * 1e6

###
fig = plt.figure(figsize=(16, 8))
plt.rcParams["font.size"] = 14
plt.hold(True)
plt.xlim(0, max(s_array))
plt.ylim(0, 30)
plt.xlabel('Lattice potential $V_{lat}$ ($E_R$)')
plt.ylabel('$E_2 - E_0$ ($E_R$)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)

plt.plot(s_array, dE, '-', linewidth=2)

###
fig2 = plt.figure(figsize=(12, 6))
plt.rcParams["font.size"] = 14
plt.hold(True)
plt.xlim(0, max(s_array))
plt.xlabel('Lattice potential $V_{lat}$ ($E_R$)')
plt.ylabel(r'$\tau$ ($\mu$sec.)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)

plt.plot(s_array, tau)

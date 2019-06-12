# -*- coding: utf-8 -*-
"""
Example for calculation of Bloch function: 1D optical lattice

Created on Fri Nov 16 18:12:16 2018
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
#    q, Energy, x, Wannier_function, C = calcBand_1d(s,Nsite=20, Wannier_calc=True, angle=np.pi * 20 / 180)
    q, Energy, x, Wannier_function, C = calcBand_1d(s,Nsite=20, Wannier_calc=True)
    
elapsed_time = time.time() - start
print ("elapsed_time (%d times): %.3f (sec.)" % (Nloop, elapsed_time))
print ("elapsed_time (average): %.3f (msec.)" % (elapsed_time/Nloop * 1e3))

# Calculation of Bloch function
q = np.linspace(-1, 1, 101)
Nsite = np.linspace(0, 19, 20) - 20/2


x = np.linspace(-1, 1, 301)
phi = np.zeros(x.size, dtype=np.complex128)

for i, N in enumerate(Nsite):
    print(N)
    phi += C[0, q == 0, i] * np.exp(-1j * 2 * np.pi * N) * x # n = 0 band, q = 0 (Gamma point)
#    phi += C[0, q == 0, N] * np.exp(-1j * 2 * np.pi * N) * x # n = 0 band, q = 0 (Gamma point)

A = np.abs(C[0, q == 0, :])**2

fig = plt.figure(figsize=(4, 5), dpi=100)
plt.xlim(-3, 3)

plt.xlabel('Position x')
plt.ylabel('$|w(x)|^2$')
#plt.xticks(np.arange(-1, 1.5, 0.5), ["-$d$","-$d$/2","0","$d$/2","$d$"]) # xlocs：位置の配列　xlabels：ラベルの配列

#plt.title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.plot(Nsite, A[0, :], '.', linewidth=2) # Ground state

# Plot calculation result
#fig = plt.figure(figsize=(8, 10), dpi=100)
#plt.xlim(-1, 1)
#
#plt.xlabel('Position x')
#plt.ylabel('$|w(x)|^2$')
#plt.xticks(np.arange(-1, 1.5, 0.5), ["-$d$","-$d$/2","0","$d$/2","$d$"]) # xlocs：位置の配列　xlabels：ラベルの配列
#
#plt.title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
#plt.plot(x, np.abs(Wannier_function[:, 0])**2, '-', linewidth=2) # Ground state
#plt.plot(x, np.abs(Wannier_function[:, 1])**2, '-', linewidth=2) # 1st excited state
#plt.plot(x, np.abs(Wannier_function[:, 2])**2, '--', linewidth=2) # 2nd excited state
#plt.plot(x, np.abs(Wannier_function[:, 3])**2, '-.', linewidth=2) # 3rd excited state

#plt.plot(x, np.abs(Wannier_function[:, 4])**2, ':', linewidth=2) # 4th excited state


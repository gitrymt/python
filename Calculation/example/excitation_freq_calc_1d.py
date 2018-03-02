# -*- coding: utf-8 -*-
"""
Example for calculation of excitaiton frequency: 1D optical lattice

Created on Tue Feb 20 19:32:57 2018
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

# Physical constants
m =  86.909180520 * 1.660538921 * 1e-27 # Mass of 87 Rb (kg)
h = 6.62606896 * 1e-34 # Prank constant (J/Hz)
wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
Er = h**2 / (2 * m * wavelength**2)

f_ex = []
f_ex_max = []
f_ex_min = []

s_list = np.linspace(0, 75, 151)

for s in s_list:
    # Lattice depth V_lat = s Er
    # Calculation
    q, Energy = calcBand_1d(s, angle=np.pi * 120 / 180)
    
    # Plot calculation result
    if False:
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
    
    # Excitation frequency (1st band -> 3rd band)    
    dE = Energy[2, :] - Energy[0, :]
    tmp = dE[q==0] * Er / h
    
    f_ex = np.append(f_ex, tmp[0])
    f_ex_max = np.append(f_ex_max, np.max(dE) * Er / h)
    f_ex_min = np.append(f_ex_min, np.min(dE) * Er / h)

fig = plt.figure(dpi=150)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list))
plt.ylim(0, 50)

plt.xlabel('Lattice depth ($E_R$)')
plt.ylabel('Excitation frequency $f_{ex}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.grid(lw=0.5, ls='--')
plt.fill_between(s_list, f_ex_min * 1e-3, f_ex_max * 1e-3, alpha=0.5)
#plt.plot(s_list, f_ex*1e-3, '-', linewidth=2)
#plt.plot(s_list, f_ex_max*1e-3, '-', linewidth=2)
#plt.plot(s_list, f_ex_min*1e-3, '-', linewidth=2)

plt.tight_layout()

#print('Excitation frequecny ((1st band -> 3rd band))', f_ex*1e-3, 'kHz')

df = pd.DataFrame({'Lattice depth (Er)': s_list,
                     'Excitation freq. min (Hz)': f_ex_min,
                     'Excitation freq. max (Hz)': f_ex_max,
                     'Excitation freq. (Hz)': f_ex})
    
df.to_csv('./fex_1D.txt')

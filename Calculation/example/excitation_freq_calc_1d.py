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
from scipy import constants
from tqdm import tqdm

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

SW_VERT = False

# Physical constants
m =  86.909180520 * constants.m_u # Mass of 87 Rb (kg)

if SW_VERT:
    wavelength = 810 * 1e-9 # Lattice wavelength (nm)
    angle_lat = np.pi * 2 * 9.05 / 180
    fname = './fex_1D_vert.txt'
    s_list = np.linspace(0, 2500, 1001)
else:
    wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
    angle_lat = np.pi * 2 * 60 / 180
    fname = './fex_1D.txt'
    s_list = np.linspace(0, 1500, 101)

Er = constants.h**2 / (2 * m * wavelength**2)

f_ex = []
f_ex_max = []
f_ex_min = []

# s_list = np.linspace(0, 120 * constants.k * 1e-6 / Er, 251)

for s in tqdm(s_list):
    # Lattice depth V_lat = s Er
    # Calculation
    q, Energy = calcBand_1d(s, Nsite=2*20, angle=angle_lat)
    # q, Energy = calcBand_1d(s, Nsite=2*50, angle=angle_lat)
    
    # Plot calculation result
    if False:
        fig = plt.figure(figsize=(6, 10))
        plt.rcParams["font.size"] = 14
        plt.hold(True)
        plt.xlim(-1, 1)
        plt.ylim(0, 40)
        
        plt.xlabel(r'$q$ ($d^{-1}$)')
        plt.ylabel(r'Energy $\epsilon_q$ ($E_R$)')
        ax = plt.gca()
        ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
        ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
        ax.set_xticklabels([r"$-\pi$",r"$-\pi/2$","0",r"$\pi/2$",r"$\pi$"])
        ax.set_xticks(np.arange(-1, 1.5, 0.5))
        ax.set_title(r'Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + r' $E_R$')
        for i in range(0, 5):
            plt.plot(q, Energy[2*i, :], '-', linewidth=2)
            plt.plot(q, Energy[2*i+1, :], '--', linewidth=2)
        
        plt.tight_layout()
        #plt.show()
        
        #plt.savefig('./hoge.pdf', dpi=200)
    
    # Excitation frequency (1st band -> 3rd band)    
    dE = Energy[2, :] - Energy[0, :]
    tmp = dE[q==0]
    
    f_ex = np.append(f_ex, tmp[0])
    f_ex_max = np.append(f_ex_max, np.max(dE))
    f_ex_min = np.append(f_ex_min, np.min(dE))

f_ex *= Er / constants.h
f_ex_max *= Er / constants.h
f_ex_min *= Er / constants.h

omega_harm = 2 * Er * np.sin(angle_lat/2) * np.sqrt(s_list) / constants.hbar
f_harm = 2 * omega_harm / (2 * np.pi)

fig = plt.figure(dpi=150)
plt.subplot(2, 2, 1)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list))
#plt.ylim(0, 50)

plt.xlabel(r'Lattice depth ($E_R$)')
plt.ylabel(r'Excitation frequency $f_{ex}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.grid(lw=0.5, ls='--')
plt.fill_between(s_list, f_ex_min * 1e-3, f_ex_max * 1e-3, alpha=0.5)
plt.plot(s_list, f_ex*1e-3, '--', c='#5599ff', linewidth=1, label='Band calculation')
plt.plot(s_list, f_harm*1e-3, '--', c='#ff5555', linewidth=1, label='Harmonic approximation')
# plt.plot(s_list, f_ex_max*1e-3, '-', linewidth=2)
# plt.plot(s_list, f_ex_min*1e-3, '-', linewidth=2)
plt.legend()

plt.subplot(2, 2, 2)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list * Er / constants.k * 1e6))
#plt.ylim(0, 50)

plt.xlabel(r'Lattice depth ($\mu$K)')
plt.ylabel(r'Excitation frequency $f_{ex}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.grid(lw=0.5, ls='--')
plt.fill_between(s_list * Er / constants.k * 1e6, f_ex_min * 1e-3, f_ex_max * 1e-3, alpha=0.5)
# plt.plot(s_list * Er / 1.38e-23 * 1e6, f_ex*1e-3, '-', linewidth=1)
plt.plot(s_list * Er / constants.k * 1e6, f_ex * 1e-3, '--', c='#5599ff', lw=1, label='Band calculation')
plt.plot(s_list * Er / constants.k * 1e6, f_harm*1e-3, '--', c='#ff5555', lw=1, label='Harmonic approximation')
# plt.plot(s_list * Er / constants.k * 1e6, f_ex_max * 1e-3, '-', linewidth=2)
# plt.plot(s_list * Er / constants.k * 1e6, f_ex_min * 1e-3, '-', linewidth=2)
plt.legend()

plt.subplot(2, 2, 3)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list))
#plt.ylim(0, 50)

plt.xlabel(r'Lattice depth ($E_R$)')
plt.ylabel(r'$f_{ex}^{BC} - f_{ex}^{HA}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.grid(lw=0.5, ls='--')
plt.plot(s_list, (f_ex-f_harm)*1e-3, '--', c='#5599ff', linewidth=1)
# plt.plot(s_list, f_ex_max*1e-3, '-', linewidth=2)
# plt.plot(s_list, f_ex_min*1e-3, '-', linewidth=2)

plt.subplot(2, 2, 4)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list * Er / constants.k * 1e6))
#plt.ylim(0, 50)

plt.xlabel(r'Lattice depth ($E_R$)')
plt.ylabel(r'$f_{ex}^{BC} - f_{ex}^{HA}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
plt.grid(lw=0.5, ls='--')
plt.plot(s_list * Er / constants.k * 1e6, (f_ex-f_harm)*1e-3, '--', c='#5599ff', linewidth=1)

# Show figure
plt.tight_layout()
plt.show()

#print('Excitation frequecny ((1st band -> 3rd band))', f_ex*1e-3, 'kHz')

df = pd.DataFrame({'Lattice depth (Er)': s_list,
                   'Lattice depth (uK)': s_list * Er / constants.k * 1e6,
                   'Excitation freq. min (Hz)': f_ex_min,
                   'Excitation freq. max (Hz)': f_ex_max,
                   'Excitation freq. (Hz)': f_ex})
    
df.to_csv(fname, sep='\t')

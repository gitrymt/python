# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: Triangular optical lattice

Created on Tue Feb 20 20:32:31 2018
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
from func_band_calc import calcBand_tri
import set_default_params

set_default_params.plot_params()

# Physical constants
mass =  86.909180520 * constants.m_u # Mass of 87 Rb (kg)
wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
Er = constants.h**2 / (2 * mass * wavelength**2)

s_max = 2500
# s_list = np.linspace(1500, s_max, s_max-1500+1)
s_list = np.linspace(0, s_max, s_max+1)/2
# s_list = np.linspace(0, s_max, 21)/2

n_list = [(0, 0)]
dE = np.array([])

f_ex = [()]
f_ex_max = []
f_ex_min = []

m = 16
# Nsite = 2 * m + 1

# l_list = [(x, y) for x in np.linspace(-m, m, Nsite) for y in np.linspace(-m, m, Nsite)]
# E = np.zeros([len(n_list), Nsite**2])

for i_s, s in tqdm(enumerate(s_list)):    # Lattice depth V_lat = s Er
    # Calculation
    E, Ctmp = calcBand_tri(s=s, m=m, Nband=10, nq_list=n_list, Wannier_calc=False)

    dE_tmp = (E - E[0, 0]) * Er / constants.h
    f_ex = np.append(f_ex, np.array(dE_tmp[0][1:11]))

f_ex = np.reshape(f_ex, [-1,10])

s_list = s_list * 2
omega_harm = Er * 3 / 2 * np.sqrt(s_list) / constants.hbar
f_harm = 2 * omega_harm / (2 * np.pi)

if True:
    fig = plt.figure()
    plt.subplot(2, 1, 1)
    plt.xlim(0, np.max(s_list))
    plt.ylim(0, 300)

    plt.xlabel('Lattice depth ($E_R$)')
    plt.ylabel('$E_n - E_0$/h (kHz)')
    ax = plt.gca()
    ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    plt.grid(lw=0.5, ls='--')
    # plt.plot(s_list, f_ex[:, 0]*1e-3, label=r'$1^{st} \rightarrow 2^{nd}$')
    # plt.plot(s_list, f_ex[:, 1]*1e-3, label=r'$1^{st} \rightarrow 3^{rd}$')
    plt.plot(s_list, f_ex[:, 2]*1e-3, label=r'$E_3 - E_0$')
    # plt.plot(s_list, f_ex[:, 3]*1e-3, label=r'$1^{st} \rightarrow 5^{th}$')
    # plt.plot(s_list, f_ex[:, 4]*1e-3, label=r'$1^{st} \rightarrow 6^{th}$')
    # plt.plot(s_list, f_ex[:, 5]*1e-3, label=r'$1^{st} \rightarrow 7^{th}$')
    plt.plot(s_list, f_ex[:, 6]*1e-3, '--', label=r'$E_7 - E_0$')
    plt.plot(s_list, f_harm*1e-3, '--', c='#ff5555', linewidth=1, label=r'$2\omega_\mathrm{HO}/2\pi$')
    plt.legend()

    plt.subplot(2, 1, 2)
    s_list_temp = s_list * Er / constants.k * 1e6
    plt.xlim(0, np.max(s_list_temp))
    plt.ylim(0, 300)

    plt.xlabel('Lattice depth ($\mu$K)')
    plt.ylabel('$E_n - E_0$/h (kHz)')
    ax = plt.gca()
    ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    plt.grid(lw=0.5, ls='--')
    # plt.plot(s_list_temp, f_ex[:, 0]*1e-3, label=r'$1^{st} \rightarrow 2^{nd}$')
    # plt.plot(s_list_temp, f_ex[:, 1]*1e-3, label=r'$1^{st} \rightarrow 3^{rd}$')
    plt.plot(s_list_temp, f_ex[:, 2]*1e-3, label=r'$E_3 - E_0$')
    # plt.plot(s_list_temp, f_ex[:, 3]*1e-3, label=r'$1^{st} \rightarrow 5^{th}$')
    # plt.plot(s_list_temp, f_ex[:, 4]*1e-3, label=r'$1^{st} \rightarrow 6^{th}$')
    # plt.plot(s_list_temp, f_ex[:, 5]*1e-3, label=r'$1^{st} \rightarrow 7^{th}$')
    plt.plot(s_list_temp, f_ex[:, 6]*1e-3, '--', label=r'$E_7 - E_0$')
    plt.plot(s_list_temp, f_harm*1e-3, '--', c='#ff5555', linewidth=1, label=r'$2\omega_\mathrm{HO}/2\pi$')
    plt.legend()

    plt.tight_layout()
    plt.show()

df = pd.DataFrame({'Lattice depth (Er)': s_list,
                   'Lattice depth (uK)': s_list_temp,
                   'Excitation freq. 1->2 (Hz)': f_ex[:, 0],
                   'Excitation freq. 1->3 (Hz)': f_ex[:, 1],
                   'Excitation freq. 1->4 (Hz)': f_ex[:, 2],
                   'Excitation freq. 1->5 (Hz)': f_ex[:, 3],
                   'Excitation freq. 1->6 (Hz)': f_ex[:, 4],
                   'Excitation freq. 1->7 (Hz)': f_ex[:, 5],
                   'Excitation freq. 1->8 (Hz)': f_ex[:, 6],
                   'Excitation freq. 1->9 (Hz)': f_ex[:, 7],
                   'Excitation freq. 1->10 (Hz)': f_ex[:, 8]})
    
# df.to_csv('./fex_tri.txt', sep='\t')
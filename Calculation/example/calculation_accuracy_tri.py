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

import time

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_tri
import set_default_params

set_default_params.plot_params()

# Physical constants
m =  86.909180520 * constants.m_u # Mass of 87 Rb (kg)
wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
Er = constants.h**2 / (2 * m * wavelength**2)

n_list = [(0, 0)]
dE = np.array([])

f_ex = [()]

s = 2000/2
m_max = 40
m_min = 30
m_list = np.array(np.linspace(m_min, m_max, m_max-m_min+1), dtype=np.int)

# m_list = np.array(np.linspace(5, 12, 12-5+1), dtype=np.int)
# m_list = np.array([20], dtype=np.int)

Nsite_min = 2 * np.min(m_list) + 1

elapsed_times = []

for m_tmp in tqdm(m_list):
# for m_tmp in m_list:
    start = time.time()

    # Calculation
    Nsite = 2 * m_tmp + 1

    # E = np.zeros([len(n_list), Nsite**2])
    l_list = [(x, y) for x in np.linspace(-m_tmp, m_tmp, Nsite) for y in np.linspace(-m_tmp, m_tmp, Nsite)]
    
    E, Ctmp = calcBand_tri(s=s, m=m_tmp, Nband=10, nq_list=n_list, Wannier_calc=False)
    dE_tmp = (E - E[0, 0]) * Er / constants.h * 1e-3
    # dE_tmp = (E - E[0, 0])
    # dE_tmp = (E) * Er / constants.h
    
    f_ex = np.append(f_ex, np.array(dE_tmp[0][1:Nsite_min**2-1]))
    # print(f_ex.shape)

    elapsed_times = np.append(elapsed_times, time.time() - start)

f_ex = np.reshape(f_ex, [-1,Nsite_min**2-2])

# print(len(m_list), f_ex.shape)

Nsite_list = 2 * m_list + 1

if False:
    fig = plt.figure()
    # plt.xlim(25, np.max(Nsite_list))
    # plt.ylim(0, 300)

    plt.xlabel('$N_\mathrm{site}$')
    plt.ylabel('($E_n - E_0$)/h (kHz)')
    ax = plt.gca()
    ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    plt.grid(lw=0.5, ls='--')
    for n in range(f_ex.shape[1]):
        # plt.plot(Nsite_list, f_ex[:, n]*1e-3, 'o', label=r'$E_{%d}$' % (n+1))
        plt.plot(Nsite_list, f_ex[:, n], 'o--', label=r'$E_{%d}$' % (n+1))
    # plt.legend()

    plt.tight_layout()
    plt.show()

if True:
    fig = plt.figure()
    # plt.xlim(25, np.max(Nsite_list))
    # plt.ylim(0, 300)

    plt.xlabel('$N_\mathrm{site}$')
    plt.ylabel('Calculation time (sec.)')
    ax = plt.gca()
    ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
    plt.grid(lw=0.5, ls='--')
    plt.semilogy(Nsite_list, elapsed_times, 'o--')
    # plt.legend()

    plt.tight_layout()
    plt.show()


# df = pd.DataFrame({'Lattice depth (Er)': s_list,
#                    'Lattice depth (uK)': s_list_temp,
#                    'Excitation freq. 1->2 (Hz)': f_ex[:, 0],
#                    'Excitation freq. 1->3 (Hz)': f_ex[:, 1],
#                    'Excitation freq. 1->4 (Hz)': f_ex[:, 2],
#                    'Excitation freq. 1->5 (Hz)': f_ex[:, 3],
#                    'Excitation freq. 1->6 (Hz)': f_ex[:, 4],
#                    'Excitation freq. 1->7 (Hz)': f_ex[:, 5],
#                    'Excitation freq. 1->8 (Hz)': f_ex[:, 6],
#                    'Excitation freq. 1->9 (Hz)': f_ex[:, 7],
#                    'Excitation freq. 1->10 (Hz)': f_ex[:, 8]})

# df.to_csv('./fex_hoge.txt', sep='\t')
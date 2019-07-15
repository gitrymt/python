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

import sympy as sp

import time

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

# Physical constants
m =  86.909180520 * constants.m_u # Mass of 87 Rb (kg)
wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
Er = constants.h**2 / (2 * m * wavelength**2)

n_list = [(0, 0)]
dE = np.array([])

f_ex = [()]

s = 5
m_max = 50
m_min = 10
m_list = np.array(np.linspace(m_min, m_max, (m_max-m_min)/10+1), dtype=np.int)

# m_list = np.array(np.linspace(5, 12, 12-5+1), dtype=np.int)
# m_list = np.array([20], dtype=np.int)

Nsite_min = 2 * np.min(m_list) + 1
angle_lat = np.pi

elapsed_times = []
elapsed_times_std = []
N_loop = 2

m = 2
Nsite = 2 * m + 1

G = np.sin(angle_lat / 2)

Vs, q = sp.symbols('s, q', real=True)
tmp = -1/4 * sp.eye(Nsite-1)
H2 = sp.zeros(Nsite, Nsite)
H2[0:Nsite-1, 1:Nsite] += tmp
H2[1:Nsite, 0:Nsite-1] += tmp
tmp0 = sp.zeros(Nsite)
for i in range(Nsite):
    tmp0[i, i] += G * (2 * (i - m) + q)**2

H2 += tmp0 + 1/2 * sp.eye(Nsite)
# H2 += Vs/2 * sp.eye(Nsite)

# print(tmp0)
        # for i in range(Nsite):
        #     H[i][i] = G**2 * (2*(i-Nsite/2) + q[i_q])**2 + s/2

A = sp.Matrix(([3, 2], [-2, 3]))
print(H2)
print(H2.eigenvals())

# for m_tmp in tqdm(m_list):
# # for m_tmp in m_list:
#     elapsed_time_tmp = np.zeros(N_loop)

#     for ite in range(N_loop):
#         start = time.time()

#         # Calculation
#         Nsite = 2 * m_tmp + 1

#         # E = np.zeros([len(n_list), Nsite**2])
#         l_list = [(x, y) for x in np.linspace(-m_tmp, m_tmp, Nsite) for y in np.linspace(-m_tmp, m_tmp, Nsite)]
        
#         E, Ctmp = calcBand_1d(s, Nsite=2*20, angle=angle_lat)
#         # dE_tmp = (E - E[0, 0]) * Er / constants.h * 1e-3
#         # dE_tmp = (E - E[0, 0])
#         # dE_tmp = (E) * Er / constants.h
        
#         # f_ex = np.append(f_ex, np.array(dE_tmp[0][1:Nsite_min**2-1]))
#         # print(f_ex.shape)
#         elapsed_time_tmp[ite] += time.time() - start

#     elapsed_times = np.append(elapsed_times, np.mean(elapsed_time_tmp))
#     elapsed_times_std = np.append(elapsed_times_std, np.std(elapsed_time_tmp, ddof=1))

# # f_ex = np.reshape(f_ex, [-1,Nsite_min**2-2])

# # print(len(m_list), f_ex.shape)

# Nsite_list = 2 * m_list + 1

# if False:
#     fig = plt.figure()
#     # plt.xlim(25, np.max(Nsite_list))
#     # plt.ylim(0, 300)

#     plt.xlabel(r'$N_\mathrm{site}$')
#     plt.ylabel(r'($E_n - E_0$)/h (kHz)')
#     ax = plt.gca()
#     ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#     ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#     plt.grid(lw=0.5, ls='--')
#     for n in range(f_ex.shape[1]):
#         # plt.plot(Nsite_list, f_ex[:, n]*1e-3, 'o', label=r'$E_{%d}$' % (n+1))
#         plt.plot(Nsite_list, f_ex[:, n], 'o--', label=r'$E_{%d}$' % (n+1))
#     # plt.legend()

#     plt.tight_layout()
#     plt.show()

# if True:
#     df_calc_read =pd.read_csv('./calc_time_1d_tmp.txt', sep='\t')
#     # print(df_calc_read)
#     Nsite_read = df_calc_read['Nsite']
#     elapsed_time_read = df_calc_read['Calc. time (s)']
#     elapsed_time_read_std = df_calc_read['Std. of calc. time (s)']

#     fig = plt.figure()
#     # plt.xlim(25, np.max(Nsite_list))
#     # plt.ylim(0, 300)

#     plt.xlabel(r'$N_\mathrm{site}$')
#     plt.ylabel('Calculation time (sec.)')
#     ax = plt.gca()
#     ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#     ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#     plt.grid(lw=0.5, ls='--')
#     # plt.legend()
#     # ax.set_xscale("log", nonposx='clip')
#     ax.set_yscale("log", nonposy='clip')

#     plt.errorbar(Nsite_read, elapsed_time_read, yerr=elapsed_time_read_std, fmt='x--', mec='#0000ff', mfc='#aaaaff', c='#aaaaff')
#     plt.errorbar(Nsite_list, elapsed_times, yerr=elapsed_times_std, fmt='o--', mec='#ff0000', mfc='#ffaaaa', c='#ffaaaa')
#     # plt.errorbar(x, y, xerr=0.1*x, yerr=5.0 + 0.75*y)
#     # ax.set_ylim(ymin=0.1)

#     plt.tight_layout()
#     plt.show()

#     df_calc = pd.DataFrame({'Nsite': Nsite_list,
#                             'Calc. time (s)': elapsed_times,
#                             'Std. of calc. time (s)': elapsed_times_std})

#     df_calc.to_csv('./calc_time_1d.txt', sep='\t')


# # df = pd.DataFrame({'Lattice depth (Er)': s_list,
# #                    'Lattice depth (uK)': s_list_temp,
# #                    'Excitation freq. 1->2 (Hz)': f_ex[:, 0],
# #                    'Excitation freq. 1->3 (Hz)': f_ex[:, 1],
# #                    'Excitation freq. 1->4 (Hz)': f_ex[:, 2],
# #                    'Excitation freq. 1->5 (Hz)': f_ex[:, 3],
# #                    'Excitation freq. 1->6 (Hz)': f_ex[:, 4],
# #                    'Excitation freq. 1->7 (Hz)': f_ex[:, 5],
# #                    'Excitation freq. 1->8 (Hz)': f_ex[:, 6],
# #                    'Excitation freq. 1->9 (Hz)': f_ex[:, 7],
# #                    'Excitation freq. 1->10 (Hz)': f_ex[:, 8]})

# # df.to_csv('./fex_hoge.txt', sep='\t')

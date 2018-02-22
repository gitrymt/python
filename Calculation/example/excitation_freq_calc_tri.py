# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: Triangular optical lattice

Created on Tue Feb 20 20:32:31 2018
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

# import user library
sys.path.append('../function')
#from func_band_calc import calcBand_1d

# Physical constants
m =  86.909180520 * 1.660538921 * 1e-27 # Mass of 87 Rb (kg)
h = 6.62606896 * 1e-34 # Prank constant (J/Hz)
wavelength = 1064 * 1e-9 # Lattice wavelength (nm)
Er = h**2 / (2 * m * wavelength**2)

s_list = np.linspace(0, 50, 51)
#dn = 25
#
#n_list = [(x, 0) for x in np.linspace(0, 1/2, int(dn * np.sqrt(3)))] # Gamma -> M
#n_M = len(n_list) - 0.5
#
#n_list = n_list + [(1/2 - x/6, -x/3) for x in np.linspace(0, 1, dn) if x>0] # M -> K
##n_K = len([(0.5, -x) for x in np.linspace(0, 1/3, dn)])
#n_K = len(n_list) - 0.5
#
#n_list = n_list + [(x/3, -x/3) for x in np.linspace(1, 0, dn*2) if x<1] # K -> Gamma
##n_Gamma = len([(x, -x) for x in np.linspace(1/3, 0, dn*2)])
#n_Gamma = len(n_list)

n_list = [(0, 0)]
dE = np.array([])

f_ex = [()]
f_ex_max = []
f_ex_min = []

for s in s_list:
    # Lattice depth V_lat = s Er
    # Calculation
    m = 6
    Nsite = 2 * m + 1
    
#    b1 = np.array([1, 0])
#    b2 = np.array([-1, -np.sqrt(3)])/2
#    b3 = np.array([-1, np.sqrt(3)])/2
#    
#    p_Gamma = 0 * b1 + 0 * b2
#    p_M = 1/2 * b1 + 0 * b2
#    p_K = 1/3 * b1 - 1/3 * b2
#    fig = plt.figure()
#    ax = fig.add_subplot(111)
#    # 5点(0.1,0.1),(0.1,0.6),(0.7,0.8),(0.6,0.4),(0.6,0.1)を通る多角形を描画
#    poly = plt.Polygon((p_Gamma, p_M, p_K, p_Gamma),fc="#ff0000", alpha=0.5)
#    ax.add_patch(poly)
#    plt.show()
    E = np.zeros([len(n_list), Nsite**2])
    l_list = [(x, y) for x in np.linspace(-m, m, Nsite) for y in np.linspace(-m, m, Nsite)]
        
    for i_n, n in enumerate(n_list):
        H = np.zeros([Nsite**2, Nsite**2])
        
        for i_1, ls_1 in enumerate(l_list):
            for i_2, ls_2 in enumerate(l_list):
                l_diff = np.array(ls_1) - np.array(ls_2)
                
                if (ls_1[0] == ls_2[0]) and (ls_1[1] == ls_2[1]):
                    H[i_1][i_2] = 3 * ((n[0] + ls_1[0])**2 + (n[1] + ls_1[1])**2 - (n[0] + ls_1[0]) * (n[1] + ls_1[1])) - 3 * s / 4
                            
                condition_1 = (int(np.abs(ls_1[0] - ls_2[0])) == 1) and (ls_1[1] == ls_2[1])
                condition_2 = (ls_1[0] == ls_2[0]) and (int(np.abs(ls_1[1] - ls_2[1])) == 1)
                condition_3 = ((l_diff[0] == 1) and (l_diff[1] == 1)) or ((l_diff[0] == -1) and (l_diff[1] == -1))
                
                if condition_1 or condition_2 or condition_3:
                    H[i_1][i_2] = - s / 4
                    
        E0, P = np.linalg.eig(H)
        rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
        
        for i in range(Nsite**2):
            E[i_n, i] = rearrangedEvalsVecs[i][0]
    #        P[:, i] = rearrangedEvalsVecs[i][1]
    
    dE_tmp = (E - E[0, 0]) * Er / h
    
    f_ex = np.append(f_ex, np.array([dE_tmp[0][3], dE_tmp[0][7]]))

f_ex = np.reshape(f_ex, [-1,2])

fig = plt.figure(dpi=150)
plt.rcParams["font.size"] = 12
plt.xlim(0, np.max(s_list))
plt.ylim(0, 100)

plt.xlabel('Lattice depth ($E_R$)')
plt.ylabel('Excitation frequency $f_{ex}$ (kHz)')
ax = plt.gca()
ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
plt.grid(lw=0.5, ls='--')
plt.plot(s_list, f_ex[:, 0]*1e-3, label='$1^{st}$')
plt.plot(s_list, f_ex[:, 1]*1e-3, '--', label='$3^{rd}$')
plt.legend()

plt.tight_layout()

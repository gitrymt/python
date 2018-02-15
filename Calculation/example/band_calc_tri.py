# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: Triangular optical lattice

Created on Thu Feb 15 20:37:38 2018
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import pandas as pd

# import user library
sys.path.append('../function')
#from func_band_calc import calcBand_1d

# Lattice depth V_lat = s Er
s = 1

# Calculation
m = 6
Nsite = 2 * m + 1

b1 = np.array([1, 0])
b2 = np.array([-1, -np.sqrt(3)])/2
b3 = np.array([-1, np.sqrt(3)])/2

p_Gamma = 0 * b1 + 0 * b2
p_M = 1/2 * b1 + 0 * b2
p_K = 1/3 * b1 - 1/3 * b2
fig = plt.figure()
ax = fig.add_subplot(111)
# 5点(0.1,0.1),(0.1,0.6),(0.7,0.8),(0.6,0.4),(0.6,0.1)を通る多角形を描画
poly = plt.Polygon((p_Gamma, p_M, p_K, p_Gamma),fc="#ff0000", alpha=0.5)
ax.add_patch(poly)
plt.show()


dn = 25

n_list = [(x, 0) for x in np.linspace(0, 1/2, int(dn * np.sqrt(3)))] # Gamma -> M
n_M = len(n_list) - 0.5

n_list = n_list + [(1/2 - x/6, -x/3) for x in np.linspace(0, 1, dn) if x>0] # M -> K
#n_K = len([(0.5, -x) for x in np.linspace(0, 1/3, dn)])
n_K = len(n_list) - 0.5

n_list = n_list + [(x/3, -x/3) for x in np.linspace(1, 0, dn*2) if x<1] # K -> Gamma
#n_Gamma = len([(x, -x) for x in np.linspace(1/3, 0, dn*2)])
n_Gamma = len(n_list)

l_list = [(x, y) for x in np.linspace(-m, m, Nsite) for y in np.linspace(-m, m, Nsite)]
E = np.zeros([len(n_list), Nsite**2])

list_emp = []
condition = pd.DataFrame([[list_emp, list_emp, list_emp,
                           False, False, False]],
                        columns = ["(l1, l2)", "(l1', l2')", "(l1-l1', l2-l2')",
                                   "Condition 1", "Condition 2", "Condition 3"
                                   ])

for i_n, n in enumerate(n_list):
    H = np.zeros([Nsite**2, Nsite**2])
    
    for i_1, ls_1 in enumerate(l_list):
        for i_2, ls_2 in enumerate(l_list):
            l_diff = np.array(ls_1) - np.array(ls_2)
            
            if (ls_1[0] == ls_2[0]) and (ls_1[1] == ls_2[1]):
                H[i_1][i_2] = 3 * ((n[0] + ls_1[0])**2 + (n[1] + ls_1[1])**2 - (n[0] + ls_1[0]) * (n[1] + ls_1[1])) - 3 * s / 4
            
#            if ((np.abs(ls_1[0] - ls_2[0]) == 1) and (ls_1[1] == ls_2[1])\
#                or ((ls_1[0] == ls_2[0]) and np.abs(ls_1[1] - ls_2[1]) == 1)\
#                or ((ls_1[0] - ls_2[0] == ls_1[1] - ls_2[1]) and (np.abs(ls_1[1] - ls_2[1]) == 1))):
            
            
            condition_1 = (int(np.abs(ls_1[0] - ls_2[0])) == 1) and (ls_1[1] == ls_2[1])
            condition_2 = (ls_1[0] == ls_2[0]) and (int(np.abs(ls_1[1] - ls_2[1])) == 1)
#            condition_3 = (int(ls_1[0] - ls_1[1]) == int(ls_2[0] - ls_2[1])) and (int(np.abs(ls_2[0] - ls_2[1])) == 1)
            condition_3 = ((l_diff[0] == 1) and (l_diff[1] == 1)) or ((l_diff[0] == -1) and (l_diff[1] == -1))
#            condition_1 = (np.abs(l_diff[0] == 1)) and (ls_1[1] == ls_2[1])
#            condition_2 = (np.abs(l_diff[1] == 1)) and (ls_1[0] == ls_2[0])
#            condition_3 = (l_diff[0] * l_diff[1]) == -1
            if condition_1 or condition_2 or condition_3:
                H[i_1][i_2] = - s / 4
                
                tmp = pd.DataFrame([[ls_1, ls_2, l_diff,
                                     condition_1, condition_2, condition_3]],
                            columns = ["(l1, l2)", "(l1', l2')", "(l1-l1', l2-l2')",
                                       "Condition 1", "Condition 2", "Condition 3"
                                       ])
                condition = condition.append(tmp)
            
    E0, P = np.linalg.eig(H)
    rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
    
    for i in range(Nsite**2):
        E[i_n, i] = rearrangedEvalsVecs[i][0]
#        P[:, i] = rearrangedEvalsVecs[i][1]


q = np.linspace(0, len(n_list), len(n_list))
plt.figure(dpi=200)
plt.plot(q, E[:, 0:4] - E[0, 0])
plt.grid(ls=':')
plt.ylabel('Energy ($E_R$)')
plt.xticks([0, n_M, n_K, n_Gamma], ['$\Gamma$', 'M', 'K', '$\Gamma$']) # xlocs：位置の配列　xlabels：ラベルの配列

# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: Triangular optical lattice

Created on Thu Feb 15 20:37:38 2018
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import axes3d
#from matplotlib import cm

import time

# import user library
sys.path.append('../function')
#from func_band_calc import calcBand_1d
import set_default_params

set_default_params.plot_params()

# Lattice depth V_lat = s Er
s = 1

# Calculation
m = 8
Nsite = 2 * m + 1

b1 = np.array([1, 0])
b2 = np.array([-1, -np.sqrt(3)])/2

dn = 25

n_list = [(x, 0) for x in np.linspace(0, 1/2, int(dn * np.sqrt(3)))] # Gamma -> M
n_M = len(n_list) - 0.5

n_list = n_list + [(1/2 - x/6, -x/3) for x in np.linspace(0, 1, dn) if x>0] # M -> K
n_K = len(n_list) - 0.5

n_list = n_list + [(x/3, -x/3) for x in np.linspace(1, 0, dn*2) if x<1] # K -> Gamma
n_Gamma = len(n_list)

l_list = [(x, y) for x in np.linspace(-m, m, Nsite, dtype=np.int) for y in np.linspace(-m, m, Nsite, dtype=np.int)]
E = np.zeros([len(n_list), Nsite**2])
C = np.zeros([Nsite**2, len(n_list), Nsite**2], dtype=np.complex)

H_tmp = np.zeros([Nsite**2, Nsite**2])

l1 = np.zeros([Nsite**2, Nsite**2])
m1 = np.zeros([Nsite**2, Nsite**2])
l2 = np.zeros([Nsite**2, Nsite**2])
m2 = np.zeros([Nsite**2, Nsite**2])

start = time.time()

for i_1, ls_1 in enumerate(l_list):
    for i_2, ls_2 in enumerate(l_list):
        l1[i_1][i_2] = ls_1[0]
        m1[i_1][i_2] = ls_1[1]
        l2[i_1][i_2] = ls_2[0]
        m2[i_1][i_2] = ls_2[1]
        
        l_diff = np.array(ls_1) - np.array(ls_2)
        
        condition_1 = (int(np.abs(ls_1[0] - ls_2[0])) == 1) and (ls_1[1] == ls_2[1])
        condition_2 = (ls_1[0] == ls_2[0]) and (int(np.abs(ls_1[1] - ls_2[1])) == 1)
        condition_3 = ((l_diff[0] == 1) and (l_diff[1] == 1)) or ((l_diff[0] == -1) and (l_diff[1] == -1))
        if condition_1 or condition_2 or condition_3:
            H_tmp[i_1][i_2] = - s / 4
        
for i_n, n in enumerate(n_list):
    H = np.zeros([Nsite**2, Nsite**2])
    H += H_tmp
    
    K = 3 * ((n[0] + l1)**2 + (n[1] + m1)**2 - (n[0] + l2) * (n[1] + m2)) - 3 * s / 4
#    H += ((np.abs(l1 - l2) < 1) * (np.abs(m1 - m2) < 1)) * K
    H += ((l1 == l2) * (m1 == m2)) * K
    
#    for i_1, ls_1 in enumerate(l_list):
#        for i_2, ls_2 in enumerate(l_list):
#            l_diff = np.array(ls_1) - np.array(ls_2)
#            
#            if (ls_1[0] == ls_2[0]) and (ls_1[1] == ls_2[1]):
#                H[i_1][i_2] = 3 * ((n[0] + ls_1[0])**2 + (n[1] + ls_1[1])**2 - (n[0] + ls_1[0]) * (n[1] + ls_1[1])) - 3 * s / 4
    
    E0, P = np.linalg.eig(H)
    rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
    
    E[i_n, :], tmp = map(list, zip(*rearrangedEvalsVecs))
    C[:, i_n, :] = np.array(tmp)

#    for i in range(Nsite**2):
#        E[i_n, i] = rearrangedEvalsVecs[i][0]
#        P[:, i] = rearrangedEvalsVecs[i][1]

elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

q = np.linspace(0, len(n_list), len(n_list))

plt.figure(dpi=200)
fig = plt.figure(dpi=100, figsize=[7, 5])
ax1 = fig.add_axes((0, 0, 0.7, 1))
ax2 = fig.add_axes((0.8, 0.4, 0.2, 0.2))

ax1.plot(q, E[:, :] - E[0, 0])
ax1.grid(ls=':')
ax1.set_ylabel('Energy ($E_R$)')
ax1.set_title('V = %.1f $E_R$' % s)
ax1.set_xticks([0, n_M, n_K, n_Gamma]) # xlocs：位置の配列　xlabels：ラベルの配列
ax1.set_xticklabels(['$\Gamma$', 'M', 'K', '$\Gamma$']) # xlocs：位置の配列　xlabels：ラベルの配列
ax1.set_xlim([0, np.max(q)])
ax1.set_ylim([-0.1, 5.1])

##ax1.plot(q, (E[:, :] - E[0, 0]) / omega)

# Draw Brillouin Zone
ax2.set_xlim([-1, 1])
ax2.set_ylim([-1, 1])
ax2.set_xticks([]) # xlocs：位置の配列　xlabels：ラベルの配列
ax2.set_yticks([]) # xlocs：位置の配列　xlabels：ラベルの配列
ax2.tick_params(labelbottom="off",bottom="off") # x軸の削除
ax2.tick_params(labelleft="off",left="off") # y軸の削除
ax2.axes.set_aspect('equal')
ax2.spines.clear() # Remove flame lines

## Hexiagonal BZ
poly = plt.Polygon([(np.cos(2 * np.pi * x/6 + np.pi/6), np.sin(2 * np.pi * x/6 + np.pi/6)) for x in np.linspace(0, 5, 6)], fill=False)
ax2.add_patch(poly)
ax2.plot([0, np.cos(2 * np.pi/12), np.cos(2 * np.pi/12), 0], [0, 0, np.sin(2 * np.pi/12), 0], 'b-')
ax2.text(-0.3, -0.25, '$\Gamma$')
ax2.text(1, -0.25, 'M')
ax2.text(1, 0.5, 'K')

#q_list = np.array(n_list)
#
#for i_q, q_pair in enumerate(q_list):
#    
#    if (q_pair[0] == 0) and (q_pair[1] == 0):
#        ms, ns = map(list, zip(*l_list))
#        ms = np.array(ms, dtype=np.float)
#        ns = np.array(ns, dtype=np.float)
#        
#        x = ms * b1[0] + ns * b2[0]
#        y = ms * b1[1] + ns * b2[1]
#        
#        fig, axs = plt.subplots(ncols=5, nrows=2, figsize=[16, 6], dpi=200, sharex=True, sharey=True)
#        plt.xlim([-3, 3])
#        plt.ylim([-3, 3])
##        plt.xlabel('$k_x$')
##        plt.ylabel('$k_y$')
#        axs = np.reshape(axs, [-1, ])
#        for k in range(10):
#            colors = np.zeros([C[0, 0, :].size, 3]) + [1, 0, 0]
#            Cs = C[k, i_q, :]
#            c_tmp = np.real(Cs / np.abs(Cs))
#            colors[c_tmp>0] = [0, 0, 1]
#            Cs = np.abs(C[k, i_q, :] / np.max(C[:, i_q, :]) * 50)
#            axs[k].scatter(x, y, s=Cs, c=colors, alpha=0.5)
#            plt.xticks([-2, -1, 0, 1, 2], ['$-2G$', '$-G$', '0', '$G$', '2G']) # xlocs：位置の配列　xlabels：ラベルの配列
#            plt.yticks([-2, -1, 0, 1, 2], ['$-2G$', '$-G$', '0', '$G$', '2G']) # xlocs：位置の配列　xlabels：ラベルの配列
#            axs[k].text(0.05, 0.85, r'$\left| \psi_{%d} \right>$' % (k+1),
#                    verticalalignment='bottom', horizontalalignment='left',
#                    transform=axs[k].transAxes,
#                    bbox={'facecolor':'white', 'alpha':0.5, 'pad':5})
#
#        fig.subplots_adjust(hspace=0, wspace=0)
##        plt.setp([a.get_xticklabels() for a in fig.axes[:-1]], visible=False)
#
##        plt.gca().set_aspect('equal', adjustable='box')
#
##        plt.savefig('k-space_%dEr.pdf' % s, dpi=400)
#        break

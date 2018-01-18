# -*- coding: utf-8 -*-
"""
Example for calculation of band structure: 2D optical lattice

Created on Wed Jan 17 21:40:11 2018
@author: gitrymt
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

# import user library
sys.path.append('../function')
#from func_band_calc import calcBand_1d

def calcBand_1d(s=1, Nsite=2*10, Nband=10, angle=np.pi):
    H = np.zeros([Nsite, Nsite])
    
    q = np.linspace(-1, 1, 101)
    E = np.zeros([q.size, Nsite])
    temp = np.eye(Nsite-1)
    
#    C = np.zeros([Nsite, q.size, Nsite])
    G = 2 * np.sin(angle / 2)
    
    for i_q in range(q.size):
        H = np.zeros([Nsite, Nsite])
        H[0:Nsite-1, 1:Nsite] += -s/4 * temp
        H[1:Nsite, 0:Nsite-1] += -s/4 * temp
        
        for i in range(Nsite):
            H[i][i] = G**2/4 * (2*(i-Nsite/2) + q[i_q])**2 + s/2
        
        E0, P = np.linalg.eig(H)
        rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
        
        for i in range(Nsite):
            E[i_q][i] = rearrangedEvalsVecs[i][0]
            P[:, i] = rearrangedEvalsVecs[i][1]
            
#        if Wannier_calc:
#            for k in range(Nsite):
#                for l in range(Nsite):
#                    C[k, i_q, l] = P[l, k]
    
    Energy = E.T
    
#    if Wannier_calc:
#        x0 = 0
#        x = np.linspace(-1, 1, 151)
#        Wannier = np.zeros([len(x), Nsite], dtype=np.complex)
#        u_q = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
#        phi = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
#        
#        for i_q, q_i in enumerate(q):
#            for i_x, x_i in enumerate(x):
#                for k in range (Nsite):
#                    for l in range(Nsite):
#                        u_q[i_q, i_x, k] += C[k, i_q, l] * np.exp(1j * 2 * np.pi * x_i * (-(Nsite-1)/2 - 1 + l))
#                    phi[i_q, i_x, k] = np.exp(1j * q_i * np.pi * x_i) * u_q[i_q, i_x, k]
#        
#        for i in range(Nsite):
#            phi[:, :, i] *= np.exp(-1j * np.angle(phi[:, x==0, i]))
#        
#        for i in range(Nsite):
#            for i_x, x_i in enumerate(x):
#                Wannier[i_x, i] = np.sum(phi[:, i_x, i] * np.exp(-1j * q * np.pi * x0), 0)
#            
#            norm_Wannier = (x[1] - x[0]) * np.sum(np.abs(Wannier[:, i])**2)
#            Wannier[:, i] = Wannier[:, i] / np.sqrt(norm_Wannier)
#            
#            if i % 2 == 1:
#                Wannier[:, i] = np.append(Wannier[int(len(x)/2):, i], Wannier[0:int(len(x)/2), i])
#        
#        return q, Energy, x, Wannier
#    else:
#        return q, Energy
    return q, Energy

# Lattice depth V_lat = s Er
s_short = 0
s_long = 50
s_diag = 0

# Calculation
Nsite = 9
tmp = np.arange(0, Nsite, 1)
l1_index, l2_index = np.meshgrid(tmp, tmp)
lx1_index = np.tile(l1_index,(Nsite,Nsite))
lx2_index = np.tile(l2_index,(Nsite,Nsite))
ly1_index = np.sort(lx1_index, axis=1)
ly2_index = np.sort(lx2_index, axis=0)

q0 = np.linspace(-2, 2, 61) * 2 * np.pi
qx, qy = np.meshgrid(q0, q0)
E = np.zeros([q0.size, q0.size, Nsite])
tmp_eye_x = np.eye(Nsite**2, dtype=np.complex)
tmp_eye_y = np.eye(Nsite, dtype=np.complex)

angle = np.pi
G = 2 * np.sin(angle / 2)

for i_qx in range(q0.size):
    for i_qy in range(q0.size):
        tmp = np.zeros([Nsite, Nsite], dtype=np.complex)
        H = np.zeros([Nsite**2, Nsite**2], dtype=np.complex)
        
        for n in range(Nsite):
            tmp[n, n] = (q0[i_qx] + 2*(n - Nsite/2))**2
#            H[n*Nsite:(n+1)*Nsite, n*Nsite:(n+1)*Nsite] += (qy[i_qy] + 2*(n - Nsite/2))**2
            H[n*Nsite:(n+1)*Nsite, n*Nsite:(n+1)*Nsite] += tmp_eye_y * (q0[i_qy] + 2*(n - Nsite/2))**2
#            for m in range(Nsite):
#                H[n*Nsite+m, n*Nsite+m] += (qy[i_qy] + 2*(m - Nsite/2))**2
#        H += np.tile(tmp,(Nsite,Nsite))
#        H += tmp_eye_x * (np.tile(tmp,(Nsite,Nsite)) + s_long + s_short + s_diag)
        H += tmp_eye_x * (np.tile(tmp,(Nsite,Nsite)) + s_long)
        
        H[np.abs(lx1_index - lx2_index) == 0] += s_long + s_short + s_diag
        H[np.abs(ly1_index - ly2_index) == 0] += s_long + s_short + s_diag
        H[np.abs(lx1_index - lx2_index) + np.abs(ly1_index - ly2_index) == 0] += s_long + s_short + s_diag
#        H[lx1_index - lx2_index == 1] += -s_long / 4
#        H[lx1_index - lx2_index == -1] += -s_long / 4
#        H[ly1_index - ly2_index == 1] += -s_long / 4
#        H[ly1_index - ly2_index == -1] += -s_long / 4
        H[np.abs(lx1_index - lx2_index) == 1] += -s_long / 4
        H[np.abs(ly1_index - ly2_index) == 1] += -s_long / 4
#        H[np.abs(lx1_index - lx2_index) == 2] += -s_short / 4
#        H[np.abs(ly1_index - ly2_index) == 2] += -s_short / 4
        index_tmp = ((lx1_index - lx2_index) == 1)
        index_tmp *= ((ly1_index - ly2_index) == -1)
#        H[((lx1_index - lx2_index) == 1) & ((ly1_index - ly2_index) == -1)] += - 1j * s_diag / 4
#        H[index_tmp] = - 1j * s_diag / 4
#        H[((lx1_index - lx2_index) == -1) & ((ly1_index - ly2_index) == 1)] = +1j * s_diag / 4
        
        E0, P = np.linalg.eig(H)
        E0 = np.abs(E0)
        rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
        for i in range(Nsite):
            E[i_qy, i_qx, i] = rearrangedEvalsVecs[i][0]

#        E[i_qy, i_qx, :] = np.real(E0[0:Nsite])
#        rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)

#        for n in range(Nsite):
#            H[n*Nsite, n*Nsite+1] += (qx[i_qx] + 2*(n - Nsite/2))**2 + (qy[i_qy] + 2*(m - Nsite/2))**2 + s_long + s_short + s_diag / 2
#            H[i][i] = (2*(i-Nsite/2) + qx[i_qx])**2 + s_long + s_short + s_diag / 2
#        print(i_qx, i_qy)

qx, qy = np.meshgrid(q0, q0)
#for i in range(Nsite):
for i in range(3):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(qx, qy, E[:,:,i], rstride=1, cstride=1, cmap=cm.coolwarm)

    fig = plt.figure(figsize=(6, 6))
    plt.imshow(E[:,:,i])

#q, Energy = calcBand_1d(s, angle=np.pi * 120 / 180)

# Plot calculation result
#fig = plt.figure(figsize=(6, 10))
#plt.rcParams["font.size"] = 14
#plt.hold(True)
#plt.xlim(-1, 1)
#plt.ylim(0, 15)
#
#plt.xlabel('$q$ ($d^{-1}$)')
#plt.ylabel('Energy $\epsilon_q$ ($E_R$)')
#ax = plt.gca()
#ax.yaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.xaxis.set_tick_params(which='both', direction='in',bottom=True, top=True, left=True, right=True)
#ax.set_xticklabels(["$-\pi$","$-\pi/2$","0","$\pi/2$","$\pi$"])
#ax.set_xticks(np.arange(-1, 1.5, 0.5))
#ax.set_title('Lattice depth $V_{lat} = $ ' + str('%.1f' % s) + ' $E_R$')
#for i in range(0, 5):
#    plt.plot(q, Energy[2*i, :], '-', linewidth=2)
#    plt.plot(q, Energy[2*i+1, :], '--', linewidth=2)
#
#plt.tight_layout()
#plt.show()

#plt.savefig('./hoge.pdf', dpi=200)

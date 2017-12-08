# -*- coding: utf-8 -*-
"""
Function library for calculation of band structure

Created on Tue Oct 31 16:01:07 2017
@author: gitrymt
"""

import numpy as np

### function: Band calculation - 1D optical lattice
def calcBand_1d(s=1, Nsite=2*10, Nband=10, Wannier_calc=False, angle=np.pi):
    H = np.zeros([Nsite, Nsite])
    
    q = np.linspace(-1, 1, 101)
    E = np.zeros([q.size, Nsite])
    temp = np.eye(Nsite-1)
    
    C = np.zeros([Nsite, q.size, Nsite])
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
            
        if Wannier_calc:
            for k in range(Nsite):
                for l in range(Nsite):
                    C[k, i_q, l] = P[l, k]
    
    Energy = E.T
    
    if Wannier_calc:
        x0 = 0
        x = np.linspace(-1, 1, 151)
        Wannier = np.zeros([len(x), Nsite], dtype=np.complex)
        u_q = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
        phi = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
        
        for i_q, q_i in enumerate(q):
            for i_x, x_i in enumerate(x):
                for k in range (Nsite):
                    for l in range(Nsite):
                        u_q[i_q, i_x, k] += C[k, i_q, l] * np.exp(1j * 2 * np.pi * x_i * (-(Nsite-1)/2 - 1 + l))
                    phi[i_q, i_x, k] = np.exp(1j * q_i * np.pi * x_i) * u_q[i_q, i_x, k]
        
        for i in range(Nsite):
            phi[:, :, i] *= np.exp(-1j * np.angle(phi[:, x==0, i]))
        
        for i in range(Nsite):
            for i_x, x_i in enumerate(x):
                Wannier[i_x, i] = np.sum(phi[:, i_x, i] * np.exp(-1j * q * np.pi * x0), 0)
            
            norm_Wannier = (x[1] - x[0]) * np.sum(np.abs(Wannier[:, i])**2)
            Wannier[:, i] = Wannier[:, i] / np.sqrt(norm_Wannier)
            
            if i % 2 == 1:
                Wannier[:, i] = np.append(Wannier[int(len(x)/2):, i], Wannier[0:int(len(x)/2), i])
        
        return q, Energy, x, Wannier
    else:
        return q, Energy
    
if __name__ == '__main__':
    print('')
# -*- coding: utf-8 -*-
"""
Function library for band calculation

Created on Tue Oct 31 16:01:07 2017
@author: gitrymt
"""

import numpy as np
import time

def calcBand_1d(s=1, Nsite=2*10, Nband=10, Wannier_calc=False, angle=np.pi):
    """
    Band calculation - 1D optical lattice

    Parameters
    ----------
    s : integer, optional
        Lattice potential depth normalized by recoil energy Er
        Here recoil energy Er is defined by hbar^2 k^2 / 2 m,
            & Lattice depth V_0 = 4 x U_0
    Nsite : integer, optional
        Site number for calculation

        For correct calculation, use even number
        e.g.) 2*10, which is default value
    Nband : integer, optional
        No use (current)
    Wannier_calc : bool, optional
        If True, calculate the Wannier function
    angle : float, optional
        Relative angle between lattice beams
        (the default is np.pi, which indicates that two lattice beams counter-propagate)
    
    """

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
        
        E[i_q, :], P = map(list, zip(*rearrangedEvalsVecs))
        C[:, i_q, :] = np.array(P)
    
    Energy = E.T
    
    if Wannier_calc:
        start = time.time()
        ltmp = (-(Nsite-1)/2 - 1 + np.array(range(Nsite)))
        
        x0 = 0
        x = np.linspace(-1, 1, 151)
        Wannier = np.zeros([len(x), Nsite], dtype=np.complex)
        u_q = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
        phi = np.zeros([len(q), len(x), Nsite], dtype=np.complex)
        
        for i_q, q_i in enumerate(q):
            for i_x, x_i in enumerate(x):
#                for k in range (Nsite):
#                    for l in range(Nsite):
#                        u_q[i_q, i_x, k] += C[k, i_q, l] * np.exp(1j * 2 * np.pi * x_i * (-(Nsite-1)/2 - 1 + l))
                    
#                    u_q[i_q, i_x, k] = np.sum(C[k, i_q, :] * np.exp(1j * 2 * np.pi * x_i * ltmp))
#                    phi[i_q, i_x, k] = np.exp(1j * q_i * np.pi * x_i) * u_q[i_q, i_x, k]
                u_q[i_q, i_x, :] = np.sum(C[:, i_q, :] * np.exp(1j * 2 * np.pi * x_i * ltmp), axis=1)
                phi[i_q, i_x, :] = np.exp(1j * q_i * np.pi * x_i) * u_q[i_q, i_x, :]
        
        elapsed_time = time.time() - start
        print("Wannier calc. elapsed_time (1 times): %.3f (sec.)" % (elapsed_time))

        for i in range(Nsite):
            phi[:, :, i] *= np.exp(-1j * np.angle(phi[:, x==0, i]))
        
        for i in range(Nsite):
            for i_x, x_i in enumerate(x):
                Wannier[i_x, i] = np.sum(phi[:, i_x, i] * np.exp(-1j * q * np.pi * x0), 0)
            
            norm_Wannier = (x[1] - x[0]) * np.sum(np.abs(Wannier[:, i])**2)
            Wannier[:, i] = Wannier[:, i] / np.sqrt(norm_Wannier)
            
            if i % 2 == 1:
                Wannier[:, i] = np.append(Wannier[int(len(x)/2):, i], Wannier[0:int(len(x)/2), i])
        
        return q, Energy, x, Wannier, C
    else:
        return q, Energy

def calcBand_tri(s=1, m=6, Nband=10, nq_list=[], Wannier_calc=False):
    """
    Band calculation - Triangular optical lattice

    Parameters
    ----------
    s : integer, optional
        Lattice potential depth normalized by recoil energy Er
        Here recoil energy Er is defined by hbar^2 k^2 / 2 m,
            & Lattice depth V_0 = 4 x U_0
    m : integer, optional
        Nsite = 2 * m + 1: Site number for calculation

        default is 6
    Nband : integer, optional
        No use (current)
    nq_list : list, optional
        wavenumber list
    Wannier_calc : bool, optional
        If True, calculate the Wannier function
    
    """

    # Calculation
    Nsite = 2 * m + 1
    
    if len(nq_list) < 1:
        dn = 10
        nq_list = [(x, 0) for x in np.linspace(0, 1/2, int(dn * np.sqrt(3)))] # Gamma -> M
        n_M = len(nq_list) - 0.5
        
        nq_list = nq_list + [(1/2 - x/6, -x/3) for x in np.linspace(0, 1, dn) if x>0] # M -> K
        n_K = len(nq_list) - 0.5
        
        nq_list = nq_list + [(x/3, -x/3) for x in np.linspace(1, 0, dn*2) if x<1] # K -> Gamma
        n_Gamma = len(nq_list)

    l_list = [(x, y) for x in np.linspace(-m, m, Nsite, dtype=np.int) for y in np.linspace(-m, m, Nsite, dtype=np.int)]
    E = np.zeros([len(nq_list), Nsite**2])
    C = np.zeros([Nsite**2, len(nq_list), Nsite**2])
    H_tmp = np.zeros([Nsite**2, Nsite**2])
    
    l1 = np.zeros([Nsite**2, Nsite**2])
    m1 = np.zeros([Nsite**2, Nsite**2])
    l2 = np.zeros([Nsite**2, Nsite**2])
    m2 = np.zeros([Nsite**2, Nsite**2])
    
#    start = time.time()
    
    for i_1, ls_1 in enumerate(l_list):
        for i_2, ls_2 in enumerate(l_list):
            l1[i_1][i_2] = ls_1[0]; m1[i_1][i_2] = ls_1[1]
            l2[i_1][i_2] = ls_2[0]; m2[i_1][i_2] = ls_2[1]
            
            l_diff = np.array(ls_1) - np.array(ls_2)
            
            condition_1 = (int(np.abs(ls_1[0] - ls_2[0])) == 1) and (ls_1[1] == ls_2[1])
            condition_2 = (ls_1[0] == ls_2[0]) and (int(np.abs(ls_1[1] - ls_2[1])) == 1)
            condition_3 = ((l_diff[0] == 1) and (l_diff[1] == 1)) or ((l_diff[0] == -1) and (l_diff[1] == -1))
            if condition_1 or condition_2 or condition_3:
                H_tmp[i_1][i_2] = - s / 4
            
    for i_n, n in enumerate(nq_list):
        H = np.zeros([Nsite**2, Nsite**2])
        H += H_tmp
        
        K = 3 * ((n[0] + l1)**2 + (n[1] + m1)**2 - (n[0] + l2) * (n[1] + m2)) - 3 * s / 4
    #    H += ((np.abs(l1 - l2) < 1) * (np.abs(m1 - m2) < 1)) * K
        H += ((l1 == l2) * (m1 == m2)) * K
        
        E0, P = np.linalg.eig(H)
        rearrangedEvalsVecs = sorted(zip(E0, P.T), key=lambda x: x[0].real, reverse=False)
        
        E[i_n, :], tmp = map(list, zip(*rearrangedEvalsVecs))
        C[:, i_n, :] = np.array(tmp)

    return E, C
#    elapsed_time = time.time() - start
#    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")


if __name__ == '__main__':
    print('')
    
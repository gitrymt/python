# -*- coding: utf-8 -*-
"""
Function library for calculation of band structure

Created on Tue Oct 31 16:01:07 2017

@author: gitrymt
"""

import numpy as np
import scipy as sp

### function: Band calculation - 1D optical lattice
def calcBand_1d(s=1, Nsite=2*10):
    H = np.zeros([Nsite, Nsite])
    
    q = np.linspace(-1, 1, 500)
    E = np.zeros([q.size, Nsite])
    temp = np.eye(Nsite-1)
    
    for i_q in range(q.size):
        H = np.zeros([Nsite, Nsite])
        H[0:Nsite-1, 1:Nsite] += -s/4 * temp
        H[1:Nsite, 0:Nsite-1] += -s/4 * temp
        
        for i in range(Nsite):
            H[i][i] = (2*(i-Nsite/2) + q[i_q])**2 + s/2
        
        E0, P = np.linalg.eig(H)
        E[:][i_q] = np.sort(E0)
    
    Nband = 5
    Eeven = np.zeros([Nband, q.size])
    Eodd = np.zeros([Nband, q.size])
    
    for i in range(Nband):
        Eeven[i][:] = E.T[2*i][:]
        Eodd[i][:] = E.T[2*i + 1][:]
    
    return q, Eeven, Eodd
            
if __name__ == '__main__':
    print('')
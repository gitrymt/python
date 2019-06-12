# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 21:48:36 2018

@author: RY
"""

import time
import sys

import numpy as np

class seq_array():
    def __init__(self, N):
        self.seq = np.zeros([N1, N2])
        
if __name__ == '__main__':
    Nseq = 1
    N1 = 64
    N2 = int(25e3 * 100)
    tmp = np.array([])
    
    for n in range(Nseq):
        print('%.2f MHz' % (N1 * N2 * 64 / 8 * 1e-6))
        tmp = np.append(tmp, seq_array([N1, N2]))
        time.sleep(1)
        print(n, sys.getsizeof(tmp[n].seq)*1e-6)
        tmp[n].seq[n] = 5
    
    for n in range(N1):
        for m in range(Nseq):
            tmp[m].seq[n, :] = (n/10)**2
        
    key = input('Please enter any key for exit program...')

    del tmp

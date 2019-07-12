# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:51:38 2019

@author: RY
"""

import numpy as np
import math
import matplotlib.pyplot as plt

from scipy import constants

mass = 87 * constants.m_u
wavelength = 1064e-9
Er = constants.h**2 / (2 * mass * wavelength**2)


n_mean = 1

p_n = []
n_list = np.linspace(0, 100, 101)
for n in n_list:
    p_n = np.append(p_n, n_mean**n * np.exp(-n_mean) / math.factorial(n))

plt.plot(1-(n_list+1) * Er / (constants.h * 100e3), p_n, 'o--')    

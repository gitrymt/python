# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 16:07:24 2019

@author: RY
"""

import numpy as np
from scipy import constants

Gamma_D2 = 2 * np.pi * 6.0666 * 1e6
Gamma_D1 = 2 * np.pi * 5.7500 * 1e6

delta_HFS = 2*np.pi * 6.834682610904 * 1e9

omega_D2 = 2*np.pi * 384.2304844685 * 1e12
omega_D1 = 2*np.pi * 377.107463380 * 1e12

omega = 2*np.pi * constants.c / 810e-9

mF1 = 1
mF2 = 2

delta_F = 2 * np.pi * np.array([2.563005979089109 * 1e9, -4.271676631815181 * 1e9]) # F=2, 1
delta_D2_F = 2 * np.pi * np.array([193.7407 * 1e6, -72.9112 * 1e6, -229.8518 * 1e6, -302.0738 * 1e6]) # F'=3, 2, 1, 0
delta_D1_F = 2 * np.pi * np.array([305.44 * 1e6, -509.06 * 1e6]) # F'=2, 1

#delta_D2_F = 2 * np.pi * np.array([0, 0, 0, 0]) # F'=3, 2, 1, 0
#delta_D1_F = 2 * np.pi * np.array([0, 0]) # F'=2, 1

if mF1 == 0:
    LS_F1_D2 = [0, -1/np.sqrt(6), 0, 1/np.sqrt(6)]
    LS_F1_D1 = [1/np.sqrt(3), 0]
elif np.abs(mF1) == 1:
    LS_F1_D2 = [0, -np.sqrt(1/8), np.sqrt(5/24), 0]
    LS_F1_D1 = [1/np.sqrt(4), -np.sqrt(1/12)]
    
if mF2 == 0:
    LS_F2_D2 = [-np.sqrt(3/10), 0, np.sqrt(1/30), 0]
    LS_F2_D1 = [0, np.sqrt(1/3)]
elif np.abs(mF2) == 1:
    LS_F2_D2 = [-np.sqrt(4/15), np.sqrt(1/24), np.sqrt(1/40), 0]
    LS_F2_D1 = [np.sqrt(1/12), np.sqrt(1/4)]
elif np.abs(mF2) == 2:
    LS_F2_D2 = [-1/np.sqrt(6), 1/np.sqrt(6), 0, 0]
    LS_F2_D1 = [np.sqrt(1/3), 0]
    

dE11 = 0
dE12 = 0
dE21 = 0
dE22 = 0

for i, delta_D2 in enumerate(delta_D2_F):
    delta1 = omega - (omega_D2 + delta_F[1] + delta_D2)
    tmp = LS_F1_D2[i]**2 / delta1
    tmp1 = 3 * np.pi * constants.c**2 * Gamma_D2 / (2 * omega_D2**3) * tmp
    dE12 += tmp1

    delta2 = omega - (omega_D2 + delta_F[0] + delta_D2)
    tmp = LS_F2_D2[i]**2 / delta2
    tmp2 = 3 * np.pi * constants.c**2 * Gamma_D2 / (2 * omega_D2**3) * tmp
    dE22 += tmp2
    print('F`=%d, D2: (F=1) %f THz, (F=2) %f THz' % (3-i, delta1 * 1e-12, delta2 * 1e-12))
    print('dE1 = %e, dE2 = %e' % (tmp1, tmp2))

print(dE12)
print(dE22)

for i, delta_D1 in enumerate(delta_D1_F):
    delta1 = omega - (omega_D1 + delta_F[1] + delta_D1)
    tmp = LS_F1_D1[i]**2 / delta1
    dE11 += 3 * np.pi * constants.c**2 * Gamma_D1 / (2 * omega_D1**3) * tmp

    delta2 = omega - (omega_D1 + delta_F[0] + delta_D1)
    tmp = LS_F2_D1[i]**2 / delta2
    dE21 += 3 * np.pi * constants.c**2 * Gamma_D1 / (2 * omega_D1**3) * tmp

    print('F`=%d, D1: (F=1) %f THz, (F=2) %f THz' % (2-i, delta1 * 1e-12, delta2 * 1e-12))

print(dE11)
print(dE21)

dE1 = dE11 + dE12
dE2 = dE21 + dE22

print((dE1 - dE2))
print('Polarizability (F=1): %e' % (dE1/constants.h))
print('Polarizability (F=2): %e' % (dE2/constants.h))

I0 = 2 * 350*1e-3 / (np.pi * (40*1e-6) * (110*1e-6)) # W/m^2
U0 = 4 * I0

alpha = (dE1 - dE2) / dE1
print('Differential light shift: %f kHz' %(250/4 * 1e-6 * constants.k / constants.h * alpha * 1e-3))
print((dE1 - dE2)*U0 / constants.h * 1e-3)

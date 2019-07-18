# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:01:53 2019

@author: RY
"""

import sys
import numpy as np
from scipy import constants
import matplotlib.pyplot as plt

# import user library
sys.path.append('../function')
from func_band_calc import calcBand_1d, calcBand_tri
import set_default_params

set_default_params.plot_params()

T = np.linspace(0, 100, 7501) # Temperature (uK)

mass = 87 * constants.m_u

dk_x = 4.01 * 1e6
dk_y = 0.41 * 1e6
dk_z = 3.21 * 1e6

dk = np.sqrt(dk_x**2 + dk_y**2 + dk_z**2)

sigma_x = np.sqrt(8 * constants.k * T * 1e-6 * np.log(2) / mass) / (2 * np.pi) * dk_x * 1e-3 # FWHM (kHz)
sigma_y = np.sqrt(8 * constants.k * T * 1e-6 * np.log(2) / mass) / (2 * np.pi) * dk_y * 1e-3 # FWHM (kHz)
sigma_z = np.sqrt(8 * constants.k * T * 1e-6 * np.log(2) / mass) / (2 * np.pi) * dk_z * 1e-3 # FWHM (kHz)
sigma = np.sqrt(8 * constants.k * T * 1e-6 * np.log(2) / mass) / (2 * np.pi) * dk * 1e-3 # FWHM (kHz)

plt.figure(dpi=125, figsize=(8,5))
plt.semilogx(T, sigma_x)
plt.semilogx(T, sigma_y)
plt.semilogx(T, sigma_z)
plt.semilogx(T, sigma)
plt.xlabel(r'Temperture ($\mu$K)')
plt.ylabel(r'FWHM (kHz)')
plt.xlim([1e-2, 100])
plt.ylim([0, 100])
plt.grid()
plt.legend(['X-axis',
            'Y-axis',
            'Z-axis',
            'Free particle'])

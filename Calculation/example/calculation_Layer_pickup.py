# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 14:29:47 2019

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

I = np.linspace(0, 10, 11)

dz = 2.575 # Layer separation (um)
dB = 2.63 * I * 1e-4 # G/um

df_base = 2 * 699.6 + 702.4 # kHz/G

df = df_base * dB * dz

plt.figure(dpi=125, figsize=(8,5))
plt.plot(I, df, c='#ff5555')
plt.xlabel('Coil current (A)')
plt.ylabel(r'$\Delta f/\Delta z$ (kHz)')
plt.xlim([0, 10])
plt.ylim([0, 15])
plt.grid()

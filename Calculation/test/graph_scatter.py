# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 05:29:48 2018

@author: gitrymt
"""
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../function')
import set_default_params

set_default_params.plot_params()


N = 20
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = np.pi * (15 * np.random.rand(N))**2 

fig = plt.figure(dpi=150)
plt.scatter(x, y, s=area, c=colors, alpha=0.5)

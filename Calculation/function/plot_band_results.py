# -*- coding: utf-8 -*-
"""
Function library for plot results of band calculation

Created on Fri Feb 23 23:44:06 2018
@author: gitrymt
"""
import numpy as np
import matplotlib.pyplot as plt

# Plot 1st Brillouin zone of triangular (hexagonal) lattice
def plotBrillouinZone_tri(cx=0, cy=0, L=1/np.sqrt(3), linecolor='k', arrowcolor='red', fontsize=10):
    PX = L * np.sqrt(3)
    
    plt.plot([cx-PX/2,cx-PX/2], [cy-L/2, cy+L/2], linecolor)
    plt.plot([cx+PX/2,cx+PX/2], [cy-L/2, cy+L/2], linecolor)
    plt.plot([cx-PX/2,cx], [cy+L/2, cy+L], linecolor)
    plt.plot([cx,cx+PX/2], [cy+L, cy+L/2], linecolor)
    plt.plot([cx-PX/2,cx], [cy-L/2, cy-L], linecolor)
    plt.plot([cx,cx+PX/2], [cy-L, cy-L/2], linecolor)
    
    # Plot high symmetry points (Gamma, M, and K)
    plt.quiver(cx, cy, PX/2, 0, scale_units='xy', scale=1, color=arrowcolor)
    plt.quiver(cx + PX/2, cy, 0, L/2, scale_units='xy', scale=1, color=arrowcolor)
    plt.quiver(cx + PX/2, cy + L/2, -PX/2, -L/2, scale_units='xy', scale=1, color=arrowcolor)
    plt.axes().set_aspect('equal', 'datalim')
    
    # Gamma point
    plt.plot(cx, cy, 'ok')
    tx_Gamma = '$\Gamma$'
    plt.text(cx - 0.2 * PX/2, cy, tx_Gamma, fontsize=fontsize)

    # M point
    plt.plot(cx + PX/2, cy, 'ok')
    tx_Gamma = 'M'
    plt.text(cx + PX/2 * (1 + 0.1), cy, tx_Gamma, fontsize=fontsize)

    # K point
    plt.plot(cx + PX/2, cy + L/2, 'ok')
    tx_K = 'K'
    plt.text(cx + PX/2 * (1 + 0.1), cy + L/2, tx_K, fontsize=fontsize)
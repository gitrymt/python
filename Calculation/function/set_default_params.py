# -*- coding: utf-8 -*-
"""
Function library for setting default parameters

Created on Sat Feb 24 13:37:11 2018
@author: gitrymt
"""
import matplotlib.pyplot as plt

def plot_params():
    # figure parameters
    # https://matplotlib.org/users/customizing.html
    plt.rcParams["font.size"] = 14
    plt.rcParams['xtick.direction'] = 'in' # direction: in, out, or inout
    plt.rcParams['ytick.direction'] = 'in' # direction: in, out, or inout
    plt.rcParams['axes.linewidth'] = 1.5 # edge linewidth
    plt.rcParams['xtick.major.size'] = 8 # major tick size in points
    plt.rcParams['xtick.major.width'] = 1.5 # major tick width in points
    plt.rcParams['xtick.top'] = True # draw ticks on the top side
    plt.rcParams['ytick.major.size'] = 8 # major tick size in points
    plt.rcParams['ytick.major.width'] = 1.5 # major tick width in points
    plt.rcParams['ytick.right'] = True # draw ticks on the right side
    

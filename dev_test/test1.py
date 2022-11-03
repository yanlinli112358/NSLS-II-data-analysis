#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 14:37:47 2022

@author: Rachel

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.stats.mstats import chisquare

#def gaussian function for fitting
def gaussian(x, A, sig, miu):

    y = A * np.exp(-1 * (x-miu)**2 / (2 * sig**2))
    return y

#def polynomial background
def bkg(x, *coeffs):
    n = 0
    y = 0
    while n < len(coeffs):
        y += coeffs[n] * np.power(x, n)
        n += 1
    return y


def signal_fit(x, num_peaks, bkg_order, *paras):
    s = "def signal_total(x"
                  
    var_n = 0
    while var_n <= (num_peaks*3 + bkg_order):
        s += ", " 
        s += "v"+str(var_n)
        var_n += 1
    s += '): \n'
    s += "    y = bkg(x"
    bkg_n = 0
    while bkg_n <= bkg_order: 
        s += ','
        s += 'v' + str(bkg_n)
        bkg_n +=1
    s += ') \n'
    s += '    print(y)\n'

    n = 0
    while n < num_peaks:
        s += "    y += gaussian(x "        
        s += ','
        s += 'v' + str(bkg_order + 1 + n*3) + ', v' + str(bkg_order + 2 + n*3) + ', v' + str(bkg_order + 3 + n*3)
        s += ')\n'
        s += '    print(y)\n'
        n += 1
    
    s += \
    "    return y"
    print(s)
    exec(s, globals())
    
    s2 = "y = signal_total(x"
    for p in paras:
        s2+= ','
        s2 += str(p)
    s2 += ') \n'
    print(s2)
    exec(s2, globals())
    
    print(y)
    return y

x = np.array([1, 2, 4, 5])
y = signal_fit(x, 2, 1, 2.0, 4.0, 2.0, 4., 5., 5., 5., 5.)

plt.plot(x, y)
plt.show()

p0_list = []
countb = 0
bkg_order = 1
num_peaks = 2
peak_centers = [3920, 4250]
while countb <= bkg_order:
    p0_list.append(0)
    countb += 1
countg = 0
while countg < num_peaks:
    p0_list.append(50)
    p0_list.append(100)
    p0_list.append(peak_centers[countg])
    countg += 1
print("p0 = " + str(p0_list))
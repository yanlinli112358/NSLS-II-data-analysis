#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:37:09 2022

@author: Rachel
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.append('../')
from utils.input_output import get_data

#specify path
os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip')

#inputs
##file reading and writing directory
file = 's2_2'
filename = 'fluo_data/' + file + '.csv'
savename = 'fluo_data_extracted/' + file + '_flu.txt'
##low_e , high_e : energy range of interest
low_e = 11500
high_e = 12200
##define fitting parameters for the peak
num_peaks = 1
bkg_order = 1
peak_centers = [11920]


# produce the total photon counts in the full spectra
total_I = get_data(filename, 10, 40950)[1]
total_counts = sum(sum(filter(lambda x: x>3, i)) for i in total_I)
print('totanumber of photon recieved by the detector is ' + str(int(total_counts)))


#def gaussian function for fitting
def gaussian(x, A, sig, miu):
    y = A * np.exp(-1 * (x-miu)**2 / (2 * sig**2))
    return y

#def polynomial background
def bkg(x, *coeffs):
    n = 0
    y = 0
    while n < len(coeffs):
        y += coeffs[n] * x**n
        n += 1
    return y


#def error processing
def r_square(x, fit_x):
    mean = np.sum(x)/len(x)
    ss_res = np.sum((x-fit_x)**2)
    ss_tot = np.sum((x - mean)**2)
    r_square = 1 - ss_res/ss_tot
    return r_square



#def sum of peaks and curves   
def signal_fit(x, y, num_peaks, bkg_order, peak_centers):
    #transform the function to a function with fixed number of parameters
    s = "def signal_total(x"
                  
    var_n = 0
    while var_n <= (num_peaks * 3 + bkg_order):
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

    n = 0
    while n < num_peaks:
        s += "    y += gaussian(x "        
        s += ','
        s += 'v' + str(bkg_order + 1 + n*3) + ', v' + str(bkg_order + 2 + n*3) + ', v' + str(bkg_order + 3 + n*3)
        s += ')\n'
        n += 1
    
    s += \
    "    return y"
    #print(s)
    exec(s, globals())
    
    #curve fit the transformed function 'signal_total'
    ##determine initial guess and bounds
    maxy = max(y)
    p0_list = []

    countb = 0
    while countb <= bkg_order:
        p0_list.append(0)
        countb += 1
    countg = 0
    while countg < num_peaks:
        p0_list.append(maxy)
        p0_list.append(100)
        p0_list.append(peak_centers[countg])
        countg += 1


    ##fit
    para, pcov = curve_fit(signal_total, x, y, p0 = p0_list)
    bkg_return = para[0: bkg_order + 1]
    gaussian_return = para[bkg_order + 1:]
    
    # print('background parameters = ' + str(bkg_return))
    # print('gaussian parameters = ' + str(gaussian_return))
    
    #calculate integrated intensity and error
    A1 = gaussian_return[0]
    sig1 = gaussian_return[1]
    intg_I = A1 * sig1

    A1_err = pcov[bkg_order + 1, bkg_order + 1]
    sig1_err = pcov[bkg_order + 2, bkg_order + 2]
    A1_sig1 = pcov[bkg_order + 1, bkg_order + 2]
    err = np.sqrt(abs(A1_err) / A1 ** 2 + abs(sig1_err) / sig1 ** 2 + 2 / sig1 / A1 * np.sqrt(abs(A1_sig1))) * intg_I

    #plot data
    plt.scatter(x,y)
    #plot fit
    s2 = "fit_y = signal_total(x" 
    for p in para:
        s2 += ','
        s2 += str(p)
    s2+= ')\n'
    exec(s2, globals())
    
    plt.plot(x, fit_y)
    #return
    return (intg_I, err)


#plot the spectra
x = np.linspace(low_e, high_e, (high_e - low_e)//10 + 1)
Qz, I =  get_data(filename, low_e, high_e)
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in I:
    plt.scatter(x, y, linewidths= 0.2)
plt.show()


#plot the full spectra
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in total_I:
    plt.scatter(np.linspace(10, 15000, len(y)), y, linewidths= 0.2)
plt.show()


##integrate intensity, plot I vs energy and fitted curve
plt.figure()
plt.ylabel('Intensity')
plt.xlabel('Energy (eV)')


integrated_I = []
err_I = []
width = []

plt.figure()
plt.title(filename + '_fit')
for y in I:
    y = np.array(y)
    integrated_I_value, err_I_value = signal_fit(x, y, num_peaks, bkg_order, peak_centers)
    integrated_I.append(integrated_I_value)
    err_I.append(err_I_value)
plt.show()


#plot integrated intensity vs Qz    
#print(integrated_I)
#print(err_I)
plt.figure()
plt.errorbar(Qz, integrated_I, yerr = err_I, fmt = "o")
plt.title(file)
plt.ylabel('Intensity')
plt.xlabel('Qz')
plt.show()

#write data into file
f = open(savename, 'w')
for i in range(len(integrated_I)):
    line = str(Qz[i]) + ' ' + str(integrated_I[i]) + ' ' + str(err_I[i])
    f.writelines(line)
    f.write('\n')
f.close()


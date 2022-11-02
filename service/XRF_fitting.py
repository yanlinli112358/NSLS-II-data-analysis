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
from utils.input_output import get_all_data
from utils.input_output import get_qz
from utils.fit_functions import signal_fit

#specify path
os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip_shared')

#inputs
##file reading and writing directory
file = 's2_10mMKBr_2-b3aa2f9a-1199-4a3d-b9af-e05292c50c70'
#filename = 'fluo_data/' + file + '.txt'
filename = 'fluo_data_all/' + file + '.txt'
Qz_name = 'fluo_data_all/Qz-' + file + '.txt'
savename = 'fluo_data_extracted/' + file + '_flu.txt'
##low_e , high_e : energy range of interest
low_e = 11500
high_e = 12200
##define fitting parameters for the peak
num_peaks = 1
bkg_order = 1
peak_centers = [11920]
scale_factor = 2500000.

# produce the total photon counts in the full spectra
total_I = get_all_data(filename, 10, 40950)
total_counts = sum(sum(filter(lambda x: x>3, i)) for i in total_I)
print('totanumber of photon recieved by the detector is ' + str(int(total_counts)))

#plot the spectra
x = np.linspace(low_e, high_e, (high_e - low_e)//10 + 1)
I = np.array(get_all_data(filename, low_e, high_e))/scale_factor
# if len(I) == 17:
#     Qz = get_qz('fluo_data/Qz_17.txt')
# else:
#     Qz = get_qz('fluo_data/Qz.txt')
Qz = get_qz(Qz_name)
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in I:
    plt.scatter(x, y/scale_factor, linewidths= 0.2)
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
plt.title('data vs fit')
for y in I:
    y = np.array(y)
    x = np.array(x)
    integrated_I_value, err_I_value = signal_fit(x, y, num_peaks, bkg_order, peak_centers)
    integrated_I.append(integrated_I_value)
    err_I.append(err_I_value)
plt.show()


print(len(integrated_I))
print(len(err_I))
print(len(Qz))

#plot integrated intensity vs Qz    
#print(integrated_I)
#print(err_I)
plt.figure()
plt.errorbar(Qz, integrated_I, yerr = err_I, fmt = "o")
plt.title(file + ' integrated intensity')
plt.ylabel('Intensity')
plt.xlabel('Qz')
plt.savefig('fluo_plots/' + file)
plt.show()


#write data into file
f = open(savename, 'w')
for i in range(len(integrated_I)):
    line = str(Qz[i]) + ' ' + str(integrated_I[i]) + ' ' + str(err_I[i])
    f.writelines(line)
    f.write('\n')
f.close()


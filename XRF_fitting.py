#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 13:37:09 2022

@author: Rachel
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import quad
from scipy.stats.mstats import chisquare

#inputs
file = 's21_1'
filename = 'fluo_data/' + file + '.csv'
savename = 'fluo_data_extrated/' + file + '_flu.txt'
low_e = 3600
high_e = 4100
peak_center = 3920

#low_e , high_e : energy range of interest
def get_data(filename, low_e, high_e):
    Qz = []
    I = []
    f = open(filename, 'r')
    line = f.readline()
    line = f.readline()
    while(line):
        data = line.split(',')
        Qz.append(float(data[0]))
        y = [float(x) for x in data[low_e//10 : high_e//10 + 1]] # list of intensities in the range of interest
        I.append(y) # I = 2D array of energies = energies each Qz
        line = f.readline()
    f.close()
    return Qz, I


# produce the total photon counts in the full spectra
total_I = get_data(filename, 10, 40950)[1]
total_counts = sum(sum(filter(lambda x: x>3, i)) for i in total_I)
print('totanumber of photon recieved by the detector is ' + str(int(total_counts)))


#def gaussian function for fitting
def gaussian(x, A, sig, miu, b):
    y = A * np.exp(-1 * (x-miu)**2 / (2 * sig**2)) + b
    return y


#plot the spectra
x = np.linspace(low_e, high_e, (high_e - low_e)//10 + 1)
Qz, I =  get_data(filename, low_e, high_e)
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in I:
    plt.scatter(x, y, linewidths= 0.2)


#plot the full spectra
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in total_I:
    plt.scatter(np.linspace(10, 15000, len(y)), y, linewidths= 0.2)

'''
y = I[5]
print(y)
para, cov = curve_fit(gaussian, x, y, p0 = [2000, 100, 12000])
print(para)
A = para[0]
sig = para[1]
miu = para[2]
print(A, sig, miu)
fit_y = gaussian(x, A, sig, miu)

plt.scatter(x,y)
plt.plot(x, fit_y)
print(quad(gaussian, low_e, high_e, args = (A, sig, miu)))

'''
def r_square(x, fit_x):
    mean = np.sum(x)/len(x)
    ss_res = np.sum((x-fit_x)**2)
    ss_tot = np.sum((x - mean)**2)
    r_square = 1 - ss_res/ss_tot
    return r_square

##integrate intensity, plot I vs energy and fitted curve
plt.figure()
plt.ylabel('Intensity')
plt.xlabel('Energy (eV)')

integrated_I = []
err_I = []
width = []
for y in I:
    y = np.array(y)
    maxy = max(y)
    para_bounds = ([0, 0, peak_center - 50, 0], [maxy, 400, peak_center + 50, maxy])
    para, pcov = curve_fit(gaussian, x, y, p0 = [maxy, 100, peak_center, 0], bounds = para_bounds) ##fit
    print(para)
    width.append(para[1])
    A = para[0]
    sig = para[1]
    miu = para[2]
    b = para[3]
    fit_y = gaussian(x, A, sig, miu, b)
    r2 = r_square(y, fit_y)
    print(r2)
    plt.scatter(x, y, linewidths=0.5)
    plt.plot(x, fit_y)
    intg_I = A * sig #integrate
    err = np.sqrt(abs(pcov[0, 0])/A**2 +  abs(pcov[1, 1])/sig**2 + 2 / sig / A * np.sqrt(abs(pcov[0,1]))) * intg_I
    integrated_I.append(intg_I)
    err_I.append(err)

#plot Qz vs width
plt.figure()
plt.scatter(Qz, width)
plt.title('peak width vs Qz')
plt.ylabel('peak width (eV)')
plt.xlabel('Qz(A^-1)')
plt.plot(Qz, [sum(width)/len(width)] * len(width), color = 'orange')
plt.text(0.06,75, 'total counts \n = ' + str(total_counts), bbox=dict(facecolor='orange', alpha=0.5))


#plot integrated intensity vs Qz    
print(integrated_I)
print(err_I)
plt.figure()
plt.errorbar(Qz, integrated_I, yerr = err_I, fmt = "o")
plt.title(file)
plt.ylabel('Intensity')
plt.xlabel('Qz')

#write data into file
f = open(savename, 'w')
for i in range(len(integrated_I)):
    line = str(Qz[i]) + ' ' + str(integrated_I[i]) + ' ' + str(err_I[i])
    f.writelines(line)
    f.write('\n')
f.close()


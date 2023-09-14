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
path = '/Users/rachel/NSLS_II_beamtrips/2023_7_trip_shared/XRF_data'
os.chdir(path)

#inputs
##file reading and writing directory
file = 'Fluo_data_col[energies]_rows[qz]-0P2mM_KCl_ODA-dfebdd20'
filename = file + '.csv'
#filename = 'XRF_data 2/' + file + '.csv'
#Qz_name = 'fluo_data_all/Qz-' + file + '.txt'
savename = 'fluo_data_extracted/' + file + '_flu.txt'

bkg_filename = 'Fluo_data_col[energies]_rows[qz]-0P2mM_KI_ODA-eb22d955' + '.csv'

#create the fluo_data_extracted folder
print(os.getcwd())
folder_name = "fluo_data_extracted"

# Check if the directory exists
if not os.path.exists(folder_name):
    # Create the directory
    os.mkdir(folder_name)
    print("Folder created successfully.")
else:
    print("Folder already exists.")
#initialize empty variables for the dictionary
low_e = 0
high_e = 0
num_peaks = 0
peak_centers = []

#common varibles thats not specific to elements
bkg_order = 2
scale_factor = 5000000.
from utils.xray_database import spectrum_dict

# Loop through the keys in the spectrum_dict
for key in spectrum_dict.keys():
    # If the filename contains the key, set the variables accordingly
    if key in filename:
        peak_centers = spectrum_dict[key]['peak_centers']
        high_e = spectrum_dict[key]['high_e']
        low_e = spectrum_dict[key]['low_e']
        num_peaks = spectrum_dict[key]['num_peaks']
        # Break the loop once the key is found
        break

# Print the variables for testing
print(peak_centers)
print(high_e)
print(low_e)
print(num_peaks)

# produce the total photon counts in the full spectra
total_I = get_data(filename, 10, 40950)[1]
total_counts = sum(sum(filter(lambda x: x>3, i)) for i in total_I)
print('totanumber of photon recieved by the detector is ' + str(int(total_counts)))

#plot the spectra
x = np.linspace(low_e, high_e, (high_e - low_e)//10 + 1)
Qz = np.array(get_data(filename, low_e, high_e)[0])
I = np.array(get_data(filename, low_e, high_e)[1])
# if len(I) == 17:
#     Qz = get_qz('fluo_data/Qz_17.txt')
# else:
#     Qz = get_qz('fluo_data/Qz.txt')
plt.figure()
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')

colors = plt.cm.viridis(np.linspace(0, 0.9, len(Qz)))
i = 0
for y in I:
    plt.scatter(x, y/scale_factor, color = colors[i], linewidths= 0.2, label = 'Qz = ' + str(round(Qz[i], 2)))
    i += 1
plt.legend()
plt.show()


#plot the full spectra
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in total_I:
    plt.scatter(np.linspace(10, 40950, len(y)), y, linewidths= 0.2)
plt.title('full spectra')
plt.show()


##integrate intensity, plot I vs energy and fitted curve
integrated_I = []
err_I = []
width = []
for y in I:
    y = np.array(y)
    x = np.array(x)
    integrated_I_value, err_I_value = signal_fit(x, y, num_peaks, bkg_order, peak_centers)
    integrated_I.append(integrated_I_value/scale_factor)
    err_I.append(err_I_value/scale_factor)

print(integrated_I)

#plot integrated intensity vs Qz    
#print(integrated_I)
#print(err_I)
plt.figure()
plt.errorbar(Qz, integrated_I, yerr = err_I, fmt = "o")
plt.title(file + ' integrated intensity')
plt.ylabel('Intensity')
plt.xlabel('Qz')
#plt.savefig('XF_plots/' + file)
plt.show()


#write data into file
def save_XF(savename, intensity_set, err_set):
    f = open(savename, 'w')
    for i in range(len(integrated_I)):
        line = str(Qz[i]) + ' ' + str(intensity_set[i]) + ' ' + str(err_set[i])
        f.writelines(line)
        f.write('\n')
    f.close()
    return None

save_XF(savename, integrated_I, err_I)

#plot the total counts versus Q
from utils.input_output import get_total_counts
total_counts_list = get_total_counts(filename)
plt.figure()
plt.scatter(Qz, total_counts_list)
plt.title('total number of counts received by detector at each Qz')
plt.show()

#instead of fittng through gaussian, sum total counts over a range
#energy to find the integrated intensity
from utils.fit_functions import total_counts_in_range
Qz, totalcounts_in_range = total_counts_in_range(filename, low_e, high_e)
Qz, bkg_total_counts = total_counts_in_range(bkg_filename, low_e, high_e)
totalcounts_no_bkg = (np.array(totalcounts_in_range) - np.array(bkg_total_counts))
err_totalcounts = np.sqrt(totalcounts_no_bkg)
savename_sum = 'fluo_data_extracted_sum/' + file + '_flu.txt'


if not os.path.exists('fluo_data_extracted_sum'):
    # Create the directory
    os.mkdir('fluo_data_extracted_sum')
    print("Folder created successfully.")
else:
    print("Folder already exists.")
save_XF(savename_sum, totalcounts_no_bkg, err_totalcounts)


totalcounts_no_bkg = np.array(totalcounts_in_range) - np.array(bkg_total_counts)

plt.scatter(Qz, np.array(totalcounts_in_range)/scale_factor*1.5, c='red', label = 'sum')
plt.errorbar(Qz, totalcounts_no_bkg/scale_factor*1.5, yerr= err_totalcounts/scale_factor*1.5, fmt = 'o',
             c = 'green', label = 'sum_no_bkg')
plt.errorbar(Qz, integrated_I, yerr = err_I, fmt = "o", label = 'gausssian')
plt.title('temp_compare')
plt.legend()
plt.savefig('temp.jpg')
plt.show()

# #filter the periodic noise out of the signal
# from utils.fit_functions import apply_filter
# cutoff_freq = 180
# sampling_freq = 1000
# filtered_intI = apply_filter(integrated_I, cutoff_freq, sampling_freq, filter_order=5)

# #plot the original data and fitted data on the same plot
# plt.figure()
# plt.scatter(Qz, integrated_I, color = 'b', label = 'original intensity')
# plt.scatter(Qz, filtered_intI, color = 'r', label = 'filtered intensity')
# plt.title(file + ' integrated intensity')
# plt.ylabel('Intensity')
# plt.xlabel('Qz')
# plt.legend()
# plt.show()

#save the filtered data into file

# f = open('fluo_data_extracted/' + file + 'filtered_flu.txt', 'w')
# for i in range(len(integrated_I)):
#     line = str(Qz[i]) + ' ' + str(filtered_intI[i]) + ' ' + str(err_I[i])
#     f.writelines(line)
#     f.write('\n')
# f.close()

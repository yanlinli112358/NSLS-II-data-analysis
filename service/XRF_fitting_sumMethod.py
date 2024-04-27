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
path = '/Users/rachel/NSLS_II_beamtrips/2024_4_trip_final/XRF_data'
os.chdir(path)

#inputs
##file reading and writing directory
file = 's42_ODG_KClO4_pH9-1dab4d4b'
filename = file + '.csv'
element_of_interest = ['direct_beam_14.4']
#bkg_filename = 's7_ODA_0p5mM_KI-a34fc0fd' + '.csv'
bkg_filename = 's4_ODG_water-95f81ad1' + '.csv'
scale_factor = 500000

#create the fluo_data_extracted folder
print(os.getcwd())
folder_name = "fluo_data_extracted_sum"

# Check if the directory exists
if not os.path.exists(folder_name):
    # Create the directory
    os.mkdir(folder_name)
    print("Folder created successfully.")
else:
    print("Folder already exists.")

##general purpose plotting
# produce the total photon counts in the full spectra
total_I = get_data(filename, 10, 40950)[1]
total_counts = sum(sum(filter(lambda x: x>3, i)) for i in total_I)
print('totanumber of photon recieved by the detector is ' + str(int(total_counts)))
#plot the full spectra
plt.ylabel('Intensity (counts)')
plt.xlabel('Energy (eV)')
for y in total_I:
    plt.scatter(np.linspace(10, 40950, len(y)), y, linewidths= 0.2)
plt.title('full spectra')
plt.show()



#element specific fitting and plotting
#initialize empty variables for the dictionary
low_e = 0
high_e = 0
num_peaks = 0
peak_centers = []

from utils.xray_database import spectrum_dict
# Loop through the keys in the spectrum_dict
for key in element_of_interest:
    # If the filename contains the key, set the variables accordingly
    if key in filename:
        #define variables unique to the key element
        peak_centers = spectrum_dict[key]['peak_centers']
        high_e = spectrum_dict[key]['high_e']
        low_e = spectrum_dict[key]['low_e']
        num_peaks = spectrum_dict[key]['num_peaks']

        element_unique_paras = [peak_centers, high_e, low_e, num_peaks]
        #read data of the element peaks from file
        energies = np.linspace(low_e, high_e, (high_e - low_e) // 10 + 1)
        Qz = np.array(get_data(filename, low_e, high_e)[0])
        I = np.array(get_data(filename, low_e, high_e)[1])

        #read the background data
        Qz_bkg = np.array(get_data(bkg_filename, low_e, high_e)[0])
        I_bkg = np.array(get_data(bkg_filename, low_e, high_e)[1])

        if np.array_equal(Qz, Qz_bkg) == False:
            print('Qz does not match between data and bkg')
            break

        plt.figure()
        for i in range(len(I)):
            plt.plot(energies, I_bkg[i], color='darkblue')
            plt.plot(energies, I[i], color = 'darkred')
            plt.title('focused spectra')
            plt.xlabel('energies (eV)')
            plt.ylabel('counts')
        plt.show()

        #fit by summing over all counts in a range
        from utils.fit_functions import signal_fit_sum
        intg_intensity_list = np.array(signal_fit_sum(I, I_bkg, energies, Qz, low_e, high_e)[1])/scale_factor
        plt.scatter(Qz, intg_intensity_list)
        plt.show()

        # write integrated intensities into file
        err_I = np.zeros(len(intg_intensity_list))
        from utils.input_output import save_XF
        savename = 'fluo_data_extracted_sum/' + file + '-' + key + '_flu.txt'
        save_XF(savename, Qz, intg_intensity_list, err_I)


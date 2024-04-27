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
file = 's5_ODA_1mM_KBr_pH4-bbde2f77'
filename = file + '.csv'
element_of_interest = ['Br']
#filename = 'XRF_data 2/' + file + '.csv'
#Qz_name = 'fluo_data_all/Qz-' + file + '.txt'
savename = 'fluo_data_extracted/' + file + '_flu.txt'
#bkg_filename = 's40_0p4mM_KI_ODA-96007c00' + '.csv'
bkg_filename = 's1_water_ODA-dd27128a' + '.csv'

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
# #plot the total counts versus Q
# from utils.input_output import get_total_counts
# total_counts_list = get_total_counts(filename)
# plt.figure()
# plt.scatter(Qz, total_counts_list)
# plt.title('total number of counts received by detector at each Qz')
# plt.show()


#element specific fitting and plotting
#initialize empty variables for the dictionary
low_e = 0
high_e = 0
num_peaks = 0
peak_centers = []

#common varibles thats not specific to elements
bkg_order = 2
scale_factor = 5000000.
#scale_factor = 1
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
        x = np.linspace(low_e, high_e, (high_e - low_e) // 10 + 1)
        Qz = np.array(get_data(filename, low_e, high_e)[0])
        I = np.array(get_data(filename, low_e, high_e)[1])

        #plot the spectrum of the element peaks
        from utils.plot_functions import plot_spec
        plot_spec(filename, low_e, high_e, scale_factor)
        plt.show()
        #integrate the intensity (fit by gaussian) through the peaks
        from utils.fit_functions import integrated_intensity
        integrated_I, err_I, width = integrated_intensity(filename, scale_factor, bkg_order, element_unique_paras)
        from utils.plot_functions import plot_integrated_I
        plot_integrated_I(Qz, integrated_I, err_I, file)
        plt.show()

        #write integrated intensities into file
        from utils.input_output import save_XF
        savename = 'fluo_data_extracted/' + file + '-' + key + '_flu.txt'
        #savename = '/Users/rachel/NU research/March Meeting 2024/20mM KI intg.txt'
        save_XF(savename, Qz, integrated_I, err_I)

        # Break the loop once the key is found
        #break

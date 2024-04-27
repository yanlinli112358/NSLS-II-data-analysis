import os
import sys
import numpy as np
import matplotlib.pyplot as plt

from utils.input_output import get_data
#specify path
path = '/Users/rachel/NSLS_II_beamtrips/2023_10_during_trip/XRF_data'
os.chdir(path)

file = 'Fluo_data_col[energies]_rows[qz]-s3_20mM_KCl_only_XFonly-42b805b1'
filename = file + '.csv'

#energy_bonds
low_e = 2200
high_e = 3000

#create a folder for to store I vs energy at each Qz for this specific file
save_folder = '0p4mM_KCl'
#check if the folder exists, if not, create one
isExist = os.path.exists(save_folder)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(save_folder)
   print("The new directory is created!")

def write_peak_curves(save_path, energy_list, I):
    f = open(save_path, 'w')
    for i in range(len(energy_list)):
        line = str('{}\t{}\n'.format(energy_list[i], I[i]))
        f.write(line)
    f.close()
    return None


def extract_peak_curves(filename, low_e, high_e, save_folder):
    Qz, I = get_data(filename, low_e, high_e)
    # create energy list according to energy bonds
    energy_list = np.linspace(low_e, high_e, (high_e - low_e) // 10 + 1)
    for qz in Qz:
        savename = 'Qz = ' + str(qz) + '.txt'
        save_path = os.path.join(save_folder, savename)
        write_peak_curves(save_path, energy_list, I)
    return None

extract_peak_curves(filename, low_e, high_e, save_folder)
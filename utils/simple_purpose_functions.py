import matplotlib.pyplot as plt
import numpy as np
import os

from utils.input_output import get_data

path = '/Users/rachel/NSLS_II_beamtrips/2023_7_during_trip/XRF_data'
os.chdir(path)

def plot_energy_range(filename, low_bond, high_bond):
    Qz, I = get_data(filename, low_bond, high_bond)
    energies = np.linspace(low_bond, high_bond, (high_bond - low_bond)//10 + 1)
    cmap = plt.get_cmap('viridis')
    i = 0
    for y in I:
        c = cmap(i/len(I))
        plt.plot(energies, y, label = str(Qz[i])[0:5], color = c)
        i+=1
    plt.legend()
    plt.show()
    return None

def plot_integrated_XF_together(folder_path, filenames_list, label_list):
    i = 0
    plt.figure()
    for filename in filenames_list:
        Qz_list = []
        I_list = []
        err_list = []
        file_path = os.path.join(folder_path, filename)
        f = open(file_path)
        line = f.readline()
        while(line):
            data = line.split()
            Qz, I, err = [float(x) for x in data]
            Qz_list.append(Qz)
            I_list.append(I)
            err_list.append(err)
            line = f.readline()
        label = label_list[i]
        i += 1
        plt.errorbar(Qz_list, I_list, err_list, label = label, fmt='-o')
    plt.xlabel('Qz')
    plt.ylabel('Integrated_Intensity')
    plt.legend()
    plt.show()

angstrom = "\u00C5"  # Angstrom symbol (Å)
superscript_2 = "\u00B2"  # Superscript 2 (²)

# Create the formatted string
formatted_text = f"{angstrom}{superscript_2}"

x = ['KCl', 'KI', 'KClO4']
y = [0.0152, 0.0130, 0.0156]
plt.title('1mM salts pH4')
plt.bar(x, y, width = 0.4)
plt.ylabel('ion per unit ' + formatted_text)
plt.show()




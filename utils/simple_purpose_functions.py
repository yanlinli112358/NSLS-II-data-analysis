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



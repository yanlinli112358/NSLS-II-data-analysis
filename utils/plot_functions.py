import numpy as np
import matplotlib.pyplot as plt

from utils.input_output import get_data
def plot_spec(filename, low_e, high_e, scale_factor):
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
    #plt.show()
    return None

def plot_integrated_I(Qz, integrated_I, err_I, file):
    plt.figure()
    plt.errorbar(Qz, integrated_I, yerr=err_I, fmt="o", c = 'brown')
    #plt.title(file + ' integrated intensity')
    plt.ylabel('Integrated Intensity (a.u.)', fontsize = 14)
    plt.xlabel('Qz', fontsize = 14)
    # plt.savefig('XF_plots/' + file)
    #plt.show()
    return None

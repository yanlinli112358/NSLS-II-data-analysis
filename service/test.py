import matplotlib.pyplot as plt
import os

import numpy as np

from utils.input_output import get_data

path = '/Users/rachel/NSLS_II_beamtrips/2023_7_trip_shared/XRF_data'
os.chdir(path)

file1 = 'Fluo_data_col[energies]_rows[qz]-10Mm KI_1-368f467b'
filename1 = file1 + '.csv'

file2 = 'Fluo_data_col[energies]_rows[qz]-0P5mM_KI_ODA-38ffdc14'
filename2 = file2 + '.csv'

file3 = 'Fluo_data_col[energies]_rows[qz]-water_1-c941df92'
filename3 = file3 + '.csv'

file4 = 'Fluo_data_col[energies]_rows[qz]-0p5mM_KCl_ODA_2-add53292'
filename4 = file4 + '.csv'

from utils.fit_functions import total_counts_in_range

Qz1, total_counts_list1 = total_counts_in_range(filename1, 10, 40950)
Qz2, total_counts_list2 = total_counts_in_range(filename2, 10, 40950)
Qz3, total_counts_list3 = total_counts_in_range(filename3, 10, 40950)
Qz4, total_counts_list4 = total_counts_in_range(filename4, 10, 40950)

low_e = 2000
high_e = 12000


I1 = get_data(filename1, low_e, high_e)[1]
I2 = get_data(filename2, low_e, high_e)[1]
I3 = get_data(filename3, low_e, high_e)[1]
I4 = get_data(filename4, low_e, high_e)[1]

plt.scatter(Qz1, total_counts_list1, label = '10mM_KI_reference')
plt.scatter(Qz2, total_counts_list2, label = '0.5mM_KI')
plt.scatter(Qz3, total_counts_list3, label = 'pure_water')
plt.scatter(Qz4, total_counts_list4, label = '0.5mM_KI')

plt.xlabel('Qz')
plt.ylabel('counts')
plt.title('total number of counts received by detector')
plt.legend()
plt.savefig('compare_total_counts.jpg')
plt.show()


for i in range(len(Qz1)):
    energies = np.linspace(low_e, high_e, (high_e - low_e)//10 + 1)
    plt.plot(energies, I1[i], label = '10mM_KI_reference')
    plt.plot(energies, I2[i], label = '0.5mM_KI')
    plt.plot(energies, I3[i], label = 'pure_water')
    plt.plot(energies, I4[i], label='0.5mM_KCl')
    plt.legend()
    plt.ylim((0, 20))
    plt.title('Qz = ' + str(Qz1[i])[0:5])
    plt.show()

from utils.fit_functions import total_counts_in_range
print(total_counts_in_range(filename3, 4000, 6000)[1])
print(total_counts_in_range(filename4, 4000, 6000)[1])

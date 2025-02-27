import numpy as np
import matplotlib.pyplot as plt
import os

from utils.input_output import remove_bkg_complete, get_data

path = '/Users/rachel/NSLS_II_beamtrips/2025_1_shared/XRF_data/q_image'
bkg_path = '/Users/rachel/NSLS_II_beamtrips/2025_1_shared/XRF_data/no_bkg'
os.chdir(path)

#remove the bakground and save file
filename = 's47_DODMA_1mM_KBr_#41835_XRF_qimage'
bkg_filename = 's58_DODMA_water_#41930_XRF_qimage'
file = filename + '.csv'
bkg_file = bkg_filename + '.csv'
remove_bkg_complete(file, bkg_file)
file_no_bkg = os.path.join(bkg_path, filename + '-no_bkg' + '.csv')
print(file_no_bkg)

#visualize data
low_e = 11000
high_e = 13000
energy_list = np.linspace(low_e, high_e, (high_e - low_e) // 10 + 1)
Qz, I = get_data(file, low_e, high_e)
Qz_no_bkg, I_no_bkg = get_data(file_no_bkg, low_e, high_e)
i = 0
from utils.plot_functions import plot_spec_compare
plot_spec_compare(file, file_no_bkg, low_e, high_e, 'raw', 'no_bkg')

import matplotlib.pyplot as plt
import numpy as np

# Data from the table (percentages)
molecules = ['ODA', 'ODG', 'DODMA']
Cl = [17.5, 0, 0]
Br = [27.6, 13.8, 43.0]
I = [40.5, 79.0, 62.0]
ClO4 = [33.0, 87.8, 0]
GC_prediction = [50.7, 99.7, 80.6]

x = np.arange(len(molecules))  # X-axis positions
width = 0.15  # Bar width

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(x - 2*width, Cl, width, label='Cl', alpha=0.8, color='royalblue')
plt.bar(x - 1*width, Br, width, label='Br', alpha=0.8, color='green')
plt.bar(x, I, width, label='I', alpha=0.8, color='orange')
plt.bar(x + 1*width, ClO4, width, label='ClO4', alpha=0.8, color='brown')
plt.bar(x + 2*width, GC_prediction, width, label='GC prediction', alpha=0.8, color='gray')

# Labels and Title
plt.xlabel('Molecules')
plt.ylabel('Percentage (%)')
plt.title('Ion adsorption to molecules')
plt.xticks(x, molecules)
plt.legend(title="Ions")

# Grid and Layout
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

# Show plot
plt.show()


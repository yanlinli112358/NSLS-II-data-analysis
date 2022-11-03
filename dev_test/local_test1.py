
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
sys.path.append('../')
from utils.input_output import get_all_data
from utils.input_output import get_data
from utils.input_output import get_qz

#specify path
os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip_shared')

file = 's_test'
filename = 'fluo_data/' + file + '.txt'
filename2 = 'fluo_data/' + file + '2.csv'
low_e = 0
high_e = 12200

I = get_all_data(filename, low_e, high_e)
print(len(I[0]))
print(I[0][0:10])

Qz, I2 = get_data(filename2, low_e, high_e)
print(len(I2[1]))
print(I2[1][1:10])

print(get_qz('fluo_data/Qz.txt'))
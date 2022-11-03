import os

os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip_shared/fluo_data')
path = os.getcwd()

def get_data(filename, low_e, high_e):
    Qz = []
    I = []
    print(os.getcwd())
    f = open(filename, 'r')
    line = f.readline()
    line = f.readline()
    while(line):
        data = line.split(',')
        Qz.append(float(data[0]))
        y = [float(x) for x in data[low_e//10 : high_e//10 + 1]] # list of intensities in the range of interest
        I.append(y) # I = 2D array of energies = energies each Qz
        line = f.readline()
    f.close()
    return Qz, I

def get_all_data(filename, low_e, high_e):
    I = []
    f = open(filename, 'r')
    line = f.readline()
    while(line):
        data = line.split()
        y = [float(x) for x in data[low_e//10 : high_e//10 + 1]]
        I.append(y)
        line = f.readline()
    f.close()
    return I

def get_qz(filename):
    f = open(filename, 'r')
    Qz_list = []
    line = f.readline()
    while(line):
        Qz_list.append(float(line))
        line = f.readline()
    return Qz_list

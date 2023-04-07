import os

os.chdir('/Users/rachel/NSLS_II_beamtrips/2022_10_trip_shared/fluo_data')
path = os.getcwd()


def get_data(filename, low_e, high_e): #get XF counts from fluo_data in the range of low_e to high_e
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

def get_all_data(filename, low_e, high_e): #get XF intensity data from fluo_data_all, E
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

def get_qz(filename): #get Qz data from fluo_data_all Qz
    f = open(filename, 'r')
    Qz_list = []
    line = f.readline()
    while(line):
        Qz_list.append(float(line))
        line = f.readline()
    return Qz_list

def get_xf_integral(filename): #get Qz, integrated_XF and err_list from XF integrated inensities
    f = open(filename, 'r')
    Qz_list = []
    xf_list = []
    err_list = []
    line = f.readline()
    line = f.readline()
    while(line):
        data = line.split('\t')
        Qz_list.append(float(data[0]))
        xf_list.append(float(data[1]))
        err_list.append(float(data[2]))
        line = f.readline()
    return Qz_list, xf_list, err_list

def get_curve(filename): #?forget what's the use of it
    f = open(filename, 'r')
    Qz_list = []
    flu_list = []
    line = f.readline()
    while(line[0] == '#'):
        line = f.readline()
    while(line):
        data = line.split('\t')
        Qz_list.append(data[0])
        flu_list.append(data[1])
        line = f.readline()
    return Qz_list, flu_list

def get_total_counts(filename): #returns a list of total counts at each Qz
    total_counts = []
    f = open(filename, 'r')
    line = f.readline()
    line = f.readline()
    while(line):
        data = line.split(',')
        total = sum(float(x) for x in data[1:])
        total_counts.append(total)
        line = f.readline()
    return total_counts



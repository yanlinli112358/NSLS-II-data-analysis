#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:46:31 2022

@author: Rachel
"""
import matplotlib.pyplot as plt
import numpy as np

"""
Run this python file to batch process BNL XRR data into rrf and ref data
"""
import os
path = '/Users/rachel/NSLS_II_beamtrips/2024_4_trip_final/XRR_analysis'
os.chdir(path)
read_folder = 'data'
rrf_read_folder = 'data3'
ref_read_folder = 'data2'
path_read = os.path.join(path, read_folder)
path_read_rrf = os.path.join(path, rrf_read_folder)
path_read_ref = os.path.join(path, ref_read_folder)

def process_BNL(filename):
    qz = []
    ref = []
    err = []
    rrf = []
    err_rrf = []

    ref_name = filename[:-4] + '_ref' + filename[-4:]
    rrf_name = filename[:-4] + '_rrf' + filename[-4:]
    f = open(read_folder + '/' + filename, 'r')
    fref = open('ref/'+ ref_name, 'w')
    frrf = open('rrf/'+ rrf_name, 'w')
    line = f.readline()
    while line:
        data_str = line.split()
        if data_str[0][0].isdigit():
            data = [float(i) for i in data_str]
            qz.append(data[0])
            ref.append(data[1])
            err.append(data[2])
            rrf.append(data[3])
            err_rrf.append(data[4])
            write1 = ' '.join([data_str[0], data_str[1], data_str[2]])
            write2 = ' '.join([data_str[0] ,data_str[3], data_str[4]])
            fref.writelines(write1 + '\n')
            frrf.writelines(write2 + '\n')
        line = f.readline()
    f.close()
    fref.close()
    frrf.close()
    return


# filenames = os.listdir(path_read)
# for i in range(len(filenames)):
#     if filenames[i] == '.DS_Store':
#         continue
#     process_BNL(filenames[i])
#
# rrf_files = os.listdir(os.path.join(path, 'rrf'))
# ref_files = os.listdir(os.path.join(path, 'ref'))


def process_BNL_rrf(filename):
    qz = []
    rrf = []
    err_rrf = []
    rrf_name = filename[:-4] + '_rrf' + filename[-4:]

    f = open(rrf_read_folder + '/' + filename, 'r')
    frrf = open('rrf/'+ rrf_name, 'w')
    line = f.readline()
    while line:
        data_str = line.split()
        if data_str[0][0].isdigit():
            data = [float(i) for i in data_str]
            qz.append(data[0])
            rrf.append(data[1])
            err_rrf.append(data[2])
            write = ' '.join([data_str[0], data_str[1], data_str[2]])
            frrf.writelines(write + '\n')
        line = f.readline()
    f.close()
    return [qz, rrf, err_rrf]

def process_BNL_ref(filename):
    qz = []
    ref = []
    err_ref = []
    ref_name = filename[:-4] + '_ref' + filename[-4:]

    f = open(ref_read_folder + '/' + filename, 'r')
    fref = open('ref/'+ ref_name, 'w')
    line = f.readline()
    while line:
        data_str = line.split()
        print(data_str)
        if data_str[0][0].isdigit():
            data = [float(i) for i in data_str]
            qz.append(data[0])
            ref.append(data[1])
            err_ref.append(data[3])
            write = ' '.join([data_str[0], data_str[1], data_str[3]])
            fref.writelines(write + '\n')
        line = f.readline()
    f.close()
    return [qz, ref, err_ref]

filenames = os.listdir(path_read_rrf)
for i in range(len(filenames)):
    if filenames[i] == '.DS_Store':
        continue
    process_BNL_rrf(filenames[i])
rrf_files = os.listdir(os.path.join(path, 'rrf'))

filenames = os.listdir(path_read_ref)
for i in range(len(filenames)):
    if filenames[i] == '.DS_Store':
        continue
    process_BNL_ref(filenames[i])
ref_files = os.listdir(os.path.join(path, 'ref'))


def plot_all_xrr_log(path_list):
    rrf = []
    qz = []
    err = []
    for i in range(len(path_list)):
        f = open(os.path.join(path,'rrf/'+path_list[i]),'r')
        line = f.readline()
        while(line):
            data = line.split()
            qz.append(data[0])
            rrf.append(data[1])
            err.append(data[2])
        f.close()
        print(i)
        rrf_log = np.log(rrf)
        plt.errorbar(qz, rrf_log, err)
        print(i)

plt.figure()
plot_all_xrr_log(rrf_files)
plt.show()

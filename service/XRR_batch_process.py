#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 16:46:31 2022

@author: Rachel
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
path = '/Users/Rachel/NU/308307_dutta (1)/XRR_analysis (1)/data2 (1)'

os.chdir(path)

def process_BNL(filename):
    qz = []
    ref = []
    err = []
    rrf = []
    f = open(filename, 'r')
    fref = open('/Users/Rachel/NU/308307_dutta (1)/XRR_analysis (1)/ref/' + filename, 'w')
    frrf = open('/Users/Rachel/NU/308307_dutta (1)/XRR_analysis (1)/rrf/' + filename, 'w')
    line = f.readline()
    while line:
        data_str = line.split()
        if data_str[0][0].isdigit():
            data = [float(i) for i in data_str]
            qz.append(data[0])
            ref.append(data[1])
            err.append(data[2])
            rrf.append(data[3])
            write1 = ' '.join([data_str[0], data_str[1], data_str[2]])
            write2 = ' '.join([data_str[0] ,data_str[3], data_str[1]])
            fref.writelines(write1 + '\n')
            frrf.writelines(write2 + '\n')
        line = f.readline()
    f.close()
    fref.close()
    frrf.close()
'''
    fig, axes = plt.subplots(2,1)
    #plot ref
    axes[0].errorbar(qz, np.log(ref), yerr = err)
    axes[0].set_xlabel('Qz')
    axes[0].set_ylabel('Reflectivity (log_scale')
    #plot r/rf
    axes[1].errorbar(qz, rrf, yerr = err)
    axes[1].set_xlabel('Qz')
    axes[1].set_ylabel('R/RF')

'''



filenames = os.listdir(path)
for i in range(len(filenames)):
    if filenames[i] == '.DS_Store':
        continue
    process_BNL(filenames[i])
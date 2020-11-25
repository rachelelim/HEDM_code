#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:46:29 2020

@author: rachellim
"""

import numpy as np

import pickle as cpl
from hexrd import rotations as rot
from hexrd import matrixutil as mutil
from hexrd import symmetry   as sym

#%%

main_dir = '#######'
sample = '#####'
grains_files = '######' #grains.out files
stress_files = '######' #pickled stress files


scanIDs = np.arange(#####) 


#%% Load data

data={}
stress_data = {}
grain_data = {}


for i in range(len(scanIDs)): #puts all of the data from the FF into dictionaries
    grain_fname = os.path.join(main_dir, sample + grains_files %scanIDs[i])
    stress_fname = os.path.join(main_dir, sample + stress_files %scanIDs[i])

    grain_data['scan%d' %scanIDs[i]] = np.loadtxt(grain_fname)
    stress_data['scan%d' %scanIDs[i]] = cpl.load(open(stress_fname,'rb'),encoding='latin1')


#%%
sig_macro = np.array([0,500,0,0,0,0]) #macroscopic stress tensor here
mag_sig_macro = np.linalg.norm(sig_macro)

coax = np.zeros([ngrains,len(scanIDs)])

for scan in range(0,len(scanIDs)):
    print(scan)

    sig_grain = stress_data['scan%d'%loaded_scans[scan]]['stress_S']
    for grains in range(0,len(sig_grain)):

        mag_sig_grain = np.linalg.norm(sig_grain[grains,:])
        coaxiality = np.degrees(np.arccos(np.inner(sig_macro,sig_grain[grains,:])/(mag_sig_grain*mag_sig_macro)))
        coax [grains,scan] = coaxiality
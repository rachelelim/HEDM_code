#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 15:53:22 2020

@author: rachellim

Plots the probability plots for a timeseries of data (von mises stress used as example)
"""

import numpy as np
from matplotlib import pyplot as plt
import os

import cPickle as cpl


from scipy.stats import probplot


#%%

main_dir = '#######'
sample = '#####'
grains_files = '######' #grains.out files
stress_files = '######' #pickled stress files


scanIDs = np.arange(#####) #for fd1-q-1


ngrains = ###### #currently manually set but really shouldn't be

#==============================================================================
# %%  Make color list
#==============================================================================



colors=np.arange(0,len(scanIDs))

colornums = np.arange(10,256,246/len(colors))


cmap = plt.cm.inferno_r

cmaplist = [cmap(i) for i in range(cmap.N)]


#%% Load data

data={}
stress_data = {}
grain_data = {}



for i in range(len(scanIDs)): #puts all of the data from the FF into dictionaries
    grain_fname = os.path.join(main_dir, sample + grains_files %scanIDs[i])
    stress_fname = os.path.join(main_dir, sample + stress_files %scanIDs[i])

    grain_data['scan%d' %scanIDs[i]] = np.loadtxt(grain_fname)
    stress_data['scan%d' %scanIDs[i]] = cpl.load(open(stress_fname,'rb'),encoding='latin1')



vonmises = np.zeros([ngrains,len(scanIDs)])

for i in range(len(scanIDs)):
    vonmises[:,i] = (stress_data['scan%d'%scanIDs[i]]['von_mises'][:,0])/1e6


#%%

fig1 = plt.figure(figsize=(6,5))
ax1 = plt.subplot(111)


for i in range(0,vonmises.shape[1]):
    pp = vonmises[:,i]
    x,y= probplot(pp)[0]
    plt.plot(y,x,'.',color=cmaplist[colornums[i]])


plt.xlim(left=0,right=0.25)


#these are admittedly hardcoded -REL
ax1.set_yticks([#-3.7190,
   # -3.2905,
   -3.0902,
   # -2.5758,
   -2.3263,
   -1.6449,
   -1.2816,
   -0.6745,
         0,
    0.6745,
    1.2816,
    1.6449,
    2.3263,
    # 2.5758,
    3.0902,
    # 3.2905,
    # 3.7190
    ])
ax1.set_yticklabels( [#'0.01',
    # '0.0005',
    '0.1',
    # '0.005 ',
    '1',
    '5',
    '10',
    '25',
    '50',
    '75',
    '90',
    '95',
    '99',
    # '0.995 ',
    '99.9',
    # '0.9995',
    # '99.99'
    ],horizontalalignment='center')
ax1.ticklabel_format()

ax1.tick_params(labelsize=12)
ax1.tick_params(axis='y',pad=20)
ax1.tick_params(axis='x',pad=8)

plt.xlabel(r'$\sigma_{VM}$ (MPa)',fontsize=18)
plt.ylabel('Probability (%)',fontsize=18)

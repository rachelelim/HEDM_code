#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 17:19:53 2018

@author: rachellim

Makes input files for building a synthetic microstructure in Dream3D from FF data
"""

import numpy as np

filepath = '####'

data = np.loadtxt('####') #grains_file
Euler_all = np.loadtxt('####') #output from Eulers_from_grains.py

chi2 = ### #chi2 cutoff
upper = ### #upper and lower bounds of volume in x and z in mm
lower = ###
upper_y = ### #upper and lower bounds of volume in x and z in mm
lower_y = ###

good_grains = np.where((data[:,2]<chi2) & (data[:,6]>lower) & (data[:,6]<upper) & (data[:,7]>-lower_y) & (data[:,7]<upper_y) & (data[:,8]>lower) & (data[:,8]<upper))

COM = data[good_grains,6:9][0]*1000

#adjusts the origin from the center of the sample (FF) to corner (Dream3D)
x = COM[:,0] + (1000 *lower)
y = COM[:,1] + (1000 * 82_y)
z = COM[:,2] + (1000 * lower)

centroids = np.stack([x,y,z]).T

#%%
ones = np.ones([len(centroids),1])
zeros = np.zeros([len(centroids),3])
size = np.expand_dims(np.repeat(20,len(centroids)),axis=1)
grainIDs = np.expand_dims(np.arange(0,len(centroids))+1,axis=1)

out = np.hstack([ones,np.round(centroids),size,size,size,ones,zeros])

for i in range(len(Euler_all)):
    for j in range(3):
        if Euler_all[i,j] < 0:
            Euler_all[i,j] += np.pi*2

Euler_out = np.hstack([grainIDs,ones,Euler_all[good_grains,:][0]])


matched_grains = np.hstack([data[good_grains,0].T,grainIDs])
#%%

np.savetxt(filepath + '/Eulers_for_Dream3d_large.txt',Euler_out,fmt = '%d\t%d\t%0.4f\t%0.4f\t%0.4f', header='%d' %len(centroids))
np.savetxt(filepath + '/for_Dream3D_large.txt',out,fmt = '%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t', header='%d' %len(centroids))
np.savetxt(filepath + '/matched_grains_CMU-1_Dream3d_large.txt',matched_grains,fmt='%d',delimiter='\t',header = 'newID \t oldID')

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 15:03:27 2020

@author: rachellim

Used to plot strain components in 2D to check spatial distribution of strain components for reasonability
"""

import numpy as np
from matplotlib import pyplot as plt

data = np.loadtxt('#####')

chi2 = data[:,2]


good_grains = np.where(chi2 < 5e-3)

good_data = data[good_grains[0],:]

x = good_data[:,6]
y = good_data[:,7]
z = good_data[:,8]

strain = good_data[:,15:]

eps11 = strain[:,0]
eps22 = strain[:,1]
eps33 = strain[:,2]
eps23 = strain[:,3]
eps13 = strain[:,4]
eps12 = strain[:,5]

#%%

fig = plt.figure(figsize=(6,5))

plt.scatter(x, z, s=50,c=eps22,cmap='bwr',vmin=-1e-3,vmax=1e-3)
plt.colorbar()

plt.xlabel('X', fontsize=14)
plt.ylabel('Z', fontsize=14)
plt.title(r'$\epsilon_{22}$',fontsize=18)

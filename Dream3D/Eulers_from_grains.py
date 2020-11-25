#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 19:37:35 2020

@author: rachellim

Calculates Euler angles from grains.out file for input into FFtoDream3D.py
"""

from hexrd import rotations as rot

import numpy as np

#%%
data = np.loadtxt('#####') #grains_file

ors = data[:,6:9]

Eulers = np.zeros([len(ors),3])

for i in range(len(ors)):
    rmats = rot.rotMatOfExpMap(ors[i,:])

    Eulers[i,:] = rot.angles_from_rmat_zxz(rmats)



np.savetxt('#####',Eulers,delimiter='\t')
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 15:48:33 2021

@author: rachellim


Needs the hexrdgui module
"""

import numpy as np
from matplotlib import pyplot as plt



import yaml

from multiprocessing import Pool
import multiprocessing as mp

from functools import partial

try:
    import dill as cpl
except(ImportError):
    import pickle as cpl

from mpl_toolkits.mplot3d import Axes3D

from hexrd import instrument
from hexrd.transforms import xfcapi
from hexrd import rotations as rot
from hexrd import gridutil as gutil
from hexrd.matrixutil import unitVector
from hexrd.symmetry import toFundamentalRegion
from hexrd import matrixutil as mutil
from hexrd.fitting import peakfunctions as pkfunc
from hexrd import material
from hexrd import valunits
from hexrd import imageseries
from hexrd.imageseries.omega import OmegaImageSeries

import polarview as pv


#%% Functions

def load_pdata(filename, d_min, energy, mat):
    '''Note: fixed for new materials files as of hexrd v0.8.x'''

    kev = valunits.valWUnit("beam_energy", "energy", energy, "keV")
    dmin = valunits.valWUnit("dmin", "length", d_min, "angstrom")
    mats = material.load_materials_hdf5(filename, dmin=dmin, kev=kev)
    pd = mats[mat].planeData
    return pd


# instrument
def load_instrument(yml):
    with open(yml, 'r') as f:
        icfg = yaml.load(f)
    instr = instrument.HEDMInstrument(instrument_config=icfg)
    for det_key in instr.detectors:
        if 'saturation_level' in icfg['detectors'][det_key].keys():
            sat_level = icfg['detectors'][det_key]['saturation_level']
            print("INFO: Setting panel '%s' saturation level to %e"
                  % (det_key, sat_level))
            instr.detectors[det_key].saturation_level = sat_level
    return instr


#%% User Input

det_file = '2m_instrument.yml'

mat_file = 'materials.h5'
mat_name = 'IN625'

x_ray_energy = 61.332  # keV

image_file = '/Users/rachellim/Documents/PSU/xray_thermal_simulation/2021-01-25_simulator_port/images/Pulse_400W_D500um_Abs0P50_2M_0.001_0.01_0.25_4.npz'

# all these values are in degrees
tth_min = 3
tth_max = 18
tth_res = 0.025

eta_min = 0
eta_max = 360
eta_res = 0.25

#%% Initialization

instr = load_instrument(det_file)
instr.detectors['2M'].panel_buffer = np.array([0., 0.])
planar_det = instr.detectors['2M']

plane_data = load_pdata(mat_file, 0.7, x_ray_energy, mat_name)

det_keys = instr.detectors.keys()
det_keys = sorted(det_keys)


#%% Load image(s)

data = np.load(image_file, 'r')
all_frames = data['images']

print('%s frames' %all_frames.shape[0])


images  = {}


#%% Check frame visually

fig0 = plt.figure()
plt.imshow(data['images'][0,:,:], vmax=25, cmap='bone')


#%% Unwrap data into eta-tth map

tth = np.arange(tth_min, tth_max, tth_res)
eta = np.arange(eta_min, eta_max, eta_res)

eta_tth = np.zeros([all_frames.shape[0],1440,len(tth)])
polar = pv.PolarView((tth_min, tth_max), instr, eta_min=eta_min, eta_max=eta_max, pixel_size=(tth_res, eta_res))

for i in range(all_frames.shape[0]):
    images['2M'] = data['images'][i,:,:]

    wimg = polar.warp_image(images)

    eta_tth[i,:,:] = wimg



#%% Plot a single frame of eta-tth


frame = 0

fig1 = plt.figure()
plt.imshow(eta_tth[frame,:,:],vmax=25, cmap='bone')
plt.xlabel(r'2$\theta$',fontsize=16)
plt.ylabel(r'$\eta$', fontsize=16)



#%% Sum rings to make intensity-tth line plot


# !!! need to account for rings falling off detector

integrated = np.sum(eta_tth, axis=1)

fig2 = plt.figure()
plt.plot(tth, integrated[frame,:])
plt.xlabel(r'2$\theta$ ($^\circ$)',fontsize=16)
plt.ylabel('Intensity', fontsize=16)
plt.xlim(left = tth_min, right = tth_max)
plt.ylim(bottom = 0)

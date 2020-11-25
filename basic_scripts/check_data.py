#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:02:29 2020

@author: rachellim

Used to make histograms to check distribution of strain components for reasonability
"""
import sys
import numpy as np
from matplotlib import pyplot as plt

def filter_grains(grainsout,chi2_thresh=1e-2,completeness=0.95,hthresh=0.3):
    good_grains = np.where((grainsout[:,2]<chi2_thresh) & (grainsout[:,1]>completeness) &
                                          (grainsout[:,6] < hthresh) & (grainsout[:,6] > -hthresh) &
                                          (grainsout[:,8] < hthresh) & (grainsout[:,8] > -hthresh))
    return good_grains[0]


#%%
scan = #####

data = np.loadtxt('#####')


#%%

good_grains = filter_grains(data,completeness=0.95)

good_data = data[good_grains,:]


chi2 = good_data[:,2]
comp = good_data[:,1]


num_bins = int(np.sqrt(len(good_data)))
#%%
fig1 = plt.figure()
plt.hist(chi2,bins=num_bins)
plt.xlabel(r'$\chi^2$',FontSize=16)
plt.xlim(left=0)
plt.ticklabel_format(axis='x',style='scientific',scilimits=(0,0))



fig2 = plt.figure()
plt.hist(comp,bins=num_bins)
plt.xlabel('Completeness',FontSize=16)
plt.xlim(right=1)


#%%

strain11 = good_data[:,15]
strain22 = good_data[:,16]
strain33 = good_data[:,17]
strain23 = good_data[:,18]
strain13 = good_data[:,19]
strain12 = good_data[:,20]


sum11 = np.sum(strain11)
sum22 = np.sum(strain22)
sum33 = np.sum(strain33)
sum23 = np.sum(strain23)
sum13 = np.sum(strain13)
sum12 = np.sum(strain12)

#%%

top=250

fig3 = plt.figure(figsize=(9,6))

ax1 = plt.subplot(2,3,1)
plt.hist(strain11,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{xx}$',FontSize=16)



ax2 = plt.subplot(2,3,2)
plt.hist(strain22,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{yy}$',FontSize=16)


ax3 = plt.subplot(2,3,3)
plt.hist(strain33,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{zz}$',FontSize=16)


ax4 = plt.subplot(2,3,4)
plt.hist(strain23,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{yz}$',FontSize=16)


ax5 = plt.subplot(2,3,5)
plt.hist(strain13,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{xz}$',FontSize=16)


ax6 = plt.subplot(2,3,6)
plt.hist(strain12,bins=num_bins,range=(-2.5e-3,2.5e-3))
plt.xlim(left=-2.5e-3,right=2.5e-3)
plt.ylim(top=top)
plt.xlabel(r'$\epsilon_{xy}$',FontSize=16)


plt.subplots_adjust(hspace = 0.3)
plt.suptitle('Scan %d'%scan, fontsize=22)


#%%

print('strain_xx averages to %.5e'%(sum11/len(good_data)))
print('strain_yy averages to %.5e'%(sum22/len(good_data)))
print('strain_zz averages to %.5e'%(sum33/len(good_data)))
print('strain_yz averages to %.5e'%(sum23/len(good_data)))
print('strain_xz averages to %.5e'%(sum13/len(good_data)))
print('strain_xy averages to %.5e'%(sum12/len(good_data)))

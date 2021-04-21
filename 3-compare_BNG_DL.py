# Script to compare orientation estimates from BNG and DL.

%load_ext autoreload
%autoreload
from setup_parameters import *
import matplotlib.pyplot as plt
import obspy
from obspy.clients.fdsn import Client
import numpy as np
import os
from pathlib import Path
import pandas as pd
%matplotlib inline

# %% codecell

file_bng = search_dir + '/BNG/orientations_BNG.txt'
file_dl = search_dir + '/DL/orientations_DL.txt'

# Load measurements
ori_bng = pd.read_table(file_bng, delim_whitespace=True)
ori_dl = pd.read_table(file_dl, delim_whitespace=True)


# %% Plot measurements
fig=plt.figure()
ax=fig.add_axes([0,0,1,1])
ax.errorbar(ori_bng.phi,ori_dl.phi,yerr=ori_dl.err,xerr=ori_bng.err,fmt='o')
for ii,sta in enumerate(ori_dl.sta):
    ax.text(ori_bng.phi[ii],ori_dl.phi[ii],str(sta),ha='right',va='bottom')
xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.plot(xlim,xlim,'--k')
ax.set_xlim(xlim)
ax.set_ylim(xlim)
ax.set_xlabel('BNG $\phi$ ($^\circ$)')
ax.set_ylabel('DL $\phi$ ($^\circ$)')
fig.show()
plt.tight_layout()
fig.savefig(search_dir+'compare_bng_dl.pdf',bbox_inches = "tight")

# Script to run DL surface wave algorithm to estimate orientations

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

DL_out = search_dir + '/DL/'
# %% codecell
if not os.path.exists(DL_out):
    os.makedirs(DL_out)
    
# LOAD CLIENT
client = Client(webservice)
print(client)

# %% codecell
# LOAD STATIONS
inventory = client.get_stations(network=network, station=stations, channel=compstr)
print(inventory)
file = open(DL_out+'stations.txt', 'w')
for ista in range(0,len(inventory[0])) :
    file.write("%5s %12f %12f %12f\n" % (inventory[0].stations[ista]._code, 
                                        inventory[0].stations[ista]._latitude, 
                                        inventory[0].stations[ista]._longitude, 
                                        inventory[0].stations[ista]._elevation))
file.close()


# %% codecell
# BUILD STATION DATABASE
stas = ",".join([sta._code for sta in inventory[0].stations])
stdb_out = DL_out+'sta_list'
!{path2envbin+'query_fdsn_stdb.py'} -N {network} -C {compstr} -S {stas} {stdb_out}

# %% codecell
# Perform DL analysis
stdb_pkl = stdb_out+'.pkl'
!{path2envbin+'dl_calc'} --min-mag={minmagnitude} --save-location {DL_out} {stdb_pkl}

# %% codecell
# Plot DL output and save
!{path2envbin+'dl_average'} --load-location {DL_out} --plot --save {stdb_pkl}
# !{path2envbin+'dl_average'} --load-location {DL_out} {stdb_pkl}

# %% codecell
# Combine all measurements into single file
pathlist = sorted(Path(DL_out).glob('*/orientation_dl.txt'))
file = open(DL_out+'/orientations_DL.txt', 'w')
file.write("%8s %10s %10s %5s\n" % ('sta', 'phi', 'err', 'num'))
for path in pathlist:
    data = pd.read_table(path, delim_whitespace=True)
    sta = data.sta[0]
    phi = data.phi[0]
    err = data.err[0]
    num = data.num[0]
    file.write("%8s %10f %10f %5d\n" % (sta, phi, err, num))
file.close()
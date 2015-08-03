#!/usr/bin/env python
#Code to calcuate and make contour plots of foF2 from RBN data over a specified region and time

import sys
import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd

from davitpy import gme
from davitpy.utils import *
import datetime

import rbn_lib
import handling

#Specify output filename
outFile=''
rbnMap=''
fof2Map=''

#Specify spatial limits for links 
latMin=25
latMax=52  
lonMin=-130
lonMax=-65

#Map Properties 
#define map projection 
mapProj='cyl'
llcrnrlon=lonMin-5 
llcrnrlat=latMin-5
urcrnrlon=lonMax+5
urcrnrlat=latMax+5
#llcrnrlon=-130 
#llcrnrlat=25
#urcrnrlon=-65
#urcrnrlat=52 

#create output directory if none exists
#output_dir='output'
output_path = os.path.join('output','rbn','foF2')
#handling.prepare_output_dirs({0:output_dir},clear_output_dirs=True)
try: 
    os.makedirs(output_path)
except:
    pass 

#Specify start and end times
#sTime = datetime.datetime(2015,9,10)
#eTime = datetime.datetime(2015,9,15)
#sTime = datetime.datetime(2015,6,28,01,12)
#eTime = datetime.datetime(2015,6,28,01,22)
sTime = datetime.datetime(2015,6,28,01,16)
eTime = datetime.datetime(2015,6,28,01,18)

map_sTime=sTime
map_eTime=eTime

#Read RBN data 
rbn_df  = rbn_lib.read_rbn(map_sTime,map_eTime,data_dir='data/rbn')
import ipdb; ipdb.set_trace()

#Select Region
rbn_df2 = rbn_lib.rbn_region(rbn_df, latMin=latMin, latMax=latMax, lonMin=lonMin, lonMax=lonMax, constr_de=True, constr_dx=True)
import ipdb; ipdb.set_trace()

#Evaluate each link
midLat=np.zeros([len(rbn_df2), 1])
import ipdb; ipdb.set_trace()
midLon=np.zeros([len(rbn_df2), 1])
dist=np.zeros([len(rbn_df2), 1])
m_dist=np.zeros([len(rbn_df2), 1])
#midLon=[]
#dist=[]
#m_dist=[]
for i in range(0, len(rbn_df2)-1): 
    #Isolate the ith link
    deLat=rbn_df2.de_lat.iloc[i]
    deLon=rbn_df2.de_lon.iloc[i]
    dxLat=rbn_df2.dx_lat.iloc[i]
    dxLon=rbn_df2.dx_lon.iloc[i]
#    import ipdb; ipdb.set_trace()
    
    #Calculate the midpoint and the distance between the two stations
    midLat[i], midLon[i],dist[i],m_dist[i] =rbn_lib.path_mid(deLat, deLon, dxLat, dxLon)
#    import ipdb; ipdb.set_trace()
#Test of path_mid function

    #Find Kp, Ap, and SSN for that location and time

    #Get hmF2 from the IRI using geomagnetic indices 

    #Get 

#Save information in data frame
rbn_df2['midLat']=midLat
rbn_df2['midLon']=midLon
rbn_df2['link_dist']=dist
rbn_df2['m_dist']=m_dist



#Test plots
#Plot on map
fig = plt.figure(figsize=(8,4))
ax0  = fig.add_subplot(1,1,1)
m, fig=rbn_lib.rbn_map_plot(rbn_df2,legend=False,ax=ax0,tick_font_size=9,ncdxf=True, llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
#leg = rbn_lib.band_legend(fig,loc='center',bbox_to_anchor=[0.48,0.505],ncdxf=True,ncol=4)
filename='RBN_linkLimit_test2.jpg'
filepath    = os.path.join(output_path,filename)
fig.savefig(filepath,bbox_inches='tight')
fig.savefig(filepath[:-3]+'pdf',bbox_inches='tight')
plt.clf()
import ipdb; ipdb.set_trace()

#Test of path_mid function
fig = plt.figure(figsize=(8,4))
ax0  = fig.add_subplot(1,1,1)
df=rbn_df2
m, fig=rbn_lib.rbn_map_plot(df,legend=False,ax=ax0,tick_font_size=9,ncdxf=True, llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)
color='m'
for i in range(0, len(rbn_df2)-1): 
    #Isolate the ith link
    deLat=rbn_df2.de_lat.iloc[i]
    deLon=rbn_df2.de_lon.iloc[i]
    midLat=rbn_df2.midLat.iloc[i]
    midLon=rbn_df2.midLon.iloc[i]
    line, = m.drawgreatcircle(deLon,deLat, midLon, midLat, color=color)

filename='RBN_linkMidpoint_test2.jpg'
filepath    = os.path.join(output_path,filename)
fig.savefig(filepath,bbox_inches='tight')
fig.savefig(filepath[:-3]+'pdf',bbox_inches='tight')
plt.clf()
import ipdb; ipdb.set_trace()

#!/usr/bin/env python
#Make maps of TEC with RBN links

import os
import sys

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.markers as mmarkers


import numpy as np
import pandas as pd

import rbn_lib
#from gps_tec import tec_lib
import tec_lib

import datetime
import handling

#Specify start and end times
year=2014
month=2
day=27
startTime=datetime.datetime(year, month, day,0,0,0)
endTime=datetime.datetime(year, month, day,1,59,59)
delta = datetime.timedelta(minutes = 5)

map_sTime=startTime
map_eTime=map_sTime+delta

#Directories 
tecDir=os.path.join('output', 'tec','data')
outputDir=os.path.join('output', 'tec','data')

kk=0
#Main loop to make TEC/RBN Maps
while map_sTime<endTime:
    #Create output file for map
    filename='rbn_'+'tec_'+map_sTime.strftime('%Y_%m_%H%M_UT-')+map_eTime.strftime('%Y_%m_%H%M_UT')+'.png'
#    filename='test_'+'tec_'+map_sTime.strftime('%Y_%m_%H%M_UT-')+map_eTime.strftime('%Y_%m_%H%M_UT')+'.png'
    outPutFile= os.path.join(outputDir,filename)

    #Read RBN data 
    print "Processing RBN Data for Interval #"+str(kk)+': '+map_sTime.strftime('%H:%M')+'-'+map_eTime.strftime('%H:%M')
    #rbn_df  = rbn_lib.read_rbn_std(map_sTime,map_eTime,data_dir='data/rbn')
    rbn_df  = rbn_lib.read_rbn(map_sTime,map_eTime,data_dir='data/rbn')

    #make TEC map
    fig, m, ax0=tec_lib.makeCartTecMap(tecDir,outputDir,
                   outPutFile,
                   map_sTime,
                   map_eTime,
                   1,
                   1,
                   1.0,
                   15,
                   False)
    #               False,rbn_df,legend=True,tick_font_size=9,ncdxf=True)
#    fig.savefig(outPutFile,bbox_inches='tight')
#    import ipdb; ipdb.set_trace()

    ##################################
    ##Debug Purposes
    #import ipdb; ipdb.set_trace()
    #fig.savefig(outPutFile,bbox_inches='tight')
    #import ipdb; ipdb.set_trace()
    ##################################

    #overlay RBN map
    m, fig=rbn_lib.rbn_map_plot(rbn_df,legend=True,ax=ax0,tick_font_size=9,ncdxf=True, m=m)
    #m, fig=rbn_lib.rbn_map_plot(rbn_df,legend=True,ax=ax0,tick_font_size=9,ncdxf=True, llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, m=m)

    #Save Figure
    fig.savefig(outPutFile,bbox_inches='tight')
    #filename='rbn_'+'tec_'+map_sTime.strftime('%Y_%m_%H%M_UT-')+map_eTime.strftime('%Y_%m_%H%M_UT')+'.png'
    #filepath    = os.path.join(outputDir,filename)
    #fig.savefig(filepath,bbox_inches='tight')
    fig.savefig(outPutFile[:-3]+'pdf',bbox_inches='tight')
    #filename='rbn_'+'tec_'+map_sTime.strftime('%Y_%m_%H%M_UT-')+map_eTime.strftime('%Y_%m_%H%M_UT')+'.jpg'
    #filepath    = os.path.join(outputDir,filename)
    #fig.savefig(filepath,bbox_inches='tight')
    #fig.savefig(filepath[:-3]+'pdf',bbox_inches='tight')
    plt.clf()
    
    #Increment
    kk=kk+1
    map_sTime=map_eTime
    map_eTime=map_sTime+delta

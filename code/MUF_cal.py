#!/usr/bin/env python
#This code is used to obtain the values for the MUF for the 2017 eclipse based off foF2 data from the 1999 Total Solar Eclipse

import sys
import os

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd

from davitpy import gme
import datetime

import rbn_lib
import handling

def MUF_calc(foF2, theta=None, phi=None):
    if phi!=None: 
        MUF=foF2/cos(phi)
    else:
        if theta!=None:
            MUF=foF2/np.cos(180-theta)
        else:
            print "Error: No angle specified"


    return MUF


#Main loop
def find_MUF(f_start,gamma, useTheta=True, f_end=None, f_step=None, incl_fend=True):
    """Find the Maximum Usable frequency (MUF) for a range of critical frequencies and/or anglesPlot Reverse Beacon Network data.

    **Args**:
        * **[f_start]**: start value of critical frequency (in MHz)datetime.datetime object for start of plotting.

    **Returns**:
        * **fig**:      matplotlib figure object that was plotted to

    .. note::
        If a matplotlib figure currently exists, it will be modified by this routine.  If not, a new one will be created.

    Written by Magda Moses 2015 Sept 11
    """
#    f_start
#    f_end=
#    f_step=
    #make sure that f_end is included in array of foF2
    if incl_fend==True:
        fEnd=f_end+f_step
    else:
        fEnd=f_end

    foF2=np.arange(f_start,fEnd,f_step)
    import ipdb; ipdb.set_trace()

    i=0
    n=0
    muf=np.ones([len(foF2)])
#    fof2=np.ones(1,[len(foF2)])
    for angle in gamma:
        if useTheta==True:
            theta=angle
            phi=None
        else: 
            theta=None
            phi=angle

        for f in foF2:
            muf[i]=MUF_calc(f, theta=theta, phi=phi)
#            fof2[i]=f
            import ipdb; ipdb.set_trace()
#            index[i]=i
            i+=1
                
            #end of if statement for storage
        
        #End of second for loop
        angle=angle*np.ones([len(foF2)])
        muf_info=zip(angle, foF2, muf) 
        if n==0:
            import ipdb; ipdb.set_trace()
            df=pd.DataFrame(muf_info, columns=['Takeoff Angle', 'Critical Frequency', 'MUF'])
        else:
            df.append(muf_info)

            #end of if statment
        n=+1

        #End of first for loop
    #Return data frame
    return df
#    Check legnth o
#    frequency_set=zip
#    df=pd.DataFrame(, columns='foF2')

#main script
df=find_MUF(f_start=6,gamma=[16], useTheta=True, f_end=8, f_step=.2, incl_fend=True)
print df.head()
print df.tail()

import ipdb; ipdb.set_trace()

#!/usr/bin/env python
#This code is to get rbn data for a given date and time interval and plot the number of counts per unit time

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

#create output directory if none exists
output_dir='output'
try: 
    os.makedirs(output_dir)
except:
    pass 

#check this line! It may not be what I want to use
#output path=os.path.join('output', 'rbn_counts')
#data_dir=os.path.join('data','rbn')
import ipdb; ipdb.set_trace()
#Specify Several Inputs for the code
#specify index for vectors later in the code
index=0
#specify unit time (in minutes) to make count/unit time
#Note: to change units of unit time then change the expression in tDelta assignment!
dt=5
unit='minutes'
#specify filename for output graph's file
graphfile='rbnCount_time_step_5min'

#specify times
sTime=datetime.datetime(2014,9,10,16,45)
eTime=datetime.datetime(2014, 9,10, 18, 30)
#specify time interval for spot counts
tDelta=datetime.timedelta(minutes=dt)

#Generate a time/date vector
curr_time=sTime
#Two ways to have time labels for each count for the graph of counts  vs time: 
    #1) the number of counts and the time at which that count started 
    #2) the number of counts and the time at which that count ended [the number of counts in a 5min interval stamped with the time the interval ended and the next interval began]
#For option 1: uncomment line 48 and comment line 49 (uncomment the line after these notes and comment the one after it)
#For option 2: uncomment line 49 and comment line 48 (comment the following line and uncomment the one after it)
#times=[sTime]
curr_time += tDelta
times=[curr_time]
#if using option 2 then delete "=" sign in the following line!!!!
#AND flip the commented "times.append(curr_time)"
while curr_time < eTime:
#    times.append(curr_time)
    curr_time+=tDelta
    times.append(curr_time)

import ipdb; ipdb.set_trace()

#Group counts together by unit time
#index=0
#define array to hold spot count
spots=np.zeros(len(times))
#import ipdb; ipdb.set_trace()
cTime=sTime
endTime=cTime
#Read RBN data for given dates/times
#call function to get rbn data, find de_lat, de_lon, dx_lat, dx_lon for the data
rbn_df=rbn_lib.read_rbn(sTime, eTime, data_dir='data/rbn')
#create data frame for the loop
rbn_df2=rbn_df
#import ipdb; ipdb.set_trace()

while cTime < eTime:
    endTime += tDelta
   # import ipdb; ipdb.set_trace()
    #rbn_df2=rbn_df
    rbn_df2['Lower']=cTime
    rbn_df2['Upper']=endTime
    #import ipdb; ipdb.set_trace()
    #Clip according to the range of time for this itteration
    df2=rbn_df2[(rbn_df2.Lower <=rbn_df2.date) & (rbn_df2.date < rbn_df2.Upper)]
    #store spot count for the given time interval in an array 
    spots[index]=len(df2)
    #Itterate current time value and index
    cTime=endTime
    index=index+1

#create Data Frame from spots and times vectors
spot_df=pd.DataFrame(data=times, columns=['dates'])
spot_df['Count']=spots
#spot_df=pd.DataFrame(data=spots, columns=['Count'])
import ipdb; ipdb.set_trace()

#now isolate those on the day side
#now we need to constrain the data to those contacts that are only on the day side 
#will need to make this more elegant and universal
#I just wrote a quick code to isolate it for ONE EXAMPLE



#Plot figures
fig=plt.figure()#generate a figure
ax=fig.add_subplot(111)
ax.plot(spot_df['dates'], spot_df['Count'],'*-')

ax.set_title('RBN Spots per Unit Time\n'+sTime.strftime('%d %b %Y %H%M UT - ')+eTime.strftime('%d %b %Y %H%M UT'))
ax.set_ylabel('Spots/minute')
ax.set_xlabel('Time [UT]')
ax.text(spot_df.dates.min(),spot_df.Count.min(),'Unit Time: '+str(dt)+' '+unit)
#ax.text(spot_df.dates[10],spot_df.Count.max(),'Unit Time: '+str(dt)+' '+unit)

fig.tight_layout()
filename=os.path.join(output_dir, graphfile)
# 'rbnCount_5min_line1.png')
fig.savefig(filename)

#count=np.ones((len(df1['date']),1))


import ipdb; ipdb.set_trace()

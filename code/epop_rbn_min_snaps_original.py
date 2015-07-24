#!/usr/bin/env python
#This code is intended to download the RBN data from the ePOP Satellite pass on Field Day 2015
#and find the RBN recievers that heard the callsigns recorded by ePOP during from 0116-0118UT on 28 June 2015

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

#ePOP data input file
inPath="data/epop"
fname="Callsigns_7MHz.csv"
infile = os.path.join(inPath,fname)
print infile
#create output directory if none exists
output_dir='output/epop'
#handling.prepare_output_dirs({0:output_dir},clear_output_dirs=True)
#try: 
#    os.makedirs(output_dir)
#except:
#    pass 

#Output file
#specify data output file
csvfname='rbn_and_epop_calls_40m.csv'
outfile=os.path.join(output_dir,csvfname)
#ePOP and RBN Map output file
filename='ePOP_RBN_40m_zoom.jpg'
filepath    = os.path.join(output_dir,filename)
#output_path = os.path.join('output','firori')
#handling.prepare_output_dirs({0:output_path},clear_output_dirs=True)

#Time of ePOP pass
epop_sTime = datetime.datetime(2015,6,28,01,16)
epop_eTime = datetime.datetime(2015,6,28,01,18)
#sTime = datetime.datetime(2015,6,28,01,16,00)
#eTime = datetime.datetime(2015,6,28,01,16,30)

sTime=epop_sTime-datetime.timedelta(minutes=4)
eTime = epop_sTime + datetime.timedelta(minutes=10)
print sTime
print eTime
#import ipdb; ipdb.set_trace()
#Get RBN data 
rbn_df=rbn_lib.read_rbn(sTime, eTime,data_dir='data/rbn')

#Get epop callsign data
epop_df=pd.DataFrame.from_csv(infile)
import ipdb; ipdb.set_trace()

i=0
#callsign=epop_df.Call[i]
#print callsign
#import ipdb; ipdb.set_trace()
#df=pd.DataFrame(callsign, ['Callsign'])

#for n in range(0,len(rbn_df)-1):
#    if rbn_df.callsign[n]==callsign:
#        if n=0:
#            df=rbn_df[n]
#        else:
#            df=concat[df, rbn_df[n]]
#        ['Lat']=rbn_df.de_lat[n]
i=0
dx_call=[]
flag=False
for i in range(0,len(epop_df)-1):
#while i<len(epop_df):
    epopCall=epop_df.Call[i]
    print epopCall
    df_temp=rbn_df[rbn_df['dx']==epopCall]
    df_temp=df_temp[df_temp['band']=='40m']
    if df_temp.empty:
        print 'not heard'
#        import ipdb; ipdb.set_trace()
    else:
        dx_call.append(epopCall)

    if flag == False: 
        df=df_temp
        flag=True
    else:
        df=pd.concat([df, df_temp])
#
#    for n in range(0,len(rbn_df)-1):
#        k=1
#        df_temp=rbn_df[:k]
##        import ipdb; ipdb.set_trace()
#        if rbn_df.callsign.iloc[n]==epopCall and flag == False:
#            df_temp.columns=[rbn_df.iloc[n]
#            df['Callsign']=rbn_df.callsign.iloc[n]
#            df['freq']=rbn_df.freq.iloc[n]
#            df['dx_lat']=rbn_df.dx_lat.iloc[n]
##            df=rbn_df
#            import ipdb; ipdb.set_trace()
#            flag=True
#        elif rbn_df.callsign.iloc[n]==epopCall and flag == True:
#                df=concat[df, rbn_df.loc(n)]
##                import ipdb; ipdb.set_trace()
#


#end of loop

#Restrict rbn recievers to 40m 
df2=rbn_df[rbn_df['band']=='40m']

#Interval
import ipdb; ipdb.set_trace()
#df_temp=
#Export to text file
df.to_csv(outfile, index=False)

#Plot on map
### Determine the aspect ratio of subplot.
#xsize       = 8.0
#ysize       = 6.0
#nx_plots    = 1
#ny_plots    = 2
## Determine the aspect ratio of subplot.
xsize       = 6.5
ysize       = 5.5
nx_plots    = 2
ny_plots    = 2

#Define colors to plot the callsign contacts with
color_array=[(0.0, 0.75, 0.75), (0.0, 0.0, 1.0), (0.0, 0.5, 0.0), (0.75, 0.75, 0), (1.0, 0.0, 0.0), (0.75, 0, 0.75), (1, .75, .75), (.05, .25, .75), (.75, .25, .05), (.5, 1, .5), (1, .5, .5), (.5, .5, 1),(0.25, 0.5, 0.70), (0.75, 0.50, 0.25) , (0.75, 0.25, 0.50)]
#color_array=[(0.0, 0.75, 0.75), (0.0, 0.0, 1.0), (0.0, 0.5, 0.0), (0.75, 0.75, 0), (1.0, 0.0, 0.0), (0.75, 0, 0.75), (1, .75, .25), (.25, .75, 1), (.75, 1, .75), (.5, 1, .2), (0.75, 0.50, 0.25), (1, .2, .5), (.5, .5, 1),(0.25, 0.5, 0.70) , (0.75, 0.25, 0.50)]
#color_array=[(0.0, 0.75, 0.75), (0.0, 0.0, 1.0), (0.0, 0.5, 0.0), (0.75, 0.75, 0), (1.0, 0.0, 0.0), (0.75, 0, 0.75), (1, .75, .75), (.75, .75, 1), (.75, 1, .75), (.5, 1, .5), (1, .5, .5), (.5, .5, 1),(0.25, 0.5, 0.70), (0.75, 0.50, 0.25) , (0.75, 0.25, 0.50)]
dx_dict, dxlist=rbn_lib.set_dx_dict(dx_call, color_array)

fig         = plt.figure(figsize=(nx_plots*xsize,ny_plots*ysize)) # Create figure with the appropriate size.
subplot_nr  = 0 # Counter for the subplot
for kk,map_sTime in enumerate(map_times):
    plt_inx = kk + 1
    ax0     = fig.add_subplot(3,2,plt_inx)

    map_eTime = map_sTime + datetime.timedelta(minutes=15)

    print ''
    print '################################################################################'
    print 'Plotting RBN Map: {0} - {1}'.format(map_sTime.strftime('%d %b %Y %H%M UT'),map_eTime.strftime('%d %b %Y %H%M UT'))

    rbn_df  = rbn_lib.read_rbn(map_sTime,map_eTime,data_dir='data/rbn')

    # Figure out how many records properly geolocated.
    good_loc    = rbn_df.dropna(subset=['dx_lat','dx_lon','de_lat','de_lon'])
    good_count_map  = good_loc['callsign'].count()
    total_count_map = len(rbn_df)
    good_pct_map    = float(good_count_map) / total_count_map * 100.

    good_count      += good_count_map
    total_count     += total_count_map

    print 'Geolocation success: {0:d}/{1:d} ({2:.1f}%)'.format(good_count_map,total_count_map,good_pct_map)
    m,fig=rbn_lib.rbn_map_byDX(df,dx_dict, dxlist, legend=True,ax=ax0,tick_font_size=9,ncdxf=True, llcrnrlat=0,llcrnrlon=-135,urcrnrlon=45)
    rbn_lib.rbn_map_overlay(df2, m,ax=ax0, plot_paths=False, legend=False,scatter_rbn=True)
    title = map_sTime.strftime('%H%M - ')+map_eTime.strftime('%H%M UT')
    ax0.set_title(title)
    letter_prop = {'weight':'bold','size':20}
    ax0.text(.015,.90,'({0})'.format(letters[kk]),transform=ax0.transAxes,**letter_prop)

#fig = plt.figure(figsize=(8,6))
#Find ePOP RBN calls 
#ax0  = fig.add_subplot(1,1,1)
print 'dx_call='
print len(dx_call)
print 'color array='
print len(color_array)
import ipdb; ipdb.set_trace()

#dx_dict, dxlist=rbn_lib.set_dx_dict(dx_call, color_array)
#m,fig=rbn_lib.rbn_map_byDX(df,dx_dict, dxlist, legend=True,ax=ax0,tick_font_size=9,ncdxf=True, llcrnrlat=0,llcrnrlon=-135,urcrnrlon=45)
#rbn_lib.rbn_map_overlay(df2, m,ax=ax0, plot_paths=False, legend=False,scatter_rbn=True)

#leg=rbn_lib.dx_legend(dx_dict, dxlist)
#leg = rbn_lib.dx_legend(dx_dict, dxlist, fig=None,loc='center',bbox_to_anchor=[0.48,0.505],ncdxf=True,ncol=4)
#rbn_lib.rbn_map_byDX(df,dx_call, color_array, legend=True,ax=ax0,tick_font_size=9,ncdxf=True)
#rbn_lib.rbn_map_plot(df,legend=False,ax=ax0,tick_font_size=9,ncdxf=True)
fig.savefig(filepath,bbox_inches='tight')
fig.savefig(filepath[:-3]+'pdf',bbox_inches='tight')
plt.clf()
import ipdb; ipdb.set_trace()

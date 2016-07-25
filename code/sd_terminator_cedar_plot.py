#!/usr/bin/env python
#Generate rti plot with SD radar map to find terminator effects in the SD data. 
#Based on eclipse_superdarn_rbn_sw_fadeout_agu.py 

import sys
sys.path.append('/data/mypython')
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
import eclipse_lib

import rti_magda
from davitpy.pydarn.radar import *
from davitpy.pydarn.plotting import *
from davitpy.utils import *

from davitpy import pydarn
from pylab import gca
from matplotlib.patches import Polygon 

#Map Properties 
#define map projection 
mapProj='cyl'
llcrnrlon=-130 
llcrnrlat=25
urcrnrlon=-65
urcrnrlat=52 

x1=0.125
w1=0.775
h1=0.235
y1=0.6647
space=0.05
y2=y1+h1+space
map_ax=[[x1,y1, w1, h1], [x1, y2, w1, h1]]

#Define Eclipse Path limits
eLimits=['ds_NL.csv', 'ds_SL.csv']
#Define visual 
eColor=(0.75,0.25,0.5)
#pZorder is the zorder of the eclipse path with higher zorder=on top
pZorder=9

#define RBN alpha
#path_alpha=0.3
path_alpha=0.8

#Define SuperDARN radars want on the map 
#Note: Data for the RTI plot will be taken from beam of radars[0]
#radars=['fhw', 'fhe','cvw','cve']
radars=['fhw', 'cvw']

beam=7
beam=19
beam=21
#Define visual properties of Radars on the map 
fovColor=(0.5,0,0.75)
#fovZorder is the zorder of the FOV with higher zorder=on top
fovZorder=10

#Define Properties of RTI plots
#plot groundscatter in gray (True) or in color (False)
gs=False
#ax_dim=[0.125,0.099999,0.7, 0.22]
#ax_dim=[0.125,0.099999,0.77, 0.22]
ax_dim=[0.125,0.099999,0.78, 0.22]

##Freq plot dim
#fax_y=ax 
#fax_dim=[cax_x, ax_dim[1],cax_w, ax_dim[3]]

#cax_x=0.125+ax_dim[2]+.005
#cax_x=0.125+ax_dim[2]+.075
cax_x=0.125+ax_dim[2]+.055
#cax_w=0.08
#cax_w=0.075
cax_w=0.025
#cax_w=(1-cax_x-0.01)/2
cax_dim=[cax_x, ax_dim[1],cax_w, ax_dim[3]]
print ax_dim
print cax_dim
#Specify start and end time
sTime = datetime.datetime(2013,5,12)
eTime = datetime.datetime(2013,5,14)
sTime=datetime.datetime(2013,5,13,23,0)
#sTime=datetime.datetime(2013,3,13,23,0)
#sTime=datetime.datetime(2015,8,21,23,0)
sTime=datetime.datetime(2013,5,14,1,0)
eTime = sTime + datetime.timedelta(hours=5) #
eTime = sTime + datetime.timedelta(hours=7) #
#sTime = datetime.datetime(2014,9,10)
#eTime = datetime.datetime(2014,9,11)
sat_nr = 15

output_path = os.path.join('output','superdarn')
#handling.prepare_output_dirs({0:output_path},clear_output_dirs=True)
## Determine the aspect ratio of subplot.
xsize       = 8.0
ysize       = 6.0
nx_plots    = 1
ny_plots    = 2
ny_plots    = 1

for rad in radars:
    #filename='SD_RTI_Map_Terminator_'+radars[0]+'beam'+str(beam)+'_'+sTime.strftime('%Y%m%d_%H%M')+'-'+eTime.strftime('%Y%m%d_%H%M')+'.png'
    filename='CEDAR_SD_RTI_Map_Terminator_'+rad+'_beam'+str(beam)+'_'+sTime.strftime('%Y%m%d_%H%M')+'-'+eTime.strftime('%Y%m%d_%H%M')+'.png'
    filepath=os.path.join(output_path,filename)

    fig         = plt.figure(figsize=(nx_plots*xsize,ny_plots*ysize)) # Create figure with the appropriate size.
#    fig     = plt.figure()

    subplot_nr  = 0 # Counter for the subplot

    good_count  = 0
    total_count = 0

#    #Get the radar inforamtion (can give more information including maxgate and beam)
#    radar_path='hdw.dat.'+radars[0]
#    import ipdb; ipdb.set_trace()
#    #sitehdw = pydarn.radar.hdwRead(radar_path)
#    #sitehdw = hdwRead(radar_path)
#    #site    = pydarn.radar.network().getRadarByCode(rad).getSiteByDate(times[fplot][0])
#    site    = pydarn.radar.network().getRadarByCode(radars[0])
#    #rad_loc=[sitehdw['geolon'], sitehdw['geolat']] 

    map_times = []
    #map_times.append(sTime+timedelta(hours=1))
    map_times.append(sTime)
    map_times.append(eTime)
    #map_times.append(datetime.datetime(2013,5,13,16,5))
    #Sunrise/Sunset Times 
    #jd = getJD(sTime)
    #riseTime, setTime=calcSunRiseSetUTC( jd, rad_loc[1], rad_loc[0])
    #jd = getJD(eTime)
    #eriseTime, esetTime=calcSunRiseSetUTC( jd, rad_loc[1], rad_loc[0])

#    for kk,map_sTime in enumerate(map_times):
#        plt_inx = kk + 1
#        ax0     = fig.add_subplot(3,1,plt_inx)
#    #            ax0     = fig.add_axes(map_ax[plt_inx])
#        map_sTime = map_times[kk]
#        map_eTime = map_sTime + datetime.timedelta(minutes=15)
#
#
#        print ''
#        print '################################################################################'
#        print 'Plotting RBN Map: {0} - {1}'.format(map_sTime.strftime('%d %b %Y %H%M UT'),map_eTime.strftime('%d %b %Y %H%M UT'))
#
#    #    rbn_df  = rbn_lib.read_rbn_std(datetime.datetime(2013,5,13,16,5),map_eTime,data_dir='data/rbn')
#    #    rbn_df  = rbn_lib.read_rbn(datetime.datetime(2013,5,13,16,5),datetime.datetime(2013,5,13,16,20),data_dir='data/rbn')
#    #Created about 8 different 1 minute long pickle files in intial tests run (consider deleting)
#    #        #sTime=datetime.datetime(2013,5,13,23,0)with h= 4,5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2013,3,13,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2015,8,20,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2015,8,21,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        ##sTime=datetime.datetime(2013,5,14,1,0) with h= 4 eTime = sTime + datetime.timedelta(hours = h) #
#    #        ##sTime=datetime.datetime(2013,5,14,1,0) with h= 4 eTime = sTime + datetime.timedelta(hours = h) #
#        rbn_df  = rbn_lib.read_rbn(map_sTime,map_sTime + datetime.timedelta(minutes=1),data_dir='data/rbn')
#    #    rbn_df  = rbn_lib.read_rbn_std(map_sTime,map_eTime,data_dir='data/rbn')
#
#        # Figure out how many records properly geolocated.
#        good_loc    = rbn_df.dropna(subset=['dx_lat','dx_lon','de_lat','de_lon'])
#        good_count_map  = good_loc['callsign'].count()
#        total_count_map = len(rbn_df)
#
#        print ''
#        print '################################################################################'
#        print 'Plotting RBN Map: {0} - {1}'.format(map_sTime.strftime('%d %b %Y %H%M UT'),map_eTime.strftime('%d %b %Y %H%M UT'))
#
#    #    rbn_df  = rbn_lib.read_rbn_std(datetime.datetime(2013,5,13,16,5),map_eTime,data_dir='data/rbn')
#    #    rbn_df  = rbn_lib.read_rbn(datetime.datetime(2013,5,13,16,5),datetime.datetime(2013,5,13,16,20),data_dir='data/rbn')
#    #Created about 8 different 1 minute long pickle files in intial tests run (consider deleting)
#    #        #sTime=datetime.datetime(2013,5,13,23,0)with h= 4,5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2013,3,13,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2015,8,20,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        #sTime=datetime.datetime(2015,8,21,23,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        ##sTime=datetime.datetime(2013,5,14,1,0) with h= 4 eTime = sTime + datetime.timedelta(hours = h) #
#    #        ##sTime=datetime.datetime(2013,5,14,1,0) with h= 5 eTime = sTime + datetime.timedelta(hours = h) #
#    #        ##sTime=datetime.datetime(2013,5,14,1,0) with h= 7 eTime = sTime + datetime.timedelta(hours = h) #
#        rbn_df  = rbn_lib.read_rbn(map_sTime,map_sTime + datetime.timedelta(minutes=1),data_dir='data/rbn')
#    #    rbn_df  = rbn_lib.read_rbn_std(map_sTime,map_eTime,data_dir='data/rbn')
#
#        # Figure out how many records properly geolocated.
#        good_loc    = rbn_df.dropna(subset=['dx_lat','dx_lon','de_lat','de_lon'])
#        good_count_map  = good_loc['callsign'].count()
#        total_count_map = len(rbn_df)
#        good_pct_map    = float(good_count_map) / total_count_map * 100.
#
#        good_count      += good_count_map
#        total_count     += total_count_map
#
#        print 'Geolocation success: {0:d}/{1:d} ({2:.1f}%)'.format(good_count_map,total_count_map,good_pct_map)
#
#        # Go plot!!
#        m,fig=rbn_lib.rbn_map_plot(rbn_df,legend=False,ax=ax0,tick_font_size=9,ncdxf=True,llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, proj=mapProj, basemapType=False, eclipse=True,path_alpha=path_alpha)
#
##        #Plot SuperDARN Radars of interest on map (Fort Hayes West on the map)
##        for code in radars:
##            overlayRadar(m,fontSize=12,codes=code,dateTime=map_sTime)
###                overlayFov(m, codes=radars, maxGate=40, beams=beam)
##            overlayFov(m, codes=code, maxGate=40, beams=beam,model='GS', fovColor=fovColor,zorder=fovZorder)
#
#        #First plot radar with the beam shown in the FOV which we will plot RTI data from later (radars[0])
#        overlayRadar(m,fontSize=12,codes=rad,dateTime=map_sTime)
#        overlayFov(m, codes=rad, maxGate=40, beams=beam,model='GS', fovColor=fovColor,zorder=fovZorder)
#        
#        #end of loop
#        x,y, w, h=ax0.get_position().bounds
#        print "ax0 map 1-(x,y,width, height)="
#        print x,y,w,h
#        #If this is the first map plotted, then save the axis as ax1
#        if plt_inx==1:
#            ax1=ax0
#    #                w1=w
#    #                h1=h
#    #                ax0.set_position([x1,y1,w1,h1])
#    #            else: 
#    #                y2=0.05+y1+w1
#    #                w1=w
#    #                h1=h
#    #                ax0.set_position([x1,y2, w1, h1])
#    #
#        print ax0.get_position().bounds
#        print map_sTime
#        #Titles and other propertites
#        title = map_sTime.strftime('%H%M - ')+map_eTime.strftime('%H%M UT')
#        ax0.set_title(title,loc='center')
#        ax0.set_title(map_sTime.strftime('%d %b %Y'),loc='right')
#        if kk == 0:
#            ax0.set_title('Preflare',loc='left')
#        else:
#            ax0.set_title('Flare Peak',loc='left')
#
#        letter_prop = {'weight':'bold','size':20}
#    #            ax0.set_position(
#    #            ax0.text(.015,.90,'({0})'.format(letters[kk]),transform=ax0.transAxes,**letter_prop)
#
#    #            for item in (ax0.get_xticklabels() + ax0.get_yticklabels()):
#    #                item.set_fontsize(4)
#
#    #    print flare
#        print map_sTime
#
#    #        ax      = fig.add_subplot(3,1,3)
#    #ax.plot(inx,flare['B_AVG'],'o',label='{0} Class Flare @ {1}'.format(flare['class'],inx.strftime('%H%M UT')))
#    #        goes_map_sTime = datetime.datetime(inx.year,inx.month,inx.day)
#    #        goes_map_eTime = goes_map_sTime + datetime.timedelta(days=1)
#
#    #goes_sTime = datetime.datetime(2013,5,13,16) - datetime.timedelta(hours=2)
#    #goes_eTime = datetime.datetime(2013,5,13,16) + datetime.timedelta(hours=2)
#
#    #goes_data_map = gme.sat.read_goes(goes_sTime,goes_eTime,sat_nr=sat_nr)

    #Plot RTI plots for rad
    ax      = fig.add_axes(ax_dim)
    cax     =fig.add_axes(cax_dim)
    #rti_magda.plotRti(sTime=sTime, eTime=eTime, ax=ax, rad=radars[0], params=['power'],yrng=[0,40], gsct=gs, cax=cax, xtick_size=18,ytick_size=18)
    #rti_magda.plotRti(sTime=sTime, eTime=eTime, bmnum=beam, ax=ax, rad=radars[0], params=['power'], gsct=gs, cax=cax, xtick_size=18,ytick_size=18, plotTerminator=True)

##    rti_magda.plotRti(sTime=sTime, eTime=eTime, bmnum=beam, ax=ax, rad=radars[0], params=['power'],coords='geo', gsct=gs, cax=cax, xtick_size=18,ytick_size=18, plotTerminator=True)
    rti_magda.plotRti(sTime=sTime, eTime=eTime, bmnum=beam, ax=ax, rad=rad, params=['power'],coords='geo', gsct=gs, cax=cax, xtick_size=18,ytick_size=18, plotTerminator=True)
#    rti_magda.plotRti(sTime=sTime, eTime=eTime, bmnum=beam, ax=ax, rad=rad, params=['power'], gsct=gs, cax=cax, xtick_size=18,ytick_size=18)
    import ipdb; ipdb.set_trace()
    
    #rti_magda.plotRti(sTime=sTime, eTime=eTime, bmnum=beam, ax=ax, rad=radars[0], params=['power'], gsct=gs, cax=cax, xtick_size=18,ytick_size=18)

    # rti_magda.plotRti(sTime=goes_sTime, eTime=goes_eTime, ax=ax2, rad=radars[1], params=['power'])

    title_prop = {'weight':'bold','size':22}
#    #        fig.text(0.525,1.025,'HF Communication Paths',ha='center',**title_prop)
#    fig.text(0.525,1.000,'Reverse Beacon Network\nSolar Flare HF Communication Paths',ha='center',**title_prop)
#    #        fig.text(0.525,0.995,flare.name.strftime('%d %B %Y'),ha='center',size=18)
#
#    x0, y0, width, height = ax.get_position().bounds
#
#    ax_bounds = ax.get_position().bounds
#    print "ax0 map2-(x,y,width, height)=" 
#    #        print ax0_bounds
#
#    #Set position of Bottommost plot
#    width   = width #0.80
#    x0      = x0 #(1.-width) / 2. + 0.050
#    #        y0      = .050
#    y0      = y0 #.080
#    height  = height #0.200
#    ax.set_position([x0,y0,width,height])
#
#    #Set postion of maps
#    #Top Map
#    x1, y1, width1, height1= ax1.get_position().bounds
#    width1=width1
#    height1=height1
#    x1=x1
#    #increase shift to shift map down; decrease shift to shift map up
#    shift=0.030
#    y1 =1-shift-height1
#    ax1.set_position([x1,y1,width1, height1])
#    #Bottom Map
#    x2, y2, width2, height2= ax0.get_position().bounds
#    width2=width2
#    height2=height2
#    x2=x2
#    #increase shift to shift map down; decrease shift to shift map up
#    shift=0.0350+0.005
#    y2 = y1-shift-height2
#    #1-0.025-height2
#    ax0.set_position([x2,y2,width2, height2])
#
#    #Set Legend position
#    #        shift=0.070
#    shift=0.070+0.005
#    #wl is the width of the legend (right now it is an educated guess)
#    wl=0.025
#    #the lower left y coordinate of the legend (yl) is equal to the lower y coordinate of the bottom map minus the estimated legend width and the shift
#    yl=y2-shift-0.025
#    leg = rbn_lib.band_legend(fig,loc='center',bbox_to_anchor=[0.48,yl],ncdxf=True,ncol=4)
#
#    #Insert line between 
#    #        axl_h=0.0025
#    #        sh_axl_y=0.005#
#    #        sh_axl=(yl+y0+height)/2
#    #        axl_y=(yl+y0+height)/2
#    ##        axl_y=y0+height+sh_axl_y
#    ##        axl=fig.add_axes([x0,axl_y,width, axl_h])
#    ##        axl.set_visible(False)
#    #        plt.axhline(axl_y,xmin=0, xmax=0,hold=None,color= 'k', linewidth=2)
#    ##        axl(linspace(0,1,100), axl_y*ones([1,100]), 'k-')

    #ax.text(-0.0320,-0.140,flare.name.strftime('%d %b %Y'),transform=ax.transAxes,size=14)
    ax.set_xlabel('Time [UT]', size=18)
    #Set title of SuperDARN RTI PLOT
#    r=pydarn.radar.network().getRadarByCode(radars[0])
    r=pydarn.radar.network().getRadarByCode(rad)
    ax.set_title(r.name+' (Beam: '+str(beam)+')')
    #       # ax.text(.015,.90,'(e)',transform=ax.transAxes,**letter_prop)

    xticks  = []
    for x in range(7):
        xticks.append(sTime + datetime.timedelta(hours=(1*x)))
    ax.xaxis.set_ticks(xticks)

    ax.title.set_fontsize(title_prop['size'])
    #        ax.title.set_weight(title_prop['weight'])
    #
    #        ax.title.set_fontsize(18)
    ax.title.set_weight(title_prop['weight'])

    xticklabels = []
    #        ax.label.set_fontsize(18) 
    #        rcParams.update({'font.size':18})
    xfont={'size':18}
    for x,tick in enumerate(xticks):
        xticklabels.append(tick.strftime('%H%M'))
    ax.set_xticklabels(xticklabels, fontdict=xfont)
    for item in (ax.get_xticklabels()):
        item.set_fontsize(18)

    ax.vlines(map_times,0,1,linestyle='--',color='b')

    #        fig.tight_layout(h_pad=2.5,w_pad=3.5)
    fig.savefig(filepath,bbox_inches='tight')
    #fig.savefig(filepath[:-3]+'pdf',bbox_inches='tight')
    plt.clf()
#
#    good_pct = float(good_count)/total_count * 100.
#    print ''
#    print 'Final stats for: {0}'.format(filepath)
#    print 'Geolocation success: {0:d}/{1:d} ({2:.1f}%)'.format(good_count,total_count,good_pct)
#    #    except:
#    #        pass

print 'Plotting Success!'

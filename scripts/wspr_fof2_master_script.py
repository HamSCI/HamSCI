#!/usr/bin/env python
#This code is used to generate the RBN-GOES map for the Space Weather feature article.

import sys
import os
import datetime
import multiprocessing

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt

import numpy as np
import pandas as pd

import hamsci
from hamsci import wspr_lib
from hamsci import handling
# Set default gridsquare precision
gridsquare_precision = 4

def loop_info(map_sTime,map_eTime):
    print ''
    print '################################################################################'
    print 'Plotting WSPR Map: {0} - {1}'.format(map_sTime.strftime('%d %b %Y %H%M UT'),map_eTime.strftime('%d %b %Y %H%M UT'))

def write_csv_dct(run_dct):
    """
    Dictionary wrapper for write_csv() to help with
    pool multiprocessing.
    """

    csv_path    = write_csv(**run_dct)
    return csv_path

def create_wspr_obj_dct_wrapper(run_dct):
    create_wspr_obj(**run_dct)

def get_wspr_obj_path(output_dir,reflection_type,sTime,eTime):
    filename    = '{}-{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}.p'.format(reflection_type,sTime,eTime)
    output_dir  = os.path.join(wspr_fof2_dir,reflection_type)
    filepath    = os.path.join(output_dir,filename)
    return filepath

def create_wspr_obj(sTime,eTime,
        llcrnrlon=-180., llcrnrlat=-90, urcrnrlon=180., urcrnrlat=90.,
        call_filt_de = None, call_filt_dx = None,
        reflection_type         = 'sp_mid',
        wspr_fof2_dir            = 'data/wspr_fof2',
        **kwargs):

    #Create wspr object
    wspr_obj = wspr_lib.WsprObject(sTime,eTime) 

    #find lat/lon from gridsquares
    wspr_obj.active.dxde_gs_latlon()
    #Filter Path 
    wspr_obj.active.filter_pathlength(500.)

    #Calculate Reflection points
    wspr_obj.active.calc_reflection_points(reflection_type=reflection_type)
    wspr_obj.active.grid_data(gridsquare_precision)

    #filter lat/lon and calls 
    latlon_bnds = {'llcrnrlat':llcrnrlat,'llcrnrlon':llcrnrlon,'urcrnrlat':urcrnrlat,'urcrnrlon':urcrnrlon}
    wspr_obj.active.latlon_filt(**latlon_bnds)
    wspr_obj.active.filter_calls(call_filt_de,call_type='de')
    wspr_obj.active.filter_calls(call_filt_dx,call_type='dx')

    #Gridsquare data 
    wspr_obj.active.compute_grid_stats()
    with open(filepath,'wb') as fl:
        pickle.dump(rbn_obj,fl)


def wspr_map(sTime,eTime,
        llcrnrlon=-180., llcrnrlat=-90, urcrnrlon=180., urcrnrlat=90.,
        call_filt_de = None, call_filt_dx = None,
        reflection_type         = 'sp_mid',
        plot_de                 = True,
        plot_dx                 = True,
        plot_midpoints          = True,
        plot_paths              = False,
        plot_ncdxf              = False,
        plot_stats              = True,
        plot_legend             = True,
        overlay_gridsquares     = True,
        overlay_gridsquare_data = True,
        gridsquare_data_param   = 'f_max_MHz',
        fname_tag               = None,
        output_dir = 'output/wspr'):
    """
    Creates 
    """
    filename    = 'wspr_map-{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}.png'.format(sTime,eTime)
    filepath    = os.path.join(output_dir,filename)

    #Create wspr object
    wspr_obj = wspr_lib.WsprObject(sTime,eTime) 
    #find lat/lon from gridsquares
    wspr_obj.active.dxde_gs_latlon()
    wspr_obj.active.filter_pathlength(500.)
    wspr_obj.active.calc_reflection_points(reflection_type=reflection_type)
    latlon_bnds = {'llcrnrlat':llcrnrlat,'llcrnrlon':llcrnrlon,'urcrnrlat':urcrnrlat,'urcrnrlon':urcrnrlon}
    wspr_obj.active.latlon_filt(**latlon_bnds)

    # Go plot!! ############################ 
    ## Determine the aspect ratio of subplot.
    xsize       = 15.0
    ysize       = 6.5
    nx_plots    = 1
    ny_plots    = 1

    rcp = mpl.rcParams
    rcp['axes.titlesize']     = 'large'
#    rcp['axes.titleweight']   = 'bold'

    fig        = plt.figure(figsize=(nx_plots*xsize,ny_plots*ysize))
    ax0        = fig.add_subplot(1,1,1)

    map_obj=wspr_lib.WsprMap(wspr_obj, ax=ax0,nightshade=term[0], solar_zenith=term[1], default_plot=False)
    if plot_de:
        map_obj.plot_de()
    if plot_dx:
        map_obj.plot_dx()
    if plot_midpoints:
        map_obj.plot_midpoints()
    if plot_paths:
        map_obj.plot_paths()
    if plot_ncdxf:
        map_obj.plot_ncdxf()
    if plot_stats:
        map_obj.plot_link_stats()
    if plot_legend:
        map_obj.plot_band_legend(band_data=map_obj.band_data)

    if overlay_gridsquares:
        map_obj.overlay_gridsquares()
    if overlay_gridsquare_data:
        wspr_obj.active.grid_data(gridsquare_precision)
        wspr_obj.active.compute_grid_stats()
        map_obj.overlay_gridsquare_data(param=gridsquare_data_param)

    ecl         = hamsci.eclipse.Eclipse2017()
    line, lbl   = ecl.overlay_umbra(map_obj.m,color='k')
    handles     = [line]
    labels      = [lbl]

    fig.savefig(filepath,bbox_inches='tight')
    plt.close(fig)

def gen_map_run_list(sTime,eTime,integration_time,interval_time,**kw_args):
    dct_list    = []
    this_sTime  = sTime
    while this_sTime+integration_time <= eTime:
        this_eTime   = this_sTime + integration_time

        tmp = {}
        tmp['sTime']    = this_sTime
        tmp['eTime']    = this_eTime
        tmp.update(kw_args)
        dct_list.append(tmp)

#        this_sTime      = this_sTime + interval_time
        this_sTime  = this_eTime

    return dct_list


def wspr_map_dct_wrapper(run_dct):
    wspr_map(**run_dct)

if __name__ == '__main__':
    multiproc   = False 
    plot_de                 = True
    plot_dx                 = False
    plot_midpoints          = False
    plot_paths              = False
    plot_ncdxf              = False
    plot_stats              = True
    plot_legend             = False
    overlay_gridsquares     = True
    overlay_gridsquare_data = True
#    gridsquare_data_param   = 'f_max_MHz'
    gridsquare_data_param   = 'foF2'
    fname_tag               = None
    #Initial WsprMap test code
    sTime = datetime.datetime(2016,11,1,22)
    eTime = datetime.datetime(2016,11,2,1)
    sTime = datetime.datetime(2016,11,1)
    eTime = datetime.datetime(2016,11,1,1)
    #CW Sweapstakes 2014
    sTime = datetime.datetime(2014, 11,1)
    eTime = datetime.datetime(2014, 11,4)
#    eTime = datetime.datetime(2014, 11,2)
#    #CW Sweapstakes 2016
#    sTime = datetime.datetime(2016, 11,5)
#    eTime = datetime.datetime(2016, 11,7)
#    #Test CW Sweapstakes 2016
#    sTime = datetime.datetime(2016, 11,4)
#    eTime = datetime.datetime(2016, 11,7)


#    #Solar Flare Event
##    sTime = datetime.datetime(2016,5,13,15,5)
##    eTime = datetime.datetime(2016,5,13,15,21)
#    sTime = datetime.datetime(2013,5,13,15,5)
#    eTime = datetime.datetime(2013,5,13,17)

#    wspr_obj = wspr_lib.WsprObject(sTime,sTime+datetime.timedelta(minutes=15)) 
#    import ipdb; ipdb.set_trace()

    term=[True, False]
    integration_time    = datetime.timedelta(minutes=15)
    interval_time       = datetime.timedelta(minutes=60)

    dct = {}
    dct.update({'llcrnrlat':20.,'llcrnrlon':-130.,'urcrnrlat':55.,'urcrnrlon':-65.})

    filt_type='sp_mid'
    filt_type='miller2015'
    reflection_type = filt_type

    map_sTime = sTime
#    map_eTime = map_sTime + datetime.timedelta(minutes = dt)
    map_eTime = map_sTime + interval_time
    map_eTime = map_sTime + integration_time

    #Create output directory based on start and end time and parameter ploted
    event_dir               = '{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}-{}'.format(sTime,eTime,reflection_type)
    output_dir              = os.path.join('output','wspr',event_dir)
    wspr_fof2_dir            = os.path.join('data','wspr_fof2',event_dir)

    dct['output_dir']       = output_dir
#    dct['wspr_fof2_dir']     = wspr_fof2_dir
    dct['reflection_type']  = reflection_type

#    #Create output directory based on start and end time and parameter ploted
#    event_dir           = '{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}'.format(sTime,eTime)
##    filename    = '{}-{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}.png'.format(fname_tag,sTime,eTime)
#    if plot_midpoints:
#        if reflection_type == 'miller2015':
#            tag = 'refl_points'
##            output_dir = os.path.join('output','wspr','maps','refl_points',event_dir)
#        if reflection_type == 'sp_mid':
#            tag='midpoints'
#    if plot_paths: 
#        tag = 'paths'
##        output_dir          = os.path.join('output','wspr','maps','paths',event_dir)
#    if overlay_gridsquare_data:
#        if gridsquare_data_param   == 'foF2':
#            tag='fof2'
##            output_dir          = os.path.join('output','wspr','maps','fof2',event_dir)
#        else:
#            tag = 'gridsqs'
##            output_dir          = os.path.join('output','wspr','maps','gridsqs',event_dir)
#    output_dir          = os.path.join('output','wspr','maps',event_dir, tag)
#
##    output_dir          = os.path.join('output','wspr','maps','paths',event_dir)
##    output_dir          = os.path.join('output','wspr','maps','midpoints',event_dir)
##    output_dir          = os.path.join('output','wspr','maps','refl_points',event_dir)
##    output_dir          = os.path.join('output','wspr','maps','defaults_test','midpoints',event_dir)
##    output_dir          = os.path.join('output','wspr','maps','defaults_test','refl_points',event_dir)
#
    try:    # Create the output directory, but fail silently if it already exists
        os.makedirs(output_dir) 
    except:
        pass

# Create input parameter dictionary 
#    dct.update({'filt_type':filt_type})
    dct.update({'reflection_type':filt_type})
    dct.update({'output_dir':output_dir})
    dct.update({'plot_de':plot_de, 'plot_dx':plot_dx, 'plot_midpoints':plot_midpoints, 'plot_paths':plot_paths, 'plot_ncdxf': plot_ncdxf, 'plot_stats':plot_stats, 'plot_legend':plot_legend, 'overlay_gridsquares':overlay_gridsquares, 'overlay_gridsquare_data':overlay_gridsquare_data, 'gridsquare_data_param':gridsquare_data_param, 'fname_tag':fname_tag})

    #Generate list of input values for every interval to plot 
    run_list    = gen_map_run_list(sTime,eTime,integration_time,interval_time,**dct)
#    run_list    = gen_map_run_list(map_sTime,map_eTime,integration_time,interval_time,**dct)
    
    #Run map code
    if multiproc:
        pool = multiprocessing.Pool()
        pool.map(wspr_map_dct_wrapper,run_list)
        pool.close()
        pool.join()
    else:
        for run_dct in run_list:
            wspr_map_dct_wrapper(run_dct)


#    wspr_path_map(map_sTime, map_eTime, filt_type = filt_type, output_dir=output_dir, **dct)


#    wspr_map.fig.savefig('output/wspr/WSPR_map_test.png')

#Adapted test code 
#    sTime = datetime.datetime(2016,11,1,0)
#    eTime = datetime.datetime(2016,11,1,1)
#    term=[True, False]
#    dt=15
#    integration_time    = datetime.timedelta(minutes=15)
#    interval_time       = datetime.timedelta(minutes=20)
##    interval_time       = datetime.timedelta(minutes=60)
#
#    dct = {}
#    dct.update({'llcrnrlat':20.,'llcrnrlon':-130.,'urcrnrlat':55.,'urcrnrlon':-65., 'filt_type':'sp_mid'})
##    dct.update({'llcrnrlat':20.,'llcrnrlon':-130.,'urcrnrlat':55.,'urcrnrlon':-65., 'output_dir': 'output/wspr'})
#
#    map_sTime = sTime
##    map_eTime = map_sTime + datetime.timedelta(minutes = dt)
#    map_eTime = map_sTime + interval_time
#
#    run_list            = gen_map_run_list(map_sTime,map_eTime,integration_time,interval_time,**dct)
#    if multiproc:
#        pool = multiprocessing.Pool()
#        pool.map(wspr_map_dct_wrapper,run_list)
#        pool.close()
#        pool.join()
#    else:
#        for run_dct in run_list:
#            wspr_map_dct_wrapper(run_dct)
#
##    wspr_map.fig.savefig('output/wspr/WSPR_map_test2.png')
#
##    mymap = wspr_map(sTime = map_sTime, eTime = map_eTime)

#Other?
#    dct = {}
#    dct.update({'llcrnrlat':20.,'llcrnrlon':-130.,'urcrnrlat':55.,'urcrnrlon':-65.})
#
#    integration_time    = datetime.timedelta(minutes=15)
#    interval_time       = datetime.timedelta(minutes=60)
#
#    event_dir           = '{:%Y%m%d.%H%M}-{:%Y%m%d.%H%M}'.format(sTime,eTime)
#    output_dir          = os.path.join('output','maps',event_dir)

#General Test Code
#    sTime = datetime.datetime(2016,11,1)
#    wspr_obj = wspr_lib.WsprObject(sTime) 
#    wspr_obj.active.calc_reflection_points(reflection_type='miller2015')
#    #For iPython
##    os.system('sudo python setup.py install')
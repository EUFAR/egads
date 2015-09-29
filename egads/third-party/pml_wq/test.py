#!/usr/bin/env python
import datetime
import os
import pml_wq


main_dir = os.path.dirname( os.path.realpath(__file__) )

im_fname = main_dir + '/test_data/e233a011b_atc_fix_vis.mapped.bil'
out_dir = main_dir + '/test_data/'

# Chl-a
pml_wq.chlor_a(im_fname,out_dir,'git')
pml_wq.chlor_a(im_fname,out_dir,'oc4')

# TSM
pml_wq.tsm(im_fname,out_dir,'nechad')

# IOP
im_fname = main_dir + '/test_data/e233a011b_atc_var_vis.mapped-downsampled.bil'
lat = 46.839528
lon = 17.720718
date_time = '21-08-2010 10:08:53'
im_date_time = datetime.datetime.strptime(date_time, "%d-%m-%Y %H:%M:%S%f")
pml_wq.iop(im_fname,out_dir,im_date_time,lat,lon)
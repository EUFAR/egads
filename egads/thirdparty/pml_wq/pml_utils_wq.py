import numpy as np
import scipy
import os
import time
import commands
import string
import re
import pdb

import pml_utils_io



#===================================================================================================================================
# Julian day 
def julian(day,month,year):
  t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
  jul = time.gmtime(t)[7]
  return jul


#===================================================================================================================================
# Water detection 
# Based on low reflection from water adn high reflection from land at around 875nm
def water_mask(im_dset,im_wl):
  
  water_threshold = 800.
  #water_threshold = 0.08

  # Select bands
  bands = [875.]
  #bands = [772.]
  sel_band_ind,sel_band_val = pml_utils_io.select_bands(im_wl,bands)

  #pdb.set_trace() 

  # Load bands
  im_data = pml_utils_io.get_image_raster(im_dset,[sel_band_ind[0]])

  water_mask = np.logical_or( im_data[:,:,0]>water_threshold , im_data[:,:,0]<=0 )

  return water_mask



#===================================================================================================================================
#----------------------------------------------------------------------------
# Gitelson 2007 for medium to high Chl concentrations.
#
# Inputs:
#   Rrs675    remote sensing reflectance for wavelength 675nm
#   Rrs695    remote sensing reflectance for wavelength 695nm
#   Rrs730    remote sensing reflectance for wavelength 730nm
#
# Outputs:
#   Chlorophyll a (Chla)
# Remark: Rrs can be replaced with Rw with the same result
#----------------------------------------------------------------------------
def gitelson(Rrs675, Rrs695, Rrs730):

  ind_nonzero = np.logical_and((Rrs675>1E-10),(Rrs695>1E-10))

  chla = np.empty_like(Rrs730)
  chla[:] = -9999
  chla[ind_nonzero] = 10.14 + 178.9 * Rrs730[ind_nonzero] * ( 1./Rrs675[ind_nonzero] - 1./Rrs695[ind_nonzero] ) 

  return chla


#----------------------------------------------------------------------------
# OC4 for low Chl concentrations
#
#   Inputs:
#             Rrs443 - remote sensing reflectance for wavelength 443nm
#             Rrs489
#             Rrs510
#             Rrs555
#
#   Outputs:
#	     Chl
# Remark: Rrs can be replaced with Rw with the same result	
#----------------------------------------------------------------------------
def oc4v6(Rrs443, Rrs489, Rrs510, Rrs555):

  ind_nonzero = (Rrs555>1E-10)

  # Choose maximum out of Rrs443, Rrs489 or Rrs510
  R1 = np.amax(zip(Rrs443,Rrs489,Rrs510),axis=1)

  # Compute X=log10(Rrs1/Rrs555)
  X = np.empty_like(Rrs555)
  X[:] = -9999
  X[ind_nonzero] = np.log10(R1[ind_nonzero]/Rrs555[ind_nonzero])

  # Compute Chl
  p = 0.3272 - 2.9940*X + 2.7218*X*X - 1.2259*X*X*X - 0.5683*np.power(X,4)
  Chl = np.power(10,p)
  
  return Chl



#===================================================================================================================================
#----------------------------------------------------------------------------
# Nechad 2010 TSM algorithm
#
#   Inputs:
#            im_dset - gdal image dataset
#            im_wl - a list of image wavelengths  
#   Outputs:
#	     TSM concentration
#----------------------------------------------------------------------------
def nechad_tsm(im_dset,im_wl):

  # Select bands
  tsm_bands = [710.]
  sel_band_ind,sel_band_val = pml_utils_io.select_bands(im_wl,tsm_bands)

  # Load bands
  im_data = pml_utils_io.get_image_raster(im_dset,sel_band_ind)

  # Interpolate bands
  ip_fun = scipy.interpolate.interp1d(sel_band_val,im_data,axis=2,kind='linear',bounds_error=False,fill_value=-9999.)
  interp_im_data = ip_fun(tsm_bands)

  # Calculation
  Rw710 = interp_im_data[:,:,0]*0.0001
  #Rw710 = interp_im_data[:,:,0]*1.

  Ap = 561.94
  Bp = 1.23
  Cp = 0.1892

  S = Ap*Rw710*(1-Rw710/Cp)+Bp

  return S
   



#===================================================================================================================================
# IOP model
def iop(im_dset,im_wl,date_time,lat,lon,water_mask):

  model_dir = os.path.dirname( os.path.realpath(__file__) ) + '/iop_model/'
  
  # ------------------------------------------
  # set model dir as your current dir
  current_dir = os.getcwd()
  os.chdir(model_dir)


  # Select bands
  bands = [412.,443.,490.,510.,555.,670.]
  sel_band_ind,sel_band_val = pml_utils_io.select_bands(im_wl,bands)

  # Load bands
  im_data = pml_utils_io.get_image_raster(im_dset,sel_band_ind)

  # Interpolate IOP bands
  ip_fun = scipy.interpolate.interp1d(sel_band_val,im_data,axis=2,kind='linear',bounds_error=False,fill_value=-9999.)
  interp_im_data = ip_fun(bands)

  # Rw calculation
  Rw = interp_im_data*0.0001

  # Calculate sun angle
  # sun_theta = `sun_angle $lat $lon $year $jday[1] $gmt`
  jday = julian(date_time.day,date_time.month,date_time.year)
  cmd_str = model_dir+'sun_angle ' + \
            str(lat) + ' ' + str(lon) + ' ' + str(date_time.year) + ' ' + str(jday) + ' ' + str(date_time.hour + date_time.minute/60.) 
  sun_theta_str = commands.getoutput(cmd_str)

  res = []
  no_data_res = ['0.0']*24


  for i in xrange(Rw.shape[0]):
    for j in xrange(Rw.shape[1]):
      if water_mask[i,j]:
        # In case of land or no data
        res.append(no_data_res)
      else:
        # Calculate iop output without noise 
        cmd_str = model_dir+'pml_iop_model_test' + \
                  ' -config '+model_dir+'config/pml_acc.cfg' + \
                  ' -sun_theta ' + sun_theta_str + \
                  ' -sen_theta ' + '0.83053' + \
                  ' -dphi '+ '1.57' + \
                  ' -rhow'
        for r in xrange(Rw.shape[2]): cmd_str = cmd_str+' '+str(Rw[i,j,r]) 

        # process and store IOP model output
        r = commands.getoutput(cmd_str)    
        rp = string.strip(r,' \t\n')   
           
        res.append(re.split('\s+',rp)) 

    print "%i/%i"%(i,Rw.shape[0])

  ares = np.array(res,dtype=float)

  a = ares[:,:6]
  ady = ares[:,6:12]
  ap = ares[:,12:18]
  bbp = ares[:,18:24]

  a_ = a.reshape((Rw.shape[0],Rw.shape[1],6))
  ady_ = ady.reshape((Rw.shape[0],Rw.shape[1],6))
  ap_ = ap.reshape((Rw.shape[0],Rw.shape[1],6))
  bbp_ = bbp.reshape((Rw.shape[0],Rw.shape[1],6))

  # return to the original working directory
  os.chdir(current_dir)

  return (a_,ady_,ap_,bbp_)

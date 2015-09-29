import gdal
import gdalconst
import numpy as np
import scipy.interpolate
import os
import pdb

import pml_utils_io
import pml_utils_wq


# ----------------------------------------------------------------------------------------------------------------------
# Chl-a algorithms
def chlor_a(im_fname, out_dir, alg_name):  
  # Load image
  im_dset = gdal.Open(im_fname, gdalconst.GA_ReadOnly)
  im_wl = pml_utils_io.get_ATCOR_image_wavelength(im_dset)
  
  # Process data
  if alg_name=='git':
    # Gitelson Chl-a

    # Select bands
    git_bands = [675.,695.,730.]              
    sel_band_ind,sel_band_val = pml_utils_io.select_bands(im_wl,git_bands)

    # Load bands
    im_data = pml_utils_io.get_image_raster(im_dset,sel_band_ind)

    # Interpolate Gitelson bands
    ip_fun = scipy.interpolate.interp1d(sel_band_val,im_data,axis=2,kind='linear',bounds_error=False,fill_value=-9999.)
    interp_im_data = ip_fun(git_bands)

    # Gitelson calculation for Rrs
    chla = pml_utils_wq.gitelson(interp_im_data[:,:,0], interp_im_data[:,:,1], interp_im_data[:,:,2])

  elif alg_name=='oc4':
    # OC4 Chl-a

    # Select bands
    oc4_bands = [443.,489.,510.,555.]    
    sel_band_ind,sel_band_val = pml_utils_io.select_bands(im_wl,oc4_bands)

    # Load bands
    im_data = pml_utils_io.get_image_raster(im_dset,sel_band_ind)

    # Interpolate OC4 bands
    ip_fun = scipy.interpolate.interp1d(sel_band_val,im_data,axis=2,kind='linear',bounds_error=False,fill_value=-9999.)
    interp_im_data = ip_fun(oc4_bands)

    # OC4 calculation
    chla = pml_utils_wq.oc4v6(interp_im_data[:,:,0], interp_im_data[:,:,1], interp_im_data[:,:,2], interp_im_data[:,:,3])

  else:
    print "ERROR: unknown name for chl-a algorithm ($s)"%alg_name
    raise

  
  # Apply water mask
  water_mask = pml_utils_wq.water_mask(im_dset,im_wl)
  chla[water_mask] = 0.

  # ------------------------------------------------------------------------------------------
  # Write down results
  out_fname = os.path.join(out_dir,'chl_'+alg_name+'_'+os.path.basename(im_fname))
  pml_utils_io.write_envi_image(out_fname,chla,im_dset)
  
  
  
  
# -------------------------------------------------------------------------------------------------------------------------------------
# TSM algorithms
def tsm(im_fname, out_dir, alg_name):
  # Load image
  im_dset = gdal.Open(im_fname, gdalconst.GA_ReadOnly)
  im_wl = pml_utils_io.get_ATCOR_image_wavelength(im_dset)

  # ------------------------------------------------------------------------------------------
  if alg_name=='nechad':
    # Nechad2010 TSM
    tsm = pml_utils_wq.nechad_tsm(im_dset,im_wl)
     
  else:
    print "ERROR: unknown algorithm name."
    raise

  # Apply water mask
  water_mask = pml_utils_wq.water_mask(im_dset,im_wl)
  tsm[water_mask] = 0.

  # Write down results
  out_fname = os.path.join(out_dir,'tsm_'+alg_name+'_'+os.path.basename(im_fname))
  pml_utils_io.write_envi_image(out_fname,tsm,im_dset)




# -------------------------------------------------------------------------------------------------------------------------------------
# IOP algorithm
def iop(im_fname, out_dir, im_date_time, lat, lon):
  
  # ------------------------------------------------------------------------------------------
  # Load image
  im_dset = gdal.Open(im_fname, gdalconst.GA_ReadOnly)
  im_wl = pml_utils_io.get_ATCOR_image_wavelength(im_dset)

  # ------------------------------------------------------------------------------------------
  # Calculate water mask
  water_mask = pml_utils_wq.water_mask(im_dset,im_wl)


  # ------------------------------------------------------------------------------------------
  # PML IOP model
  a,ady,ap,bbp = pml_utils_wq.iop(im_dset,im_wl,im_date_time,lat,lon,water_mask)

  # ------------------------------------------------------------------------------------------
  # Write down results
  bands = [412.,443.,490.,510.,555.,670.]
  for i,band in enumerate(bands):
    out_fname = os.path.join(out_dir,'atot('+'%i'%int(band)+')_PMLiop_'+os.path.basename(im_fname))
    pml_utils_io.write_envi_image(out_fname,a[:,:,i],im_dset)

    out_fname = os.path.join(out_dir,'bbp('+'%i'%int(band)+')_PMLiop_'+os.path.basename(im_fname))
    pml_utils_io.write_envi_image(out_fname,bbp[:,:,i],im_dset)

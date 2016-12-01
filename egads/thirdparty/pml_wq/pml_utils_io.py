import numpy as np
import struct
import gdal
import gdalconst




# Select neighbour bands from the list
# We assume that all_bands are ordered from low to high values !!!
def select_bands(all_bands,sel_bands):

  out_band_val = []
  out_band_ind = []

  out_band = {}

  for sband in sel_bands:
    
    found = False

    for i in xrange(len(all_bands)-1):
      if sband>=all_bands[i] and sband<=all_bands[i+1]:
        out_band[all_bands[i]] = i
        out_band[all_bands[i+1]] = i+1
        found = True

    if not found: return ([],[])

  for key in sorted(out_band.iterkeys()):
    out_band_val.append(key)
    out_band_ind.append(out_band[key])

  return (out_band_ind,out_band_val)



# get wavelength from ATCOR image metadata 
def get_ATCOR_image_wavelength(dataset): 
  meta = dataset.GetMetadata()
  wavelength = np.zeros(dataset.RasterCount,float)

  for k,v in meta.iteritems():
    ind = int(float(k.split("_")[1]))-1  

    #val = float(v.split('(')[-1].split(' ')[0])*1000.
    val = float(v.split(" ")[0]) 
    wavelength[ind] = val

  return wavelength



# returns an image array a[rows,cols,bands] for selected bands
def get_image_raster(dataset,band_num,downsample=None):

  xnum = dataset.RasterXSize
  ynum = dataset.RasterYSize
  znum = len(band_num)

  data = np.zeros((ynum,xnum,znum),dtype=float)

  for i,bn in enumerate(band_num):
    band = dataset.GetRasterBand(bn+1)
    scanval = band.ReadRaster(0,0,xnum,ynum,xnum,ynum,gdalconst.GDT_Float32) 

    if not scanval: 
      data[:,:,i] = -9999. 
      continue
    else:  
      data[:,:,i] = np.array(struct.unpack(xnum*ynum*'f', scanval),float).reshape((ynum,xnum))

  if downsample==None or downsample==1: 
    return data
  else: 
    return data[::downsample,::downsample,:]



# write an image of one band
def write_envi_image(file_name,data,im_dset):
  ynum = data.shape[0]
  xnum = data.shape[1]

  format = 'ENVI'
  driver = gdal.GetDriverByName( format )

  dst_ds = driver.Create(file_name, xnum, ynum, 1, gdal.GDT_Float32)

  dst_ds.SetGeoTransform(im_dset.GetGeoTransform())
  dst_ds.SetProjection(im_dset.GetProjection())

  dst_ds.GetRasterBand(1).WriteArray(data)

  dst_ds = None   

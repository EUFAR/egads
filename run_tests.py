#!/usr/bin/env python
"""
Launcher to test EGADS functionality and installation of required libraries.

"""
import sys

import egads

# required libraries check
try:
    import numpy
except:
    sys.stderr.write('Error: Numpy installation not found. You must install Numpy before EGADS can be used. See INSTALL.txt for more info. \n')
else:
    print 'Numpy installation ... ok'

try:
   import scipy
except:
   sys.stderr.write('Error: Scipy installation not found. You must install Scipy before EGADS can be used. See INSTALL.txt for more info. \n')
else:
   print 'Scipy installation ... ok'

min_version_netCDF4 = '0.8.2'
try:
    import netCDF4
    if netCDF4.__version__ != '0.8.2':
        sys.stderr.write('Warning: netCDF4 library version ' + netCDF4.__version__ + ' found. It is recommended that netCDF4 version 0.8.2 be used.')
except:
    sys.stderr.write('Error: netCDF4 installation not found. YYou must install the netCDF4 library before using EGADS. See INSTALL.txt for more info. \n')
else:
    print 'netCDF4 installation ... ok'

try:
    import nappy
except:
    sys.stderr.write('NaPPy should have been installed with your EGADS installation, but it could not be found. You may need to install it independently. See INSTALL.txt fore more info. \n')
else:
    print 'NaPPy installation ... ok'

# EGADS test protocol
print ' '
egads.test()



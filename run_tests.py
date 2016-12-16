#!/usr/bin/env python
"""
Launcher to test EGADS functionality and installation of required libraries.
"""
import sys
import egads


# required libraries check
try:
    import numpy  # @UnusedImport
except:
    sys.stderr.write('Error: Numpy installation not found. You must install Numpy before EGADS can be used. See INSTALL.txt for more info.\n')
else:
    print 'Numpy installation ... ok'

try:
    import scipy  # @UnusedImport
except:
    sys.stderr.write('Error: Scipy installation not found. You must install Scipy before EGADS can be used. See INSTALL.txt for more info.\n')
else:
    print 'Scipy installation ... ok'

try:
    from distutils.version import LooseVersion
    import netCDF4
    if LooseVersion(netCDF4.__version__) < LooseVersion("1.1.9"):
        sys.stderr.write('Warning: netCDF4 library version ' + netCDF4.__version__ + ' found. It is recommended that netCDF4 version 1.1.9 or greater be used.')
except:
    sys.stderr.write('Error: netCDF4 installation not found. You must install the netCDF4 library before using EGADS. See INSTALL.txt for more info.\n')
else:
    print 'netCDF4 installation ... ok'
    
try:
    import nappy  # @UnresolvedImport
    nappy_path = nappy.__path__
    if '/thirdparty/' in str(nappy_path):
        print 'nappy in third party directory ... ok'
    else:
        print 'Warning: egads.test() has detected that Nappy hasn''t been imported from EGADS directory. Nappy is an old module and few critical fixes have been included in EGADS embedded version. Issues linked to Numpy can occure if an old version of Nappy is used.'
except:
    sys.stderr.write('Error: nappy module not found. Nappy should be included in the thirdparty directory of EGADS. Please correct that issue before using EGADS')


# EGADS test protocol
print ''
egads.test()

#!/usr/bin/env python
"""
Launcher to test EGADS functionality and installation of required libraries.
"""
import sys
import egads
import logging

logging.debug('egads.run_tests invoked')
# required libraries check
try:
    import numpy
except:
    sys.stderr.write('Error: Numpy installation not found. You must install Numpy before EGADS can be used. See INSTALL.txt for more info.\n')
    logging.exception('Error: Numpy installation not found. You must install Numpy before EGADS can be used. See INSTALL.txt for more info.')
else:
    print 'Numpy installation ... ok'

try:
    import scipy
except:
    sys.stderr.write('Error: Scipy installation not found. You must install Scipy before EGADS can be used. See INSTALL.txt for more info.\n')
    logging.exception('Error: Scipy installation not found. You must install Scipy before EGADS can be used. See INSTALL.txt for more info.')
else:
    print 'Scipy installation ... ok'

try:
    from distutils.version import LooseVersion
    import netCDF4
    if LooseVersion(netCDF4.__version__) < LooseVersion("1.1.9"):
        sys.stderr.write('Warning: netCDF4 library version ' + netCDF4.__version__ + ' found. It is recommended that netCDF4 version 1.1.9 or greater be used.')
        logging.warning('Warning: netCDF4 library version ' + netCDF4.__version__ + ' found. It is recommended that netCDF4 version 1.1.9 or greater be used.')
except:
    sys.stderr.write('Error: netCDF4 installation not found. You must install the netCDF4 library before using EGADS. See INSTALL.txt for more info.\n')
    logging.exception('Error: netCDF4 installation not found. You must install the netCDF4 library before using EGADS. See INSTALL.txt for more info.')
else:
    print 'netCDF4 installation ... ok'
    
try:
    import nappy  # @UnresolvedImport
    nappy_path = nappy.__path__
    if '/thirdparty/' in str(nappy_path):
        print 'nappy in third party directory ... ok'
    else:
        print 'Warning: egads has detected that Nappy hasn''t been imported from EGADS directory. Nappy is an old module and few critical fixes have been included in EGADS embedded version. Issues linked to Numpy can occure if an old version of Nappy is used.'
        logging.warning('Warning: egads has detected that Nappy hasn''t been imported from EGADS directory. Nappy is an old module and few critical fixes have been included in EGADS embedded version. Issues linked to Numpy can occure if an old version of Nappy is used.')
except:
    sys.stderr.write('Error: nappy module not found. Nappy should be included in the thirdparty directory of EGADS. Please correct that issue before using EGADS')
    logging.exception('Error: nappy module not found. Nappy should be included in the thirdparty directory of EGADS. Please correct that issue before using EGADS')
    
try:
    import quantities
    quantities_path = quantities.__path__
    if '/thirdparty/' in str(quantities_path):
        print 'quantities in third party directory ... ok'
    else:
        print 'Warning: egads has detected that Quantities hasn''t been imported from EGADS directory. Quantities showed few compatibility issues with Numpy, if the latest version is not used (included in EGADS third party folder).'
        logging.warning('Warning: egads has detected that Quantities hasn''t been imported from EGADS directory. Quantities showed few compatibility issues with Numpy, if the latest version is not used (included in EGADS third party folder).')
except:
    sys.stderr.write('Error: quantities module not found. Quantities should be included in the thirdparty directory of EGADS. Please correct that issue before using EGADS')
    logging.exception('Error: quantities module not found. Quantities should be included in the thirdparty directory of EGADS. Please correct that issue before using EGADS')


# EGADS test protocol
print ''
egads.test()

__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 15:00"
__version__ = "1.2"

from egads_core import EgadsData
from egads_core import EgadsAlgorithm
import metadata
import logging

try:
    import quantities
    logging.info('egads - core - __init__.py - quantities has been imported')
    if 'egads' not in quantities.__path__[0]:
        logging.warning('egads - core - __init__.py - EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
except ImportError:
    logging.exception('egads - core - __init__.py - EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')

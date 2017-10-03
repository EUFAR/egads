__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 15:00"
__version__ = "1.2"

from egads_core import EgadsData
from egads_core import EgadsAlgorithm
import metadata
import logging

try:
    import quantities
    logging.info('egads.__init__: quantities has been imported')
    if 'egads' not in quantities.__path__[0]:
        logging.warning('egads.__init__: EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
except ImportError:
    logging.warning('egads.__init__: EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')

__author__ = "mfreer, ohenry"
__date__ = "$Date:: 2016-12-6 15:00#$"
__version__ = "$Revision:: 102       $"

from egads_core import EgadsData
from egads_core import EgadsAlgorithm
import metadata
import logging

try:
    import quantities  # @UnresolvedImport
    logging.info('quantities has been imported')
    if 'egads' not in quantities.__path__[0]:
        logging.warning('EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
except ImportError:
    logging.warning('EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')

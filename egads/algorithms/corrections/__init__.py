"""
EGADS corrections algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.1"

import logging
try:
    from .correction_spike_simple_cnrm import *
    logging.info('egads [corrections] algorithms have been loaded')
    logging.debug('egads [corrections] path: ' + str(__path__))
except Exception:
    logging.exception('an error occurred during the loading of a [corrections] algorithm')
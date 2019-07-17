"""
EGADS mathematics algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.1"

import logging
try:
    from .derivative_wrt_time import *
    from .limit_angle_range import *
    logging.info('egads [mathematics] algorithms have been loaded')
    logging.debug('egads [mathematics] path: ' + str(__path__))
except Exception:
    logging.exception('an error occurred during the loading of a [mathematics] algorithm')

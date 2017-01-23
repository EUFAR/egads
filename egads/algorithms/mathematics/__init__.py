"""
EGADS mathematics algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "mfreer, ohenry"
__date__ = "$Date:: 2017-01-19 11:44#$"
__version__ = "$Revision:: 154       $"

import logging
try:
    from derivative_wrt_time import *
    from limit_angle_range import *
    logging.info('egads [mathematics] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [mathematics] algorithm')

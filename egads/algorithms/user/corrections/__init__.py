"""
EGADS corrections algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2017-05-03 10:54"
__version__ = "1.0"

import logging
try:
    from my_algorithm_for_correction import *
    logging.info('egads [user/corrections] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [user/corrections] algorithm')
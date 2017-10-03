"""
EGADS corrections algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "mfreer, ohenry"
__date__ = "2017-01-19 11:41"
__version__ = "1.0"

import logging
try:
    from correction_spike_simple_cnrm import *
    logging.info('egads [corrections] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [corrections] algorithm')
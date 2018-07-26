"""
EGADS comparisons algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.0"

import logging
try:
    from .compare_param_lcss import *
    logging.info('egads [comparisons] algorithms have been loaded')
except Exception:
    logging.exception('an error occured during the loading of a [comparisons] algorithm')

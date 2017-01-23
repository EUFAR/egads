"""
EGADS comparisons algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "mfreer, ohenry"
__date__ = "$Date: 2017-01-19 11:44$"
__version__ = "$Revision: 152 $"

import logging
try:
    from compare_param_lcss import *
    logging.info('egads [comparisons] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [comparisons] algorithm')

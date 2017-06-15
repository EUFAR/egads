"""
EGADS new algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "$Date:: 2017-01-27 10:52#$"
__version__ = "$Revision:: 1      $"

import logging
try:
    from the_name_of_my_new_algorithm_file import *
    logging.info('egads [corrections] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [corrections] algorithm')

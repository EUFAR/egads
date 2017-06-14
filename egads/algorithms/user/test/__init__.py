__author__ = "Olivier Henry"
__date__ = "$Date: 2017-5-3 15:16$"
__version__ = "$Revision: 100 $"

import logging

try:
    from a_simple_computation import *
    logging.info('egads [user/comparisons] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [user/comparisons] algorithm')

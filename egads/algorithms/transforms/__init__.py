"""
EGADS transforms algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "mfreer, ohenry"
__date__ = "2017-01-08 11:42"
__version__ = "1.2"

import logging
try:
    from interpolation_linear import *
    from isotime_to_elements import *
    from isotime_to_seconds import *
    from seconds_to_isotime import *
    from time_to_decimal_year import *
    logging.info('egads [transforms] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [transforms] algorithm')
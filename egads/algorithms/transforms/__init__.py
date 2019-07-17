"""
EGADS transforms algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.1"

import logging
try:
    from .interpolation_linear import *
    from .isotime_to_elements import *
    from .isotime_to_seconds import *
    from .seconds_to_isotime import *
    from .time_to_decimal_year import *
    logging.info('egads [transforms] algorithms have been loaded')
    logging.debug('egads [transforms] path: ' + str(__path__))
except Exception:
    logging.exception('an error occurred during the loading of a [transforms] algorithm')
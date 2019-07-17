"""
EGADS radiation algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.1"

import logging
try:
    from .camera_viewing_angles import *
    from .planck_emission import *
    from .rotate_solar_vector_to_aircraft_frame import *
    from .scattering_angles import *
    from .solar_vector_blanco import *
    from .solar_vector_reda import *
    from .temp_blackbody import *
    logging.info('egads [radiation] algorithms have been loaded')
    logging.debug('egads [radiation] path: ' + str(__path__))
except Exception:
    logging.exception('an error occurred during the loading of a [radiation] algorithm')

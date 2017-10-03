"""
EGADS radiation algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "mfreer, ohenry"
__date__ = "2017-01-19 11:39"
__version__ = "1.2"

import logging
try:
    from camera_viewing_angles import *
    from planck_emission import *
    from rotate_solar_vector_to_aircraft_frame import *
    from scattering_angles import *
    from solar_vector_blanco import *
    from solar_vector_reda import *
    from temp_blackbody import *
    logging.info('egads [radiation] algorithms have been loaded')
except Exception:
    logging.error('an error occured during the loading of a [radiation] algorithm')

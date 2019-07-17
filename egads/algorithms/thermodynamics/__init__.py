"""
EGADS thermodynamics algorithms. See EGADS Algorithm Documentation for more info.
"""

__author__ = "ohenry"
__date__ = "2018-03-05 11:13"
__version__ = "1.1"

import logging
try:
    from .altitude_pressure_incremental_cnrm import *
    from .altitude_pressure_raf import *
    from .density_dry_air_cnrm import *
    from .hum_rel_capacitive_cnrm import *
    from .pressure_angle_incidence_cnrm import *
    from .pressure_dynamic_angle_incidence_vdk import *
    from .temp_potential_cnrm import *
    from .temp_static_cnrm import *
    from .temp_virtual_cnrm import *
    from .velocity_mach_raf import *
    from .velocity_tas_cnrm import *
    from .velocity_tas_longitudinal_cnrm import *
    from .velocity_tas_raf import *
    from .wind_vector_3d_raf import *
    logging.info('egads [thermodynamics] algorithms have been loaded')
    logging.debug('egads [thermodynamics] path: ' + str(__path__))
except Exception:
    logging.exception('an error occurred during the loading of a [thermodynamics] algorithm')

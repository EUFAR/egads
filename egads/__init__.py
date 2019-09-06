__author__ = "ohenry"
__date__ = "2018-03-05 10:59"
__version__ = "1.5"


import logging
import os
import platform
import quantities
import configparser
import sys
import pathlib
from ._version import __version__
from ._version import __branch__
from .utils.egads_utils import _create_user_algorithms_structure
from .utils.egads_utils import _create_option_dictionary
from .utils.egads_utils import _create_log_system
from xml.dom import minidom
from numpy import __version__ as np_version
from netCDF4 import __version__ as nc_version
from dateutil import __version__ as du_version
try:
    from requests import __version__ as rq_version
except ImportError:
    rq_version = 'requests is not available'

if getattr(sys, 'frozen', False):
    frozen = True
else:
    frozen = False


user_path = str(pathlib.Path.home().joinpath('.egads_lineage'))
_create_option_dictionary(user_path)
config_dict = configparser.ConfigParser()
config_dict.read(os.path.join(user_path, 'egads.ini'))
_create_log_system(config_dict, user_path)
logging.info('*****************************************')
logging.info('EGADS ' + __version__ + ' is starting ...')
logging.info('*****************************************')
logging.debug('egads - __init__.py - egads frozen ? ' + str(frozen))
system, release, version = platform.system_alias(platform.system(), platform.release(), platform.version())
logging.debug('egads - __init__.py - operating system: ' + system + ' ' + release + ' (' + version + ')')
logging.debug('egads - __init__.py - python version: ' + str(platform.python_version()))
logging.debug('egads - __init__.py - numpy version: ' + np_version)
logging.debug('egads - __init__.py - quantities version: ' + quantities.__version__)
logging.debug('egads - __init__.py - netcdf4 version: ' + nc_version)
logging.debug('egads - __init__.py - python_dateutil version: ' + du_version)
logging.debug('egads - __init__.py - requests version: ' + rq_version)

import egads.core
import egads.core.metadata
_create_user_algorithms_structure(user_path)
sys.path.append(user_path)
import egads.algorithms
import user_algorithms
from .input import get_file_list
from .core.egads_core import *
from .tests.test_all import test
from .core.egads_update import CheckEgadsUpdate


ug = quantities.UnitQuantity('microgram', quantities.gram/1e6, symbol='ug', aliases=['micrograms'])
psu = quantities.UnitQuantity('practical salinity unit', quantities.gram/quantities.kilogram, symbol='psu',
                              aliases=['practical salinity unit'])
logging.debug('egads - __init__.py - units have been added: ' + str(ug) + ', ' + str(psu))


def change_log_level(log_level='INFO'):
    logging.debug('egads - __init__.py - change_log_level - log_level ' + log_level)
    logging.getLogger().setLevel(getattr(logging, log_level))


def set_options(log_level=None, log_path=None, check_update=None):
    logging.debug('egads - __init__.py - set_options - log_level ' + str(log_level + ', log_path ' + str(log_path))
                  + ' ; check_update ' + str(check_update))
    if log_level is not None:
        config_dict.set("LOG", "level", log_level)
    if log_path is not None:
        config_dict.set('LOG', 'path', log_path)
    if check_update is not None:
        config_dict.set('OPTIONS', 'check_update', str(check_update))
    if log_level or log_path or check_update:
        set_options_file = open(os.path.join(user_path, 'egads.ini'), 'w')
        config_dict.write(set_options_file)
        set_options_file.close()


def print_options():
    logging.debug('egads - __init__.py - print_options')
    log_level = config_dict.get('LOG', 'level')
    log_path = config_dict.get('LOG', 'path')
    check_update_bool = config_dict.get('OPTIONS', 'check_update')
    print('EGADS options:')
    print('   - logging level: ' + log_level)
    print('   - log path: ' + log_path)
    print('   - update automatic check: ' + check_update_bool)


def check_update():
    if not frozen:
        logging.debug('egads - __init__.py - check_update - egads_version ' + __version__)
        check_update_thread = CheckEgadsUpdate(__version__)
        check_update_thread.start()
    else:
        logging.debug('egads - __init__.py - check_update - app is frozen, no update check')


def _reload_user_algorithms():
    """
    function to reload algorithms created by a user. It is intended to be used by the GUI.
    """

    logging.debug('egads - __init__.py - _reload_user_algorithms')
    import importlib
    importlib.reload(user_algorithms)
    rep_list = [item for item in dir(egads.user_algorithms) if '__' not in item]
    rep_list.remove('user_algorithms')
    for rep in rep_list:
        importlib.reload(getattr(user_algorithms, rep))


if rq_version != 'requests is not available':
    if not frozen:
        if config_dict.getboolean('OPTIONS', 'check_update'):
            check_update()
        else:
            logging.debug('egads - __init__.py - check_update on False, no update check')
    else:
        logging.debug('egads - __init__.py - app is frozen, no update check')
else:
    logging.debug('egads - __init__.py - no requests module, no update check')


logging.info('EGADS ' + __version__ + ' is ready ...')

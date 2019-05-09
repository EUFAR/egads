__author__ = "ohenry"
__date__ = "2018-03-05 10:59"
__version__ = "1.4"

from ._version import __version__
from ._version import __branch__
import logging
import os
import platform
import configparser
import quantities
from numpy import __version__ as np_version
from scipy import __version__ as sy_version
from netCDF4 import __version__ as nc_version
from dateutil import __version__ as du_version
try:
    from requests import __version__ as rq_version
except ImportError:
    rq_version = 'requests is not available'


def _create_user_algorithms_structure(main_path):
    logging.debug('egads - __init__.py - create_user_algorithms_structure - main_path ' + str(main_path))
    user_path = os.path.join(main_path, 'algorithms/user/')
    if not os.path.isdir(user_path):
        logging.debug('egads - __init__.py - create_user_algorithms_structure - no user folder detected, '
                      'creating user structure')
        os.makedirs(user_path)
        init_string = ('__author__ = "Olivier Henry"\n'
                       + '__date__ = "2019/05/06 11:45"\n'
                       + '__version__ = "1.0"\n\n'
                       + 'import egads.algorithms.user.comparisons\n'
                       + 'import egads.algorithms.user.corrections\n'
                       + 'import egads.algorithms.user.mathematics\n'
                       + 'import egads.algorithms.user.microphysics\n'
                       + 'import egads.algorithms.user.thermodynamics\n'
                       + 'import egads.algorithms.user.transforms\n'
                       + 'import egads.algorithms.user.radiation\n')
        init_file = open(user_path + '__init__.py', 'w')
        init_file.write(init_string)
        init_file.close()

        user_folder = ['comparisons', 'corrections', 'mathematics', 'microphysics', 'thermodynamics', 'transforms',
                       'radiation']
        for folder in user_folder:
            logging.debug('egads - __init__.py - create_user_algorithms_structure - creating [user/' + folder + '] '
                          + 'folder')
            os.makedirs(os.path.join(user_path, folder))
            init_string = ('__author__ = "Olivier Henry"\n'
                           + '__date__ = "2019/05/06 11:45"\n'
                           + '__version__ = "1.0"\n\n'
                           + 'import logging\n\n'
                           + 'try:\n'
                           + "    logging.info('egads [user/" + folder + "] algorithms have been loaded')\n"
                           + 'except Exception:\n'
                           + "    logging.error('an error occured during the loading of a [user/" + folder
                           + "] algorithm')\n")
            init_file = open(os.path.join(user_path, folder) + '/__init__.py', 'w')
            init_file.write(init_string)
            init_file.close()
    else:
        logging.debug('egads - __init__.py - create_user_algorithms_structure - user folder detected, no need to '
                      'create user structure')


path = os.path.abspath(os.path.dirname(__file__))
config_dict = configparser.ConfigParser()
if not os.path.exists(os.path.join(path, 'egads.ini')):
    ini_file = open(os.path.join(path, 'egads.ini'), 'w')
    config_dict.add_section('LOG')
    config_dict.add_section('OPTIONS')
    config_dict.set('LOG', 'level', 'DEBUG')
    config_dict.set('LOG', 'path', path)
    config_dict.set('OPTIONS', 'check_update', 'False')
    config_dict.write(ini_file)
    ini_file.close()
config_dict.read(os.path.join(path, 'egads.ini'))
log_filename = os.path.join(config_dict.get('LOG', 'path'), 'egads.log')
logging.getLogger('').handlers = []
logging.basicConfig(filename=log_filename,
                    level=getattr(logging, config_dict.get('LOG', 'level')),
                    filemode='w',
                    format='%(asctime)s : %(levelname)s : %(message)s')
formatter = logging.Formatter('%(levelname)s : %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
logging.info('*****************************************')
logging.info('EGADS ' + __version__ + ' is starting ...')
logging.info('*****************************************')
system, release, version = platform.system_alias(platform.system(), platform.release(), platform.version())
logging.debug('egads - __init__.py - operating system: ' + system + ' ' + release + ' (' + version + ')')
logging.debug('egads - __init__.py - python version: ' + str(platform.python_version()))
logging.debug('egads - __init__.py - numpy version: ' + np_version)
logging.debug('egads - __init__.py - quantities version: ' + quantities.__version__)
logging.debug('egads - __init__.py - scipy version: ' + sy_version)
logging.debug('egads - __init__.py - netcdf4 version: ' + nc_version)
logging.debug('egads - __init__.py - python_dateutil version: ' + du_version)
logging.debug('egads - __init__.py - requests version: ' + rq_version)

import egads.core
import egads.core.metadata
_create_user_algorithms_structure(path)
import egads.algorithms
from .input import get_file_list
from .core.egads_core import *
from .tests.test_all import test
from .core.egads_update import CheckEgadsUpdate

ug = quantities.UnitQuantity('microgram', quantities.gram/1e6, symbol='ug', aliases=['micrograms'])
hpa = quantities.UnitQuantity('hectopascal', quantities.Pa * 100, symbol='hPa', aliases=['hectopascals'])
psu = quantities.UnitQuantity('practical salinity unit', quantities.gram/quantities.kilogram, symbol='psu',
                              aliases=['practical salinity unit'])
logging.debug('egads - __init__.py - units have been added: ' + str(ug) + ', ' + str(hpa) + ', ' + str(psu))


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
        set_options_file = open(os.path.join(path, 'egads.ini'), 'w')
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
    logging.debug('egads - __init__.py - check_update - egads_version ' + __version__)
    check_update_thread = CheckEgadsUpdate(__version__)
    check_update_thread.start()


if rq_version != 'requests is not available':
    if config_dict.getboolean('OPTIONS', 'check_update'):
        check_update()
    else:
        logging.debug('egads - __init__.py - check_update on False, no update check')
else:
    logging.debug('egads - __init__.py - no requests module, no update check')


logging.info('EGADS ' + __version__ + ' is ready ...')

__author__ = "mfreer, ohenry"
__date__ = "2016-12-16 10:33"
__version__ = "1.8"

from _version import __version__
import logging
from logging.handlers import RotatingFileHandler
from threading import Thread
import os
import sys
import site
import ConfigParser

path = os.path.abspath(os.path.dirname(__file__))
config_dict = ConfigParser.ConfigParser()
if not os.path.exists(os.path.join(path, 'egads.ini')):
        ini_file = open(os.path.join(path, 'egads.ini'), 'w')
        config_dict.add_section('LOG')
        config_dict.add_section('OPTIONS')
        config_dict.set('LOG','level','DEBUG')
        config_dict.set('LOG','path', '')
        config_dict.set('OPTIONS','check_update','False')
        config_dict.write(ini_file)
        ini_file.close()   
config_dict.read(os.path.join(path, 'egads.ini'))
log_filename = os.path.join(config_dict.get('LOG', 'path'),'egads.log')
logging.getLogger('').handlers = []
logging.basicConfig(filename = log_filename,
                    level = getattr(logging, config_dict.get('LOG', 'level')),
                    filemode = 'w',
                    format = '%(asctime)s : %(levelname)s : %(message)s')
formatter = logging.Formatter('%(levelname)s : %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.info('*****************************************')
logging.info('EGADS ' + __version__ + ' is starting ...')
logging.info('*****************************************')

logging.debug('egads - __init__.py - operating system: ' + str(sys.platform))
python_version = str(sys.version_info[0]) + '.' + str(sys.version_info[1]) + '.' + str(sys.version_info[2])
logging.debug('egads - __init__.py - python version: ' + python_version)

ver = 'python%d.%d' % sys.version_info[:2]
thirdparty = os.path.join(path, 'thirdparty')
site.addsitedir(thirdparty)

import core
import core.metadata
import algorithms
from input import get_file_list
from core.egads_core import *
from tests.test_all import test
from core.egads_update import CheckEgadsUpdate


try:
    import quantities
    logging.info('egads - __init__.py - quantities has been imported')
    if 'egads' not in quantities.__path__[0]:
        logging.warning('egads - __init__.py - EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
        print ('EGADS has imported an already installed version of Quantities. If issues occure,'
               + ' please check the version number of Quantities.')
except ImportError:
    logging.exception('egads - __init__.py - EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')
    raise ImportError('EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')

quantities.UnitQuantity('microgram', quantities.gram/1e6, symbol='ug', aliases=['micrograms'])
quantities.UnitQuantity('hectopascal', quantities.Pa * 100, symbol='hPa', aliases=['hectopascals'])

def change_log_level(log_level='INFO'):
    logging.debug('egads - __init__.py - change_log_level - log_level ' + log_level)
    logging.getLogger().setLevel(getattr(logging, log_level))
    
def set_log_options(log_level=None, log_path=None):
    logging.debug('egads - __init__.py - set_log_options - log_level ' + str(log_level + ', log_path ' + str(log_path)))
    if log_level:
        config_dict.set("LOG", "level", log_level)
    if log_path:
        config_dict.set('LOG', 'path', log_path)
    if log_level or log_path:
        ini_file = open(os.path.join(path, 'egads.ini'), 'w')
        config_dict.write(ini_file)
        ini_file.close()
        
def print_options():
    logging.debug('egads - __init__.py - print_log_options')
    log_level = config_dict.get('LOG', 'level')
    log_path = config_dict.get('LOG', 'path')
    check_update = config_dict.get('OPTIONS', 'check_update')
    if not log_path:
        log_path = 'default directory'
    print 'The logging level is set on ' + log_level + ' and the log file is available in ' + log_path + '.'
    print 'The option to check automatically for an update is set on ' + check_update + '.'

def set_update_check_option(check_update=None):
    logging.debug('egads - __init__.py - set_update_check_option - check_update ' + str(check_update))
    if check_update:
        config_dict.set('OPTIONS', 'check_update', check_update)
        ini_file = open(os.path.join(path, 'egads.ini'), 'w')
        config_dict.write(ini_file)
        ini_file.close()

def check_update():
    check_update = CheckEgadsUpdate()
    check_update.start()

if config_dict.getboolean('OPTIONS', 'check_update'):
    import imp
    if imp.lock_held():
        imp.release_lock()
        check_update()
        imp.acquire_lock()

logging.info('EGADS ' + __version__ + ' is ready ...')


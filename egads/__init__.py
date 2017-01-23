__author__ = "mfreer, ohenry"
__date__ = "$Date:: 2016-12-16 10:33#$"
__revision__ = "$Revision:: 135       $"
__version__ = "unknown"

from _version import __version__
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import site
import ConfigParser

path = os.path.abspath(os.path.dirname(__file__))

config_dict = ConfigParser.ConfigParser()
config_dict.read(os.path.join(path, 'egads.ini'))

if not config_dict.get('LOG', 'path'):
    log_filename = os.path.join(path,'egads_log.out')
else:
    log_filename = os.path.join(config_dict.get('LOG', 'path'),'egads_log.out')

logging.getLogger('').handlers = []
logging.basicConfig(filename = log_filename,
                    level = getattr(logging, config_dict.get('LOG', 'level')),
                    filemode = 'w',
                    format = '%(asctime)s : %(levelname)s : %(message)s')
formatter = logging.Formatter('%(levelname)s : %(message)s')
'''console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)'''

logging.info('*****************************************')
logging.info('EGADS ' + __version__ + ' is starting ...')
logging.info('*****************************************')

ver = 'python%d.%d' % sys.version_info[:2]
thirdparty = os.path.join(path, 'thirdparty')
site.addsitedir(thirdparty)

import core
import core.metadata
import algorithms
from input import get_file_list
from core.egads_core import *
from tests.test_all import test

try:
    import quantities  # @UnresolvedImport
    logging.info('quantities has been imported')
    if 'egads' not in quantities.__path__[0]:
        logging.warning('EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
except ImportError:
    logging.warning('EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')

quantities.UnitQuantity('microgram', quantities.gram/1e6, symbol='ug', aliases=['micrograms'])
quantities.UnitQuantity('hectopascal', quantities.Pa * 100, symbol='hPa', aliases=['hectopascals'])

def change_log_level(log_level='INFO'):
    logging.getLogger().setLevel(getattr(logging, log_level))
    
def set_log_options(log_options=None):
    if log_options:
        for key, value in log_options.iteritems():
            config_dict.set("LOG", key, value)
        with open(os.path.join(path, 'egads.ini'), 'w') as configfile:    # save
            config_dict.write(configfile)

logging.info('EGADS ' + __version__ + ' is ready ...')


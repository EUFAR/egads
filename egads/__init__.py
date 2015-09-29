__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__revision__ = "$Revision:: 125       $"
__version__ = "unknown"
try:
    from _version import __version__
except ImportError:
    # No _version.py in tree, so we dont know what the version is
    pass

# TODO Add docstrings to file

# from tests import test_all

import os
import sys
import site
path = os.path.abspath(os.path.dirname(__file__))
ver = 'python%d.%d' % sys.version_info[:2]
thirdparty = os.path.join(path, 'third-party')
site.addsitedir(thirdparty)

import quantities as units

units.hPa = units.UnitQuantity('hectopascal', units.Pa * 100, symbol='hPa')

import core
import core.metadata
import algorithms
import input
from input import get_file_list

from core.egads_core import *

from tests.test_all import test

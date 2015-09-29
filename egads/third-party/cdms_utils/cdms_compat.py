"""
cdms_compat.py
==============

Does imports of cdms, numpy and related modules for either python2.4 or python2.5 versions.

"""

try:
	import cdms2 as cdms
except ImportError:
	import cdms
	import MV
	import Numeric as N
	import MA
else:
	import MV2 as MV
	import numpy.oldnumeric as N
	import numpy.oldnumeric.ma as MA


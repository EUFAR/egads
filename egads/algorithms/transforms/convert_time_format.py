"""
Utility to convert time format into format recognized by dateutil.
"""
__author__ = "ohenry"
__date__ = "2018-03-07 18:34"
__version__ = "1.1"

from collections import OrderedDict


def convert_time_format(fmt):
    FMT_DICT = OrderedDict([('yyyy','%Y'),
                            ('yy','%y'),
                            ('mm','%m'),
                            ('dd','%d'),
                            ('HH','%H'),
                            ('hh','%H'),
                            ('MM','%M'),
                            ('ss','%S'),
                            ('SS','%S')])

    fmt = str(fmt)
    for key, val in FMT_DICT.items():
        fmt = fmt.replace(key, val)
    return fmt

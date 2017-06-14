"""
Utility to convert time format into format recognized by dateutil.
"""
__author__ = "mfreer"
__date__ = "2012-07-06 17:42"
__version__ = "146"

def convert_time_format(fmt):
    FMT_DICT = {'yyyy':'%Y',
                'yy':'%y',
                'mm':'%m',
                'dd':'%d',
                'HH':'%H',
                'hh':'%H',
                'MM':'%M',
                'ss':'%S',
                'SS':'%S'}

    fmt = str(fmt)
    for key, val in FMT_DICT.iteritems():
        fmt = fmt.replace(key, val)
    return fmt

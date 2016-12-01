__author__ = "mfreer"
__date__ = "$Date:: 2012-07-12 17:27#$"
__version__ = "$Revision:: 150       $"
__all__ = ['SecondsToIsotime']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import datetime
import dateutil.parser

from convert_time_format import convert_time_format

class SecondsToIsotime(egads_core.EgadsAlgorithm):
    """

    FILE        seconds_to_isotime.py

    VERSION     $Revision: 150 $

    CATEGORY    Transforms

    PURPOSE     Converts an elapsed seconds parameter into ISO 8601 formatted time string 

    DESCRIPTION Given a vector of seconds elapsed and a reference time, this algorithm
                calculates  a series of ISO 8601 strings using the Python datetime module.
                ISO 8601 string formats can be controlled by the optional format string, 
                default is yyyymmddTHHMMss.

    INPUT       t_secs    vector    seconds     elapsed seconds
                t_ref     string                ISO 8601 reference time
                format    string, optional      ISO 8601 format string, default is yyyymmddTHHMMss 

    OUTPUT      t_ISO     vector                ISO 8601 date-time strings

    SOURCE      

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'ISO 8601 date-time',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['t_secs', 't_ref', 'format'],
                                                          'InputUnits':['s', '', ''],
                                                          'InputTypes':['vector','string','string_optional'],
                                                          'InputDescription':['Elapsed seconds','ISO 8601 reference time','ISO 8601 format string, default is yyyymmddTHHMMss '],
                                                          'Outputs':['t_ISO'],
                                                          'OutputDescription':['ISO 8601 date-time strings'],
                                                          'Purpose':'Converts an elapsed seconds parameter into ISO 8601 formatted time string',
                                                          'Description':'Given a vector of seconds elapsed and a reference time, this algorithm calculates  a series of ISO 8601 strings using the Python datetime module. ISO 8601 string formats can be controlled by the optional format string, default is yyyymmddTHHMMss',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

        self.format_default = 'yyyymmddTHHMMss'

    def run(self, t_secs, t_ref, fmt=None):

        return egads_core.EgadsAlgorithm.run(self, t_secs, t_ref, fmt)


    def _algorithm(self, t_secs, t_ref, fmt):

        if fmt:
            fmt = str(fmt)
        else:
            fmt = self.format_default

        fmt = convert_time_format(fmt)

        t_ISO = []
        datetime_ref = dateutil.parser.parse(str(t_ref))

        for time in t_secs:
            time_delta = datetime.timedelta(0, float(time))
            merge_time = datetime_ref + time_delta
            t_ISO.append(merge_time.strftime(fmt))


        return t_ISO



__author__ = "mfreer"
__date__ = "2012-07-06 17:42"
__version__ = "1.3"
__all__ = ['IsotimeToSeconds']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import dateutil.parser
import datetime
from convert_time_format import convert_time_format

class IsotimeToSeconds(egads_core.EgadsAlgorithm):
    
    """
    FILE        isotime_to_seconds.py

    VERSION     1.3

    CATEGORY    Transforms

    PURPOSE     Calculates seconds elapsed from a series of ISO 8601 date/time strings

    DESCRIPTION Calculates seconds elapsed from a series of ISO 8601 date/time strings 
                (yyyymmddThhmmss, yyyy-mm-ddThh:mm:ss,yyyymmdd or similar) using the Python 
                dateutil and datetime modules.

    INPUT       t_ISO         vector            yyyymmddThhmmss     ISO 8601 date-time string
                                                yyyymmdd            ISO 8601 date string
                t_ISO_ref     string, optional                      Reference time (ISO 8601 string).
                                                                    default is 19700101T000000.
                format        string, optional                      Time string format, if none 
                                                                    provided algorithm will attempt 
                                                                    to automatically deconstruct 
                                                                    timestring.

    OUTPUT      delta_t       vector            seconds             seconds since reference

    SOURCE      

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'s',
                                                               'long_name':'elapsed seconds',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['t_ISO', 't_ISO_ref', 'format'],
                                                          'InputUnits':['', '', ''],
                                                          'InputTypes':['vector','string_optional','string_optional'],
                                                          'InputDescription':['ISO 8601 strings','Reference time (ISO 8601 string) - default is 19700101T000000','Time string format - if none provided algorithm will attempt to automatically deconstruct timestring'],
                                                          'Outputs':['delta_t'],
                                                          'OutputUnits':['s'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Seconds since reference'],
                                                          'Purpose':'Calculates seconds elapsed from a series of ISO 8601 date/time strings',
                                                          'Description':'Calculates seconds elapsed from a series of ISO 8601 date/time strings using the Python dateutil and datetime modules',
                                                          'Category':'Transforms',
                                                          'Source':'',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

        self.default_ref_time = datetime.datetime(1970, 1, 1, 0, 0, 0)

    def run(self, t_ISO, t_ISO_ref=None, fmt=None):
        return egads_core.EgadsAlgorithm.run(self, t_ISO, t_ISO_ref, fmt)

    def _algorithm(self, t_ISO, t_ISO_ref, fmt):
        time_delta_secs = []
        SECS_PER_DAY = 60 * 60 * 24
        if fmt:
            fmt = convert_time_format(fmt)
            if t_ISO_ref:
                time0 = datetime.datetime.strptime(str(t_ISO_ref), fmt)
            else:
                time0 = self.default_ref_time
            for time in t_ISO:
                time_decomp = datetime.datetime.strptime(time, fmt)
                time_delta = time_decomp - time0
                time_delta_secs.append(time_delta.days * SECS_PER_DAY + time_delta.seconds +
                                       time_delta.microseconds * 1.0e-6)
        else:
            if t_ISO_ref:
                time0 = dateutil.parser.parse(str(t_ISO_ref))
            else:
                time0 = self.default_ref_time
            for time in t_ISO:
                time_decomp = dateutil.parser.parse(time)
                time_delta = time_decomp - time0
                time_delta_secs.append(time_delta.days * SECS_PER_DAY + time_delta.seconds +
                                       time_delta.microseconds * 1.0e-6)
        return time_delta_secs


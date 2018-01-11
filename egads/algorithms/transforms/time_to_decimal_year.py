__author__ = "ohenry"
__date__ = "2017-09-28 16:06"
__version__ = "1.1"
__all__ = ['TimeToDecimalYear']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import egads

class TimeToDecimalYear(egads_core.EgadsAlgorithm):
    
    """
    FILE        time_to_decimal_year.py

    VERSION     1.1

    CATEGORY    Transforms

    PURPOSE     Converts a time or a time vector to decimal year. 

    DESCRIPTION Given a vector of time (ms/s/mm/h/d/m) and an optional reference year, this algorithm
                converts the data to a format in decimal year. Ex: 1995.0125

    INPUT       t         vector            s/mm/h/...        time.
                t_ref     string, optional  yyyymmddTHHMMss   time reference. 
                                                              by default: 19500101T000000

    OUTPUT      t_y       vector            year              time in decimal year.

    SOURCE

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'year',
                                                               'long_name':'time in decimal year',
                                                               'standard_name':'time',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['t', 't_ref'],
                                                          'InputUnits':['year', None],
                                                          'InputTypes':['vector','coeff_optional'],
                                                          'InputDescription':['Time.','Time reference in year.'],
                                                          'Outputs':['t_y'],
                                                          'OutputUnits':['year'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Time in decimal year.'],
                                                          'Purpose':'Converts a time or a time vector to decimal year.',
                                                          'Description':'Given a vector of time elapsed and an optional reference year, this algorithm convert the data to a format in decimal year. Ex: 1995.0125',
                                                          'Category':'Transforms',
                                                          'Source':'',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, t, t_ref=None):
        return egads_core.EgadsAlgorithm.run(self, t, t_ref)

    def _algorithm(self, t, t_ref=None):
        t_ref_s = 0
        if t_ref:
            t_ref_s = egads.algorithms.transforms.IsotimeToSeconds().run([t_ref], '19500101T000000')  # @UndefinedVariable
        t_s = t + egads.EgadsData(value=t_ref_s, units='s').rescale('year').value
        t_y = t_s + 1950
        return t_y

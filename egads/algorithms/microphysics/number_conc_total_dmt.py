__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__version__ = "$Revision:: 125       $"
__all__ = ['NumberConcTotalDmt']

import numpy

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class NumberConcTotalDmt(egads_core.EgadsAlgorithm):

    """

    FILE        number_conc_total_dmt.py

    VERSION     $Revision: 125 $

    CATEGORY    Microphysics

    PURPOSE     Calculation of total number concentration given distribution of 
                particle counts from a particle sampling probe

    DESCRIPTION Calculation of total number concentration given distribution of 
                particle counts from a particle sampling probe

    INPUT       c_i    array[time, bins]    cm-3    number concentration of hydrometeors
                                                    in size category i
                                                        
    OUTPUT      N      vector[time]         cm-3    Total number concentration

    SOURCE      sources

    REFERENCES  "Data Analysis User's Guide", Droplet Measurement Technologies, 2009,
                44 pp.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'cm^-3',
                                                               'long_name':'total number concentration',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['c_i'],
                                                          'InputUnits':['cm^-3'],
                                                          'InputTypes':['array'],
                                                          'InputDescription':['Number concentration of hydrometeors in size category i'],
                                                          'Outputs':['N'],
                                                          'OutputDescription':['Total number concentration'],
                                                          'Purpose':'Calculation of total number concentration given distribution of particle counts from a particle sampling probe',
                                                          'Description':'alculation of total number concentration given distribution of particle counts from a particle sampling probe',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, c_i):

        return egads_core.EgadsAlgorithm.run(self, c_i)

    def _algorithm(self, c_i):

        N = numpy.sum(c_i, axis=1)

        return N



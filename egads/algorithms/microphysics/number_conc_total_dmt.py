__author__ = "mfreer"
__date__ = "2012-02-07 17:23"
__version__ = "1.2"
__all__ = ['NumberConcTotalDmt']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class NumberConcTotalDmt(egads_core.EgadsAlgorithm):

    """
    FILE        number_conc_total_dmt.py

    VERSION     1.2

    CATEGORY    Microphysics

    PURPOSE     Calculation of total number concentration given distribution of 
                particle counts from a particle sampling probe

    DESCRIPTION Calculation of total number concentration given distribution of 
                particle counts from a particle sampling probe

    INPUT       c_i    array[time, bins]    cm-3    number concentration of hydrometeors
                                                    in size category i
                                                        
    OUTPUT      N      vector[time]         cm-3    Total number concentration

    SOURCE      sources

    REFERENCES  "Data Analysis User's Guide, Chapter 1, Section 1.3.2", Droplet Measurement 
                Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/Manuals
                Guides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'cm^-3',
                                                               'long_name':'total number concentration',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['c_i'],
                                                          'InputUnits':['cm^-3'],
                                                          'InputTypes':['array[time, bins]'],
                                                          'InputDescription':['Number concentration of hydrometeors in size category i'],
                                                          'Outputs':['N'],
                                                          'OutputUnits':['cm^-3'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Total number concentration'],
                                                          'Purpose':'Calculation of total number concentration given distribution of particle counts from a particle sampling probe',
                                                          'Description':'alculation of total number concentration given distribution of particle counts from a particle sampling probe',
                                                          'Category':'Microphysics',
                                                          'Source':'',
                                                          'References':"Data Analysis User's Guide, Chapter 1, Section 1.3.2, Droplet Measurement Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/ManualsGuides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf",
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


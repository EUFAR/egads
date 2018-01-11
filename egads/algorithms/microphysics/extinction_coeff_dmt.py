__author__ = "mfreer, ohenry"
__date__ = "2016-01-10 10:01"
__version__ = "1.2"
__all__ = ['ExtinctionCoeffDmt']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class ExtinctionCoeffDmt(egads_core.EgadsAlgorithm):

    """
    FILE        extinction_coeff_dmt.py

    VERSION     1.2

    CATEGORY    Microphysics

    PURPOSE     Calculates extinction coefficient based on a particle size distribution

    DESCRIPTION Calculates extinction coefficient based on a particle size distribution

    INPUT       n_i    array[time,bins]        cm-3    number concentration of 
                                                       hydrometeors in size category i
                d_i    vector[bins]            um      average diameter of size category i
                Q_e    vector[bins],optional   _       extinction efficiency; default is 2
    
    OUTPUT      B_e    vector[time]            km-1    extinction coefficient

    SOURCE      

    REFERENCES  "Data Analysis User's Guide, Chapter 1, Section 1.3.2.2", Droplet Measurement 
                Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/Manuals
                Guides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'km^-1',
                                                               'long_name':'extinction coefficient',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i', 'Q_e'],
                                                          'InputUnits':['cm^-3', 'um', ''],
                                                          'InputTypes':['array[time,bins]','vector[bins]','vector[bins]_optional'],
                                                          'InputDescription':['Number concentration of hydrometeors in size category i',
                                                                              'Average diameter of size category i',
                                                                              'Extinction efficiency; default is 2'],
                                                          'Outputs':['B_e'],
                                                          'OutputUnits':['km^-1'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Extinction coefficient'],
                                                          'Purpose':'Calculates extinction coefficient based on a particle size distribution',
                                                          'Description':'Calculates extinction coefficient based on a particle size distribution',
                                                          'Category':'Microphysics',
                                                          'Source':'',
                                                          'References':"Data Analysis User's Guide, Chapter 1, Section 1.3.2.2, Droplet Measurement Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/ManualsGuides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf",
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_i, d_i, Q_e=2):
        return egads_core.EgadsAlgorithm.run(self, n_i, d_i, Q_e)

    def _algorithm(self, n_i, d_i, Q_e):
        B_e = numpy.pi / 4.0 * numpy.sum(Q_e * n_i * d_i ** 2, axis=1)
        B_e = B_e * 0.001
        return B_e


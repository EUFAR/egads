__author__ = "mfreer"
__date__ = "$Date:: 2012-02-10 17:51#$"
__version__ = "$Revision:: 126       $"
__all__ = ['ExtinctionCoeffDmt']

import numpy

import egads
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class ExtinctionCoeffDmt(egads_core.EgadsAlgorithm):

    """
    FILE        extinction_coeff_dmt.py

    VERSION     $Revision: 126 $

    CATEGORY    Microphysics

    PURPOSE     Calculates extinction coefficient based on a particle size distribution

    DESCRIPTION 

    INPUT       n_i    array[time,bins]        cm-3    number concentration of 
                                                       hydrometeors in size category i
                d_i    vector[bins]            um      average diameter of size category i
                Q_e    vector[bins],optional   _       extinction efficiency; default is 2
    
    OUTPUT      B_e    vector[time]            km-1    extinction coefficient

    SOURCE      

    REFERENCES  "Data Analysis User's Guide", Droplet Measurement Technologies, 2009,
                44 pp.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'km^-1',
                                                               'long_name':'extinction coefficient',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i', 'Q_e'],
                                                          'InputUnits':['cm^-3', 'um', ''],
                                                          'Outputs':['B_e'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, n_i, d_i, Q_e=2):

        return egads_core.EgadsAlgorithm.run(self, n_i, d_i, Q_e)


    def _algorithm(self, n_i, d_i, Q_e):

        B_e = egads.units.pi / 4.0 * numpy.sum(Q_e * n_i * d_i ** 2, axis=1) # um^2/cm^3

        B_e = B_e * 0.001 # 1/km

        return B_e



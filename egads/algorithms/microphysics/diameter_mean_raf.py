__author__ = "mfreer"
__date__ = "2012-02-07 17:23"
__version__ = "1.1"
__all__ = ['DiameterMeanRaf']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class DiameterMeanRaf(egads_core.EgadsAlgorithm):
    
    """
    FILE        diameter_mean_raf.py

    VERSION     1.1

    CATEGORY    Microphysics

    PURPOSE     Calculates mean diameter of particles.

    DESCRIPTION Calculates mean diameter of particles given an array of particle
                counts and a vector of their corresponding sizes, using the methods
                given in the NCAR RAF Bulletin #24

    INPUT       n_i     array[time, bins]   _   Particle counts in each bin over time
                d_i     vector[bins]        um  Diameter of each channel

    OUTPUT      D_bar   vector[time]        um  Mean diameter

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'um',
                                                               'long_name':'mean diameter',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i','d_i'],
                                                          'InputUnits':['','um'],
                                                          'InputTypes':['array[time, bins]','vector[bins]'],
                                                          'InputDescription':['Particle counts in each bin over time','Diameter of each channel'],
                                                          'Outputs':['D_bar'],
                                                          'OutputUnits':['um'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Mean diameter'],
                                                          'Purpose':'Calculates mean diameter of particles',
                                                          'Description':'Calculates mean diameter of particles given an array of particle counts and a vector of their corresponding sizes, using the methods given in the NCAR RAF Bulletin #24',
                                                          'Category':'Microphysics',
                                                          'Source':'NCAR-RAF',
                                                          'References':'NCAR-RAF Bulletin No. 24',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_i, d_i):
        return egads_core.EgadsAlgorithm.run(self, n_i, d_i)

    def _algorithm(self, n_i, d_i):
        D_bar = numpy.sum(n_i * d_i, axis=1) / numpy.sum(n_i, axis=1)
        return D_bar

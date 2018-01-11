__author__ = "mfreer"
__date__ = "2012-02-07 17:23"
__version__ = "1.2"
__all__ = ['NumberConcTotalRaf']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class NumberConcTotalRaf(egads_core.EgadsAlgorithm):
    
    """
    FILE        number_conc_total_raf.py

    VERSION     1.2

    CATEGORY    Microphysics

    PURPOSE     Calculates total number concentration for a particle probe

    DESCRIPTION Calculates total number concentration for a generic particle
                probe given counts for each bin and probe sample volume.

    INPUT       n_i     array[time, bins]   _       Particle counts in each bin over time
                SV      array[time, bins]   m3      Sample volume for each bin over time

    OUTPUT      N_t     vector[time]        m-3     Total number concentration

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m^-3',
                                                               'long_name':'total number concentration',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'SV'],
                                                          'InputUnits':['', 'm^3'],
                                                          'InputTypes':['array[time, bins]','array[time, bins]'],
                                                          'InputDescription':['Particle counts in each bin over time','Sample volume for each bin over time'],
                                                          'Outputs':['N_t'],
                                                          'OutputUnits':['m^-3'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Total number concentration'],
                                                          'Purpose':'Calculates total number concentration for a particle probe',
                                                          'Description':'Calculates total number concentration for a generic particle probe given counts for each bin and probe sample volume',
                                                          'Category':'',
                                                          'Source':'',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_i, SV):
        return egads_core.EgadsAlgorithm.run(self, n_i, SV)

    def _algorithm(self, n_i, SV):
        N_t = numpy.sum(n_i / SV, axis=1)
        return N_t


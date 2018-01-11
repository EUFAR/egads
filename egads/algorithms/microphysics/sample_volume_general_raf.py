__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.3"
__all__ = ['SampleVolumeGeneralRaf']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class SampleVolumeGeneralRaf(egads_core.EgadsAlgorithm):
    
    """
    FILE        sample_volume_general_raf.py

    VERSION     1.3

    CATEGORY    Microphysics

    PURPOSE     Calculate sample volume for microphysics probes.

    DESCRIPTION Calculate sample volume for microphysics probes given true air
                speed, probe sample area and sample rate.

    INPUT       V_t     vector[time]    m/s     True air speed
                SA      vector[bins]    m2      Probe sample area
                t_s     coeff           s       Probe sample rate

    OUTPUT      SV      array[time, bins]   m3  Sample volume

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m^3',
                                                               'long_name':'sample volume',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['V_t', 'SA', 't_s'],
                                                          'InputUnits':['m/s', 'm^2', 's'],
                                                          'InputTypes':['vector', 'vector', 'coeff'],
                                                          'InputDescription':['True air speed', 'Probe sample area', 'Probe sample rate'],
                                                          'Outputs':['SV'],
                                                          'OutputUnits':['m^3'],
                                                          'OutputTypes':['array[time, bins]'],
                                                          'OutputDescription':['Sample volume'],
                                                          'Purpose':'Calculate sample volume for microphysics probes',
                                                          'Description':'Calculate sample volume for microphysics probes given true air speed, probe sample area and sample rate',
                                                          'Category':'Microphysics',
                                                          'Source':'NCAR-RAF',
                                                          'References':'NCAR-RAF Bulletin No. 24',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, V_t, SA, t_s):
        return egads_core.EgadsAlgorithm.run(self, V_t, SA, t_s)

    def _algorithm(self, V_t, SA, t_s):
        SA = numpy.array(SA)
        if SA.ndim == 0:
            SV = V_t * SA * t_s
        else:
            SV = numpy.zeros([len(V_t), len(SA)])
            for i, SA_bin in enumerate(SA):
                SV[:, i] = V_t * SA_bin * t_s
        return SV
    
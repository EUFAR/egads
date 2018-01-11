__author__ = "mfreer, ohenry"
__date__ = "2016-01-12 9:35"
__version__ = "1.2"
__all__ = ["HumRelCapacitiveCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class HumRelCapacitiveCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        hum_rel_capacitive_cnrm.py

    VERSION     1.2

    CATEGORY    Thermodynamics

    PURPOSE     Calculate relative humidity from capacitive probe

    DESCRIPTION Calculates relative humidity of the air based on the frequency
                of the capacitive probe.

    INPUT       Ucapf       vector  Hz      output frequency of capacitive probe
                T_s         vector  K       static temperature
                P_s         vector  hPa     static pressure
                dP          vector  hPa     dynamic pressure
                C_t         coeff.  %/C     temperature correction coefficient
                Fmin        coeff.  Hz      minimal acceptable frequency
                C_0         coeff.  ()      calibration law 0th degree coefficient
                C_1         coeff.  ()      calibration law 1st degree coefficient
                C_2         coeff.  ()      calibration law 2nd degree coefficient

    OUTPUT      H_u         vector  %       relative humidity

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'relative humidity',
                                                               'standard_name':'relative_humidity',
                                                               'Category':['Thermodynamics', 'Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['Ucapf', 'T_s', 'P_s', 'dP', 'C_t', 'Fmin', 'C_0', 'C_1', 'C_2'],
                                                          'InputUnits':['Hz', 'K', 'hPa', 'hPa', '%/degC', 'Hz', '', '', ''],
                                                          'InputTypes':['vector','vector','vector','vector','coeff','coeff','coeff','coeff','coeff'],
                                                          'InputDescription':['Output frequency of capacitive probe','Static temperature','Static pressure','Dynamic pressure','Temperature correction coefficient','Minimal acceptable frequency','Calibration law 0th degree coefficient','Calibration law 1st degree coefficient','Calibration law 2nd degree coefficient'],
                                                          'Outputs':['H_u'],
                                                          'OutputUnits':[''],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Relative humidity'],
                                                          'Purpose':'Calculate relative humidity from capacitive probe',
                                                          'Description':'Calculates relative humidity of the air based on the frequency of the capacitive probe',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, Ucapf, T_s, P_s, dP, C_t, Fmin, C_0, C_1, C_2):
        return egads_core.EgadsAlgorithm.run(self, Ucapf, T_s, P_s, dP, C_t, Fmin, C_0, C_1, C_2)

    def _algorithm(self, Ucapf, T_s, P_s, dP, C_t, Fmin, C_0, C_1, C_2):
        tempUcapf = numpy.array(Ucapf)
        tempUcapf[tempUcapf < Fmin] = Fmin
        Ucapf = tempUcapf.tolist()
        temp_factor = 273.15 + 20
        H_u = (P_s / (P_s + dP)) * (C_0 + numpy.multiply(C_1, Ucapf) + 
            numpy.multiply(C_2, numpy.power(Ucapf, 2)) + numpy.multiply(C_t, (T_s - temp_factor)))
        return H_u
    

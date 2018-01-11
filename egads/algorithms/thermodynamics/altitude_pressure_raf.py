__author__ = "mfreer, ohenry"
__date__ = "2017-01-12 9:28"
__version__ = "1.2"
__all__ = ["AltitudePressureRaf"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class AltitudePressureRaf(egads_core.EgadsAlgorithm):
    
    """
    FILE        altitude_pressure_raf.py

    VERSION     1.2

    CATEGORY    Thermodynamics

    PURPOSE     Calculate pressure altitude

    DESCRIPTION Calculate pressure altitude using static pressure and the US Standard Atmosphere
                definitions. 

    INPUT       P_s         vector  hPa     static pressure
                
    OUTPUT      H           vector  m       pressure altitude

    SOURCE      NCAR EOL-RAF

    REFERENCES US Standard Atmosphere 1976 (NASA-TM-X-74335), 241 pages. 
               http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19770009539_1977009539.pdf
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m',
                                                               'long_name':'pressure altitude',
                                                               'standard_name':'pressure altitude',
                                                               'Category':['Thermodynamics', 'Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['P_s'],
                                                          'InputUnits':['hPa'],
                                                          'InputTypes':['vector'],
                                                          'InputDescription':['Static pressure'],
                                                          'Outputs':['alt_p'],
                                                          'OutputUnits':['m'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Pressure altitude'],
                                                          'Purpose':'Calculate pressure altitude',
                                                          'Description':'Calculate pressure altitude using static pressure and the US Standard Atmosphere definitions',
                                                          'Category':'Thermodynamics',
                                                          'Source':'NCAR EOL-RAF',
                                                          'References':'US Standard Atmosphere 1976 (NASA-TM-X-74335), 241 pages. http://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/19770009539_1977009539.pdf',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, P_s):
        return egads_core.EgadsAlgorithm.run(self, P_s)

    def _algorithm(self, P_s):
        P_0 = 1013.25  # hPa
        T_0 = 288.15  # K
        R_a = 287.0531  # J/kg/K
        g = 9.80665  # m/s2
        L = 0.0065  # K/m
        P_1 = 226.3206  # hPa
        T_1 = 216.65  # K
        H_1 = 11000.0  # m
        if P_s.size == 1:
            if P_s >= P_1:
                H = (T_0 / L) * (1 - (P_s / P_0) ** (R_a * L / g))
            else:
                H = H_1 + ((R_a * T_1) / g) * numpy.log(P_1 / P_s)
        else:
            H = numpy.zeros(P_s.size)
            H[P_s >= P_1] = (T_0 / L) * (1 - (P_s[P_s >= P_1] / P_0) ** (R_a * L / g))
            H[P_s < P_1] = H_1 + ((R_a * T_1) / g) * numpy.log(P_1 / P_s[P_s < P_1])
        return H

__author__ = "ohenry"
__date__ = "$Date:: 2016-02-04 16:06#$"
__version__ = "$Revision:: 1       $"
__all__ = ["TestAlgorithm1"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import numpy

class TestAlgorithm1(egads_core.EgadsAlgorithm):
    """

    FILE        test_algorithm_1.py

    VERSION     $Revision: 1 $

    CATEGORY    Tests

    PURPOSE     Test EGADS GUI and window dedicated to algorithms

    DESCRIPTION Test EGADS GUI and window dedicated to algorithms

    INPUT       A         vector  hPa     static pressure
                B         vector  hPa     static pressure
                C         vector  hPa     static pressure
                D         vector  hPa     static pressure
                E         vector  hPa     static pressure
                F         vector  hPa     static pressure
                G         vector  hPa     static pressure
                
    OUTPUT      alt_p           vector  m       pressure altitude test
                out_a           vector  m       pressure altitude test
                out_b           vector  m       pressure altitude test

    SOURCE      none

    REFERENCES  none
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m',
                                                               'long_name':'pressure altitude test',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamic', 'Aircraft State', 'Test']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['A','B','C','D','E','F','G','H','I','J','K'],
                                                          'InputUnits':['hPa','hPa','hPa','hPa','hPa','hPa','hPa','hPa','hPa','hPa','hPa'],
                                                          'InputTypes':['coeff.[2]','coeff.[3]','coeff.[4]','coeff.[5]','vector','vector','vector','vector','vector','vector','vector',],
                                                          'Outputs':['alt_p'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now(),
                                                          'Description':'Test EGADS GUI and window dedicated to algorithms'},
                                                          self.output_metadata)



    def run(self, A, B, C, D, E, F, G, H, I, J, K):

        return egads_core.EgadsAlgorithm.run(self, A, B, C, D, E, F, G, H, I, J, K)


    def _algorithm(self, A, B, C, D, E, F, G, H, I, J, K):

        P_0 = 1013.25  # hPa
        T_0 = 288.15  # K
        R_a = 287.0531  # J/kg/K
        g = 9.80665  # m/s2
        L = 0.0065  # K/m

        P_1 = 226.3206  # hPa
        T_1 = 216.65  # K
        H_1 = 11000.0  # m
        
        out_a = 999
        out_b = 333

        if A.size == 1:
            if A >= P_1:
                H = T_0 / L * (1 - (A / P_0) ** (R_a * L / g))
            else:
                H = H_1 + R_a * T_1 / g * numpy.log(P_1 / A)

        else:
            H = numpy.zeros(A.size)

            H[A >= P_1] = T_0 / L * (1 - (A[A >= P_1] / P_0) ** (R_a * L / g))
            H[A < P_1] = H_1 + R_a * T_1 / g * numpy.log(P_1 / A[A < P_1])

        return H

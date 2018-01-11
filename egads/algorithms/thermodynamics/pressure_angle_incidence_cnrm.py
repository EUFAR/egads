__author__ = "mfreer, ohenry"
__date__ = "2016-01-12 13:15"
__version__ = "1.3"
__all__ = ["PressureAngleIncidenceCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
from numpy import multiply, power, zeros, logical_and

class PressureAngleIncidenceCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        pressure_angle_incidence_cnrm.py

    VERSION     1.3

    CATEGORY    Thermodynamic

    PURPOSE     Calculate static pressure, error-corrected dynamic pressure, angle
                of attack and sideslip

    DESCRIPTION Calculates static pressure and dynamic pressure by correction of
                static error. Angle of attack and sideslip are calculated from the 
                horizontal and vertical differential pressures.

    INPUT       P_sr        vector      hPa     raw static pressure
                delta_P_r   vector      hPa     raw dynamic pressure
                delta_P_h   vector      hPa     horizontal differential pressure
                delta_P_v   vector      hPa     vertical differential pressure
                C_alpha     coeff.[2]   _       angle of attack calibration coeff.
                C_beta      coeff.[2]   _       sideslip calibration coeff.
                C_errstat   coeff.[4]   _       static error coefficients

    OUTPUT      P_s         vector      hPa     static pressure
                delta_P     vector      hPa     static error corrected dynamic pressure
                alpha       vector      rad     angle of attack
                beta        vector      rad     sideslip angle

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'hPa',
                                                               'long_name':'static pressure',
                                                               'standard_name':'air_pressure',
                                                               'Category':['Thermodynamics', 'Atmos State']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'hPa',
                                                               'long_name':'dynamic pressure',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamics', 'Atmos State']}))


        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'rad',
                                                               'long_name':'angle of attack',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamics', 'Aircraft State']}))


        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'rad',
                                                               'long_name':'sideslip angle',
                                                               'standard_name':'',
                                                               'Category':['Thermodynamics', 'Aircraft State']}))


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['P_sr', 'deltaP_r', 'deltaP_h', 'deltaP_v', 'C_alpha', 'C_beta', 'C_errstat'],
                                                          'InputUnits':['hPa', 'hPa', 'hPa', 'hPa', '', '', ''],
                                                          'InputTypes':['vector','vector','vector','vector','coeff.[2]','coeff.[2]','coeff.[4]'],
                                                          'InputDescription':['Raw static pressure','Raw dynamic pressure','Horizontal differential pressure','Vertical differential pressure','Angle of attack calibration coefficients','Sideslip calibration coefficients','Static error coefficients'],
                                                          'Outputs':['P_s', 'delta_P', 'alpha', 'beta'],
                                                          'OutputUnits':['hPa', 'hPa', 'rad', 'rad'],
                                                          'OutputTypes':['vector','vector','vector','vector'],
                                                          'OutputDescription':['Static pressure','Static error corrected dynamic pressure','Angle of attack','Sideslip angle'],
                                                          'Purpose':'Calculate static pressure, error-corrected dynamic pressure, angle of attack and sideslip',
                                                          'Description':'Calculates static pressure and dynamic pressure by correction of static error. Angle of attack and sideslip are calculated from the horizontal and vertical differential pressures',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, P_sr, delta_P_r, delta_P_h, delta_P_v, C_alpha, C_beta, C_errstat):
        return egads_core.EgadsAlgorithm.run(self, P_sr, delta_P_r, delta_P_h,
                                             delta_P_v, C_alpha, C_beta, C_errstat)

    def _algorithm(self, P_sr, delta_P_r, delta_P_h, delta_P_v, C_alpha, C_beta, C_errstat):

        errstat25 = (C_errstat[0] + C_errstat[1] * 25 + C_errstat[2] * 25 ** 2 + C_errstat[3] * 25 ** 3)
        errstat = zeros(P_sr.shape)
        errstat[delta_P_r > 25] = (C_errstat[0] + multiply(C_errstat[1], delta_P_r[delta_P_r > 25]) +
                                    multiply(C_errstat[2], power(delta_P_r[delta_P_r > 25], 2)) +
                                    multiply(C_errstat[3], power(delta_P_r[delta_P_r > 25], 3)))
        errstat[logical_and(delta_P_r > 0, delta_P_r <= 25)] = (delta_P_r[logical_and(delta_P_r > 0, 
                                                                delta_P_r <= 25)] / 25) * errstat25
        P_s = P_sr - errstat
        delta_P = delta_P_r + errstat
        alpha = C_alpha[0] + C_alpha[1] * (delta_P_v / delta_P)
        beta = C_beta[0] + C_beta[1] * (delta_P_h / delta_P)
        return P_s, delta_P, alpha, beta


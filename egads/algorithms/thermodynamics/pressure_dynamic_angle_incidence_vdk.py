__author__ = "ohenry"
__date__ = "2017-01-12 11:26"
__version__ = "0.9"
__all__ = ["PressureAngleIncidenceVdk"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class PressureAngleIncidenceVdk(egads_core.EgadsAlgorithm):
    
    """
    FILE        pressure_dynamic_angle_incidence_vdk.py

    VERSION     0.9

    CATEGORY    Thermodynamic

    PURPOSE     Calculate dynamic pressure, angle of attack and sideslip. WARNING: BETA !

    DESCRIPTION Calculates dynamic pressure and angles of incidence from a 5-hole probe
                using differences between the ports. The algorithm requires calibration 
                coefficients which are obtained by a calibration procedure of the probe
                at predefined airflow angles. See van den Kroonenberg, 2008, for more 
                details on the calibration procedure.

    INPUT       delta_P_t   vector          hPa     pressure difference between top port and center port
                delta_P_b   vector          hPa     pressure difference between bottom port and center port
                delta_P_l   vector          hPa     pressure difference between left port and center port
                delta_P_r   vector          hPa     pressure difference between right port and center port
                delta_P_s   vector          hPa     pressure difference between center port and static pressure
                C_alpha     coeff.[11,11]   ()      angle of attack calibration coeff.
                C_beta      coeff.[11,11]   ()      sideslip calibration coeff.
                C_dyn       coeff.[11,11]   ()      dynamic pressure calibration coeff.

    OUTPUT      P_d         vector      hPa     dynamic pressure
                alpha       vector      rad     angle of attack
                beta        vector      rad     sideslip angle

    SOURCE      

    REFERENCES  A.C. van der Kroonenberg et al, "Measuring the wind vector using the 
                autonomous mini aerial vehicle M^2AV", J. Atmos. Oceanic Technol., 25 
                (2008), pp. 1969-1982.
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'hPa',
                                                                     'long_name':'dynamic pressure',
                                                                     'standard_name':'',
                                                                     'Category':['Thermodynamics',
                                                                                 'Atmos State']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'rad',
                                                                     'long_name':'angle of attack',
                                                                     'standard_name':'',
                                                                     'Category':['Thermodynamics',
                                                                                 'Aircraft State']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'rad',
                                                                     'long_name':'sideslip angle',
                                                                     'standard_name':'',
                                                                     'Category':['Thermodynamics',
                                                                                 'Aircraft State']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['delta_P_t', 'delta_P_b', 'delta_P_l', 'delta_P_r', 'delta_P_s', 'C_alpha', 'C_beta', 'C_dyn'],
                                                          'InputUnits':['hPa', 'hPa', 'hPa', 'hPa', 'hPa', '', '', ''],
                                                          'InputTypes':['vector','vector','vector','vector','vector','coeff.[11,11]','coeff.[11,11]','coeff.[11,11]'],
                                                          'InputDescription':['Pressure difference between top port and center port',
                                                                              'Pressure difference between bottom port and center port',
                                                                              'Pressure difference between left port and center port',
                                                                              'Pressure difference between right port and center port',
                                                                              'Pressure difference between center port and static pressure',
                                                                              'Angle of attack calibration coefficients',
                                                                              'Sideslip calibration coefficients',
                                                                              'Dynamic pressure calibration coefficients'],
                                                          'Outputs':['P_d', 'alpha', 'beta'],
                                                          'OutputUnits':['hPa','rad','rad'],
                                                          'OutputTypes':['vector','vector','vector'],
                                                          'OutputDescription':['Dynamic pressure','Angle of attack','Sideslip angle'],
                                                          'Purpose':'Calculate dynamic pressure, angle of attack and sideslip',
                                                          'Description':'Calculates dynamic pressure and angles of incidence from a 5-hole probe'
                                                                        + ' using differences between the ports. The algorithm requires calibration'
                                                                        + ' coefficients which are obtained by a calibration procedure of the probe'
                                                                        + ' at predefined airflow angles. See van den Kroonenberg, 2008, for more '
                                                                        + ' details on the calibration procedure.',
                                                          'Category':'Thermodynamics',
                                                          'Source':'',
                                                          'References':'A.C. van der Kroonenberg et al, "Measuring the wind vector using the autonomous mini aerial vehicle M^2AV", J. Atmos. Oceanic Technol., 25 (2008), pp. 1969-1982.',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, delta_P_t, delta_P_b, delta_P_l, delta_P_r, delta_P_s, C_alpha, C_beta, C_dyn):
        return egads_core.EgadsAlgorithm.run(self, delta_P_t, delta_P_b, delta_P_l, delta_P_r, 
                                             delta_P_s, C_alpha, C_beta, C_dyn)

    def _algorithm(self, delta_P_t, delta_P_b, delta_P_l, delta_P_r, delta_P_s, C_alpha, C_beta, C_dyn):

        print 'Warning: the algorithm is still in beta phase and must be reviewed.'

        P_tot =  (numpy.sqrt((1. / 125.) * ((delta_P_t + delta_P_r + delta_P_b + delta_P_l)**2 
                                      + (- 4 * delta_P_t + delta_P_r + delta_P_b + delta_P_l)**2
                                      + (delta_P_t - 4 * delta_P_r + delta_P_b + delta_P_l)**2 
                                      + (delta_P_t + delta_P_r - 4 * delta_P_b + delta_P_l)**2
                                      + (delta_P_t + delta_P_r + delta_P_b - 4 * delta_P_l)**2)) 
                  + (1./4.) * (delta_P_t + delta_P_r + delta_P_b + delta_P_l)) 
        k_a = (delta_P_t - delta_P_b) / P_tot
        k_b = (delta_P_r - delta_P_l) / P_tot

        sum_out = numpy.zeros((12, len(k_a)))
        for i in range(0,12):
            sum_in = numpy.zeros((12, len(k_b)))
            for j in range(0,12):
                sum_in[j] = C_alpha[i][j] * (k_b ** j)
            sum_out[i] = (k_a**i) * numpy.sum(sum_in, axis = 0)
        alpha_cp = numpy.sum(sum_out, axis = 0)
        
        sum_out = numpy.zeros((12, len(k_a)))
        for i in range(0,12):
            sum_in = numpy.zeros((12, len(k_b)))
            for j in range(0,12):
                sum_in[j] = C_beta[i][j] * (k_b ** j)
            sum_out[i] = (k_a**i) * numpy.sum(sum_in, axis = 0)
        beta_cp = numpy.sum(sum_out, axis = 0)

        sum_out = numpy.zeros((12, len(k_a)))
        for i in range(0,12):
            sum_in = numpy.zeros((12, len(k_b)))
            for j in range(0,12):
                sum_in[j] = C_dyn[i][j] * (k_b ** j)
            sum_out[i] = (k_a**i) * numpy.sum(sum_in, axis = 0)
        k_q = numpy.sum(sum_out, axis = 0)
        
        P_d = delta_P_s + P_tot * k_q
        alpha = alpha_cp
        beta = numpy.arctan(numpy.tan(beta_cp) / numpy.cos(alpha_cp))
        
        return P_d, alpha, beta


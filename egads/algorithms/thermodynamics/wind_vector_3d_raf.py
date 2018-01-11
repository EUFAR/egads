__author__ = "mfreer"
__date__ = "2012-06-22 17:19"
__version__ = "1.2"
__all__ = ['WindVector3dRaf']

from numpy import sin, cos, tan, sqrt
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class WindVector3dRaf(egads_core.EgadsAlgorithm):
    
    """
    FILE        wind_vector_3d_raf.py

    VERSION     1.2

    CATEGORY    Thermodynamics

    PURPOSE     Calculation of 3d wind vector components.

    DESCRIPTION This algorithm applies vector transformations using aircraft speed,
                angle of attack and sideslip to calculate the three-dimensional
                wind vector components.

    INPUT       U_a        vector    m/s    corrected true air speed
                alpha      vector    rad    aircraft angle of attack
                beta       vector    rad    aircraft sideslip angle
                u_p        vector    m/s    easterly aircraft velocity from INS
                v_p        vector    m/s    northerly aircraft velocity from INS
                w_p        vector    m/s    upward aircraft velocity from INS
                phi        vector    rad    roll angle
                theta      vector    rad    pitch angle
                psi        vector    rad    true heading
                theta_dot  vector    rad/s  pitch rate
                psi_dot    vector    rad/s  roll rate
                L          coeff     m      distance separating INS and gust probe
                                          along aircraft center line

    OUTPUT      u          vector    m/s    easterly wind velocity component
                v          vector    m/s    northerly wind velocity component
                w          vector    m/s    upward wind velocity component
              
    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin #23

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'easterly wind velocity',
                                                               'standard_name':'eastward_wind',
                                                               'Category':['Thermodynamics', 'Wind']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'northerly wind velocity',
                                                               'standard_name':'northward_wind',
                                                               'Category':['Thermodynamics', 'Wind']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'upward wind velocity',
                                                               'standard_name':'upward_air_velocity',
                                                               'Category':['Thermodynamics', 'Wind']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['U_a', 'alpha', 'beta',
                                                                    'u_p', 'v_p', 'w_p',
                                                                    'phi', 'theta', 'psi',
                                                                    'theta_dot', 'psi_dot', 'L'],
                                                          'InputUnits':['m/s', 'rad', 'rad',
                                                                        'm/s', 'm/s', 'm/s',
                                                                        'rad', 'rad', 'rad',
                                                                        'rad/s', 'rad/s', 'm'],
                                                          'InputTypes':['vector','vector','vector','vector','vector','vector','vector','vector','vector','vector','vector','coeff'],
                                                          'InputDescription':['Corrected true air speed','Aircraft angle of attack','Aircraft sideslip angle','Easterly aircraft velocity from INS','Northerly aircraft velocity from INS','Upward aircraft velocity from INS','Roll angle','Pitch angle','True heading','Pitch rate','Roll rate','Distance separating INS and gust probe along aircraft center line'],
                                                          'Outputs':['u', 'v', 'w'],
                                                          'OutputUnits':['m/s','m/s','m/s'],
                                                          'OutputTypes':['vector','vector','vector'],
                                                          'OutputDescription':['Easterly wind velocity component','Northerly wind velocity component','Upward wind velocity component'],
                                                          'Purpose':'Calculation of 3d wind vector components',
                                                          'Description':'This algorithm applies vector transformations using aircraft speed, angle of attack and sideslip to calculate the three-dimensional wind vector components',
                                                          'Category':'Thermodynamics',
                                                          'Source':'NCAR-RAF',
                                                          'References':'NCAR-RAF Bulletin #23',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, U_a, alpha, beta, u_p, v_p, w_p, phi, theta, psi, theta_dot, psi_dot, L):
        return egads_core.EgadsAlgorithm.run(self, U_a, alpha, beta, u_p, v_p, w_p, phi, theta, psi, theta_dot, psi_dot, L)

    def _algorithm(self, U_a, alpha, beta, u_p, v_p, w_p, phi, theta, psi, theta_dot, psi_dot, L):
        D = sqrt(1 + tan(alpha) ** 2 + tan(beta) ** 2)
        u = ((-U_a / D) * (sin(psi) * cos(theta) + tan(beta) * (cos(psi) * cos(phi) 
                         + sin(psi) * sin(theta) * sin(phi)) + tan(alpha) * (sin(psi) * sin(theta) * cos(phi) 
                         - cos(psi) * sin(phi))) + u_p - L * (theta_dot * sin(theta) * sin(psi) - psi_dot * cos(psi) * cos(theta)))
        v = ((-U_a / D) * (cos(psi) * cos(theta) -
                         tan(beta) * (sin(psi) * cos(phi) - cos(psi) * sin(theta) * sin(phi)) +
                         tan(alpha) * (cos(psi) * sin(theta) * cos(phi) + sin(psi) * sin(phi))) +
             v_p - L * (psi_dot * sin(psi) * cos(theta) + theta_dot * cos(psi) * sin(theta)))
        w = ((-U_a / D) * (sin(theta) - tan(beta) * cos(theta) * sin(phi) -
                         tan(alpha) * cos(theta) * cos(phi)) +
             w_p + L * theta_dot * cos(theta))
        return u, v, w


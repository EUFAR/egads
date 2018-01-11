__author__ = "mfreer"
__date__ = "2012-08-24 08:41"
__version__ = "1.3"
__all__ = ['ScatteringAngles']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class ScatteringAngles(egads_core.EgadsAlgorithm):
    
    """
    FILE        scattering_angles.py

    VERSION     1.3

    CATEGORY    Radiation

    PURPOSE     Calculates the scattering angle for each pixel on an image given the camera
                viewing angle and solar vector.

    DESCRIPTION Calculates the scattering angle for each pixel on an image given the camera
                viewing angle and solar vector.

    INPUT       n_x        coeff            _        number of pixels in x dimension
                n_y        coeff            _        number of pixels in y dimension
                theta_c    array[n_x,n_y]   deg      camera viewing zenith angle
                phi_c      array[n_x,n_y]   deg      camera viewing azimuth angle (0 deg = flight dir)
                theta_sun  coeff            deg      solar zenith angle
                phi_sun    coeff            deg      solar azimuth angle

    OUTPUT      theta_scat    array[n_x, n_y]    deg    scattering angles of each pixel

    SOURCE      Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)
        self.output_metadata = egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'scattering angle',
                                                               'standard_name':'',
                                                               'Category':['Radiation']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_x', 'n_y', 'theta_c', 'phi_c', 'theta_sun', 'phi_sun'],
                                                          'InputUnits':['', '', 'deg', 'deg', 'deg', 'deg'],
                                                          'InputTypes':['coeff', 'coeff', 'array', 'array', 'coeff', 'coeff'],
                                                          'InputDescription':['Number of pixels in x dimension',
                                                                              'Number of pixels in y dimension',
                                                                              'Camera viewing zenith angle',
                                                                              'Camera viewing azimuth angle (0 deg = flight dir)',
                                                                              'Solar zenith angle',
                                                                              'Solar azimuth angle'],
                                                          'Outputs':['theta_scat'],
                                                          'OutputUnits':['deg'],
                                                          'OutputTypes':['array[n_x, n_y]'],
                                                          'OutputDescription':['Scattering angles of each pixel'],
                                                          'Purpose':'Calculates the scattering angle for each pixel on an image given the camera viewing angle and solar vector',
                                                          'Description':'No description',
                                                          'Category':'Radiation',
                                                          'Source':'Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_x, n_y, theta_c, phi_c, theta_sun, phi_sun):
        return egads_core.EgadsAlgorithm.run(self, n_x, n_y, theta_c, phi_c, theta_sun, phi_sun)

    def _algorithm(self, n_x, n_y, theta_c, phi_c, theta_sun, phi_sun):
        sin = numpy.sin
        cos = numpy.cos
        rad2deg = 180 / numpy.pi
        deg2rad = numpy.pi / 180.0
        theta_sun_r = theta_sun * deg2rad
        phi_sun_r = phi_sun * deg2rad
        theta_c_r = theta_c * deg2rad
        phi_c_r = phi_c * deg2rad
        theta_scat_r = numpy.arccos(-sin(theta_sun_r) * cos(phi_sun_r) * sin(theta_c_r) * cos(phi_c_r)
                                  - sin(theta_sun_r) * sin(phi_sun_r) * sin(theta_c_r) * cos(phi_c_r)
                                  + cos(theta_sun_r) * cos(theta_c_r))
        theta_scat = theta_scat_r * rad2deg
        return theta_scat


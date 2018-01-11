__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.3"
__all__ = ['CameraViewingAngles']

import egads
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class CameraViewingAngles(egads_core.EgadsAlgorithm):
    
    """
    FILE        camera_viewing_angles.py

    VERSION     1.3

    CATEGORY    Radiation

    PURPOSE     Calculates per-pixel camera viewing angles for a digital camera image

    DESCRIPTION Calculates per-pixel camera viewing angles of a digital camera given 
                its sensor dimension and focal length. x--y coordinates are defined 
                as having the left side of the image (x=0) aligned with the flight 
                direction and y=0 to the top of the image.

    INPUT       n_x        coeff        _        number of pixels in x direction
                n_y        coeff        _        number of pixels in y direction
                l_x        coeff        mm       length of the camera sensor in x direction
                l_y        coeff        mm       length of the camera sensor in y direction
                f          coeff        mm       focal length of the camera lens

    OUTPUT      theta_c    array[n_x, n_y]    degrees    camera viewing zenith angle
                phi_c      array[n_x, n_y]    degrees    camera viewing azimuth angle (mathematic
                                                         negative system with 0 deg into flight direction)

    SOURCE      Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'camera viewing zenith angle',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'camera viewing azimuth angle',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_x', 'n_y', 'l_x', 'l_y', 'f'],
                                                          'InputUnits':['', '', 'mm', 'mm', 'mm'],
                                                          'InputTypes':['coeff','coeff','coeff','coeff','coeff'],
                                                          'InputDescription':['Number of pixels in x direction','Number of pixels in y direction','Length of the camera sensor in x direction','Length of the camera sensor in y direction','Focal length of the camera lens'],
                                                          'Outputs':['theta_c', 'phi_c'],
                                                          'OutputUnits':['deg','deg'],
                                                          'OutputTypes':['array[n_x, n_y]','array[n_x, n_y]'],
                                                          'OutputDescription':['Camera viewing zenith angle','Camera viewing azimuth angle (mathematic negative system with 0 deg into flight direction)'],
                                                          'Purpose':'Calculates per-pixel camera viewing angles for a digital camera image',
                                                          'Description':'Calculates per-pixel camera viewing angles of a digital camera given its sensor dimension and focal length. x--y coordinates are defined as having the left side of the image (x=0) aligned with the flight direction and y=0 to the top of the image',
                                                          'Category':'Radiation',
                                                          'Source':'Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_x, n_y, l_x, l_y, f):
        return egads_core.EgadsAlgorithm.run(self, n_x, n_y, l_x, l_y, f)

    def _algorithm(self, n_x, n_y, l_x, l_y, f):
        AngleLimit = egads.algorithms.mathematics.LimitAngleRange  # @UndefinedVariable
        theta_c = numpy.zeros([n_x, n_y])
        phi_c = numpy.zeros([n_x, n_y])
        for i in range(n_x):
            x = (i - n_x / 2.) / n_x * l_x
            for j in range(n_y):
                y = (j - n_y / 2.) / n_y * l_y
                d = numpy.sqrt(x ** 2 + y ** 2)
                theta_c[i, j] = AngleLimit().run(2 * numpy.arctan(d / (2. * f)) * 180.0 / numpy.pi)
                phi_c[i, j] = AngleLimit().run(360 - numpy.arctan2(y, x) * 180.0 / numpy.pi)
        return theta_c, phi_c


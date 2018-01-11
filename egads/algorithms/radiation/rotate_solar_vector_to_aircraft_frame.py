__author__ = "mfreer, ohenry"
__date__ = "2016-01-11 9:31"
__version__ = "1.3"
__all__ = ['RotateSolarVectorToAircraftFrame']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy
import egads

class RotateSolarVectorToAircraftFrame(egads_core.EgadsAlgorithm):
    
    """
    FILE        rotate_solar_vector_to_aircraft_frame.py

    VERSION     1.3

    CATEGORY    Radiation

    PURPOSE     Rotates polar solar vector by rotation of aircraft roll, pitch and yaw.

    DESCRIPTION Rotates polar solar vector by rotation of aircraft roll, pitch and yaw.

    INPUT       theta_sun    vector    degrees    solar zenith
                phi_sun      vector    degrees    solar azimuth (mathematic negative, north=0 deg)
                roll         vector    degrees    aircraft roll (mathematic positive, left wing up=positive)
                pitch        vector    degrees    aircraft pitch (mathematic positive, nose down=positive)
                yaw          vector    degrees    aircraft yaw (mathematic negative, north=0 deg)
                
    OUTPUT      theta_new    vector    degrees    solar zenith, aircraft coordinates
                phi_new      vector    degrees    solar azimuth, aircraft coordinates (mathematic negative, north
                                                                                       north=0 deg)

    SOURCE      Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'solar zenith, aircraft coordinates',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'solar azimuth, aircraft coordinates',
                                                               'standard_name':'',
                                                               'Category':['Radiation']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['theta_sun', 'phi_sun', 'roll', 'pitch', 'roll'],
                                                          'InputUnits':['deg', 'deg', 'deg', 'deg', 'deg'],
                                                          'InputTypes':['vector','vector','vector','vector','vector'],
                                                          'InputDescription':['Solar zenith',
                                                                              'Solar azimuth (mathematic negative, north=0 deg)',
                                                                              'Aircraft roll (mathematic positive, left wing up=positive)',
                                                                              'Aircraft pitch (mathematic positive, nose down=positive)',
                                                                              'Aircraft yaw (mathematic negative, north=0 deg)'],
                                                          'Outputs':['theta_new', 'phi_new'],
                                                          'OutputUnits':['deg','deg'],
                                                          'OutputTypes':['vector','vector'],
                                                          'OutputDescription':['Solar zenith, aircraft coordinates','Solar azimuth, aircraft coordinates (mathematic negative, north=0 deg)'],
                                                          'Purpose':'Rotates polar solar vector by rotation of aircraft roll, pitch and yaw',
                                                          'Description':'No description',
                                                          'Category':'Radiation',
                                                          'Source':'Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, theta_sun, phi_sun, roll, pitch, yaw):
        return egads_core.EgadsAlgorithm.run(self, theta_sun, phi_sun, roll, pitch, yaw)

    def _algorithm(self, theta_sun, phi_sun, roll, pitch, yaw):
        cos = numpy.cos
        sin = numpy.sin
        deg2rad = numpy.pi / 180.0
        rad2deg = 180.0 / numpy.pi
        phi_sun = 360 - phi_sun
        yaw = 360 - yaw
        theta_sun_r = theta_sun * deg2rad
        phi_sun_r = phi_sun * deg2rad
        roll_r = roll * deg2rad
        pitch_r = pitch * deg2rad
        yaw_r = yaw * deg2rad
        x = sin(theta_sun_r) * cos(phi_sun_r)
        y = sin(theta_sun_r) * sin(phi_sun_r)
        z = cos(theta_sun_r)
        xx = x * (cos(pitch_r) * cos(yaw_r)) + y * (cos(pitch_r) * sin(yaw_r)) + z * (-sin(pitch_r))
        yy = (x * (sin(roll_r) * sin(pitch_r) * cos(yaw_r) - cos(roll_r) * sin(yaw_r))
              + y * (sin(roll_r) * sin(pitch_r) * sin(yaw_r) + cos(roll_r) * cos(yaw_r))
              + z * (sin(roll_r) * cos(pitch_r)))
        zz = (x * (cos(roll_r) * sin(pitch_r) * cos(yaw_r) + sin(roll_r) * sin(yaw_r))
              + y * (cos(roll_r) * sin(pitch_r) * sin(yaw_r) - sin(roll_r) * cos(yaw_r))
              + z * (cos(roll_r) * cos(pitch_r)))
        theta_new = numpy.arccos(zz / numpy.sqrt(xx ** 2 + yy ** 2 + zz ** 2)) * rad2deg
        phi_new = egads.EgadsData(value=360, units='deg', long_name='') - egads.algorithms.mathematics.LimitAngleRange().run(numpy.arctan(yy / xx) * rad2deg)  # @UndefinedVariable
        return theta_new, phi_new


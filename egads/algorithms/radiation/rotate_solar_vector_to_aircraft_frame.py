__author__ = "mfreer"
__date__ = "$Date:: 2012-02-03 17:40#$"
__version__ = "$Revision:: 118       $"
__all__ = ['RotateSolarVectorToAircraftFrame']


import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import numpy
import egads

class RotateSolarVectorToAircraftFrame(egads_core.EgadsAlgorithm):
    """
    FILE        rotate_solar_vector_to_aircraft_frame.py

    VERSION     $Revision: 118 $

    CATEGORY    Radiation

    PURPOSE     Rotates polar solar vector by rotation of aircraft roll, pitch and yaw.

    DESCRIPTION ...

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
                                                          'Outputs':['theta_new', 'phi_new'],
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
        phi_new = numpy.arctan(yy / xx) * rad2deg

        phi_new = 360 * egads.units.deg - egads.algorithms.mathematics.LimitAngleRange().run(phi_new)



        return theta_new, phi_new



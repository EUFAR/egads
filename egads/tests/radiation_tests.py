"""
Test suite to verify complete functioning of all Radiation algorithms.
"""

__author__ = "henry"
__date__ = "2017-1-10 14:25"
__version__ = "1.3"
__all__ = ['RadiationTestCase']

import unittest
import numpy as np
from egads.algorithms import radiation


class RadiationTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_camera_viewing_angle(self):
        res_theta = [[16.588,14.529,14.529],
                     [9.808,5.564,5.564],
                     [9.808,5.564,5.564]]
        res_phi = [[149.036,168.690,191.310],
                   [119.055,149.036,210.964],
                   [60.945,30.964,329.036]]
        theta, phi = radiation.CameraViewingAngles().run(3, 3, 10, 6, 20)
        for i, _ in np.ndenumerate(theta):
            self.assertAlmostEqual(theta.value[i[0]][i[1]], res_theta[i[0]][i[1]], 3, "Theta values dont match")
            self.assertAlmostEqual(phi.value[i[0]][i[1]], res_phi[i[0]][i[1]], 3, "Phi values dont match")
            
    def test_planck_emission(self):
        res_emission = radiation.PlanckEmission().run(273, 500)
        self.assertAlmostEqual(res_emission.value, 6.35e-40, 42, "Planck emission dont match")
        
    def test_rotate_solar_vector(self):
        solar_zenith = [-90.0,-45.0,0.0,33.0,66.0]
        solar_azimuth = [0.0,150.0,180.0,20.0,320.0]
        roll = [0.0,-2.0,10.0,3.0,0.0]
        pitch = [-1.0,5.1,0.01,3.0,1.0]
        yaw = [1.0,0.0,0.0,3.23,11.0,]
        solar_zenith_ai = [89.0, 39.6, 10.0, 29.3, 65.4]
        solar_azimuth_ai = [359.0,329.1,89.9,13.2,308.6]
        solar_zenith_cp, solar_azimuth_cp = radiation.RotateSolarVectorToAircraftFrame().run(solar_zenith, solar_azimuth, roll, pitch, yaw)
        for i, _ in enumerate(solar_zenith_ai):
            self.assertAlmostEqual(solar_zenith_cp.value[i], solar_zenith_ai[i], 1, "Solar zenith dont match")
            self.assertAlmostEqual(solar_azimuth_cp.value[i], solar_azimuth_ai[i], 1, "Solar azimuth dont match")
    
    def test_scattering_angles(self):
        res_theta = [[70.464,70.364,70.364],
                     [83.512,83.479,83.479],
                     [96.488,96.521,96.521]]
        theta, phi = radiation.CameraViewingAngles().run(3, 3, 10, 6, 20)
        theta= radiation.ScatteringAngles().run(3, 3, theta, phi, 90, 60)
        for i, _ in np.ndenumerate(res_theta):
            self.assertAlmostEqual(theta.value[i[0]][i[1]], res_theta[i[0]][i[1]], 3, "Theta values dont match")
    
    def test_solar_vector_blanco(self):
        ra, delta, theta, gamma = radiation.SolarVectorBlanco().run('20041231T104352', -30.3, 0.0)
        self.assertAlmostEqual(ra.value, 4.90, 2, 'Right ascension values dont match')
        self.assertAlmostEqual(delta.value, -0.402, 3, 'Declination values dont match')
        self.assertAlmostEqual(theta.value, 0.333, 3, 'Solar zenith values dont match')
        self.assertAlmostEqual(gamma.value, 1.26, 2, 'Solar azimuth values dont match')
        
    def test_solar_vector_resa_andreas(self):
        theta, phi = radiation.SolarVectorReda().run('20120821T230005', 15.0, -145.0, 150.0, 1024)
        self.assertAlmostEqual(theta.value, 19.05, 2, 'Solar zenith values dont match')
        self.assertAlmostEqual(phi.value, 262.45, 2, 'Solar azimuth values dont match')
    
    def test_temp_black_body(self):
        temperature = radiation.TempBlackbody().run(0.0000001, 500)
        self.assertAlmostEqual(temperature.value, 920.214, 3, 'Temperature values dont match')


def suite():
    egads_radiation_suite = unittest.TestLoader().loadTestsFromTestCase(RadiationTestCase)
    return unittest.TestSuite([egads_radiation_suite])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

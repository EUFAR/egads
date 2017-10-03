"""
Test suite to verify complete functioning of all Microphysics algorithms.
"""

__author__ = "henry"
__date__ = "2017-1-5 14:48"
__version__ = "1.4"
__all__ = ['MicrophysicsTestCase']

import unittest
import egads
from egads.algorithms import microphysics


class MicrophysicsTestCase(unittest.TestCase):
    def setUp(self):
        self.C1 = egads.EgadsData(value=[[11,10.5,20.21],  
                                        [33,150,20]],
                                 units='cm^-3',
                                 long_name='number concentration of hydrometeors')
        
        self.C2 = egads.EgadsData(value=[[11,10, 20],  
                                        [33,150,20]],
                                 units='',
                                 long_name='number concentration of hydrometeors')
        
        self.C3 = egads.EgadsData(value=[[0.01,0,0.0001],  
                                        [0.0,3.1,2.0]],
                                 units='cm^-3',
                                 long_name='number concentration of hydrometeors')
        
        self.C4 = egads.EgadsData(value=[[1.0,0.03,12.0],  
                                        [0.0,3.0,12.0]],
                                 units='cm^-3',
                                 long_name='number concentration of hydrometeors')
        
        self.C5 = egads.EgadsData(value=[[0.3,0.2,0.5],  
                                        [0.7,0.6,0.1]],
                                 units='cm^-3',
                                 long_name='number concentration of hydrometeors')
        
        self.D1 = egads.EgadsData(value=[1,1.2,3],
                                 units='um',
                                 long_name='average diameter')
        
        self.D2 = egads.EgadsData(value=[0.1,1.0,2.0],
                                 units='um',
                                 long_name='average diameter')
        
        self.D3 = egads.EgadsData(value=[0.3,0.5,0.1],
                                 units='um',
                                 long_name='average diameter')
        
        self.S1 = egads.EgadsData(value=[[1,0.5,3],
                                         [1,0.9,1.1]],
                                 units='',
                                 long_name='shape factors')
        
        self.S2 = egads.EgadsData(value=[[1.1,1.2,1],
                                         [0.9,1.1,0.98]],
                                 units='',
                                 long_name='shape factors')
        
        self.De1 = egads.EgadsData(value=[0.01,2,7],
                                 units='g/cm^3',
                                 long_name='density')
        
        self.De2 = egads.EgadsData(value=[0.4,11,0.2],
                                 units='g/cm^3',
                                 long_name='density')
        
        
        self.E1 = egads.EgadsData(value=[2,5,1],
                                 units='',
                                 long_name='extinction efficiency')
        
        self.P1 = egads.EgadsData(value=[[3.0,10.0,2.0,1.0],
                                         [7.0,2.0,3.0,1.0]],
                                  units='',
                                  long_name='number of particles')
        
        self.V1 = egads.EgadsData(value=[3.0,2.0,1.0,1.0],
                                  units='m^3',
                                  long_name='sample volume')

    def test_effective_radius_dmt(self):
        result = [2.07,1.45]
        res_radius = microphysics.DiameterEffectiveDmt().run(self.C1, self.D1)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_radius.value[index], value, 2, 'Effective diameters dont match')

    def test_mean_diameter_raf(self):
        result = [2.02,1.34]
        res_radius = microphysics.DiameterMeanRaf().run(self.C2, self.D1)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_radius.value[index], value, 2, 'Mean diameters dont match')

    def test_median_volume_diameter_dmt(self):
        result = [2.097, 2.059]
        res_radius = microphysics.DiameterMedianVolumeDmt().run(self.C3, self.D1, self.S1, self.De1)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_radius.value[index], value, 3, 'Median volume diameters dont match')
    
    def test_extinction_coeff_dmt(self):
        result = [0.0378, 0.0495]
        res_coeff = microphysics.ExtinctionCoeffDmt().run(self.C4, self.D2, self.E1)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_coeff.value[index], value, 3, 'Extinction coefficients dont match')

    def test_mass_concentration_dmt(self):
        result = [3.02e-11, 3.88e-11]
        res_mass = microphysics.MassConcDmt().run(self.C4, self.D2, self.S1[0], self.De2)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_mass.value[index], value, 13, 'Extinction coefficients dont match')
        
    def test_total_number_concentration_dmt(self):
        result = [13.03,15.00]
        res_number = microphysics.NumberConcTotalDmt().run(self.C4)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_number.value[index], value, 2, 'Total number concentration dont match')
        
    def test_total_number_concentration_raf(self):
        result = [9.00,7.33]
        res_number = microphysics.NumberConcTotalRaf().run(self.P1, self.V1)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_number.value[index], value, 2, 'Total number concentration dont match')
    
    def test_sample_area_all_in_raf(self):
        result = [1.97e-10, 3.94e-10,0.0,-1.577e-9]
        res_area = microphysics.SampleAreaOapAllInRaf().run(831.0,0.3,3.2,0.6,4.0)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_area.value[index], value, 12, 'Sample areas dont match')
            
    def test_sample_area_center_in_raf(self):
        result = [3.94e-10, 1.577e-9, 3.549e-9, 6.309e-9]
        res_area = microphysics.SampleAreaOapCenterInRaf().run(831.0,0.3,3.2,0.6,4.0)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_area.value[index], value, 12, 'Sample areas dont match')
    
    def test_sample_area_scattering_raf(self):
        res_area = microphysics.SampleAreaScatteringRaf().run(0.1, 0.5)
        self.assertEqual(res_area.value, 0.05, 'Sample areas dont match')
    
    def test_sample_volume_general_raf(self):
        result = [[0,0],[0.05,0.001]]
        tas = egads.EgadsData(value=[0,10],
                              units='m/s',
                              long_name='true air speed')
        sample_area= egads.EgadsData(value=[0.05,0.001],
                                     units='m^2',
                                     long_name='sample areas of probes')
        res_volume = microphysics.SampleVolumeGeneralRaf().run(tas, sample_area, 0.1)
        for index, value in enumerate(result):
            self.assertListEqual(res_volume.value[index].tolist(), value, 'Sample volumes dont match')
    
    def test_surface_area_concentration_dmt(self):
        result = [0.298, 0.700]
        res_conc = microphysics.SurfaceAreaConcDmt().run(self.C5, self.D3, self.S2)
        for index, value in enumerate(result):
            self.assertAlmostEqual(res_conc.value[index], value,3, 'Surface area concentration dont match')

def suite():
    egads_microphysics_suite = unittest.TestLoader().loadTestsFromTestCase(MicrophysicsTestCase)
    return unittest.TestSuite([egads_microphysics_suite])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

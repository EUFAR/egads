"""
Test suite to verify complete functioning of all Corrections, Mathematics and Transforms 
algorithms.
"""

__author__ = "henry"
__date__ = "2017-1-2 15:43"
__version__ = "1.1"
__all__ = ['CorrectionsTestCase', 'MathematicsTestCase', 'ConversionsTestCase']

import numpy
import unittest
import egads
from egads.algorithms import corrections
from egads.algorithms import mathematics
from egads.algorithms import transforms
from numpy import nan


class CorrectionsTestCase(unittest.TestCase):
    def setUp(self):
        self.sea_level = egads.EgadsData(value=[2,5,3,-1,4,15,5,3,6,4,2,-2,-16,-4,1,3,7,2,18,-1,-5,3,-2,4,1],
                                           units='mm',
                                           long_name='sea level anomalies')
        self.corr_sea_level = [2,5,3,-1,4,4,5,3,6,4,2,-2,-3,-4,1,3,7,2,0,-1,-5,3,-2,4,1]
        self.array_test = numpy.zeros(25) + 10
        self.array_shape = self.array_test.shape

    def test_correction_spike_cnrm(self):
        
        print self.sea_level.value
        
        
        res_corr = corrections.CorrectionSpikeSimpleCnrm().run(self.sea_level, 5)
        
        print res_corr.value
        
        
        self.assertListEqual(res_corr.value.tolist(), self.corr_sea_level, 'The test vector and corrected vector dont match')
        res_corr = corrections.CorrectionSpikeSimpleCnrm().run(self.array_test, 5)
        self.assertEqual(res_corr.shape, self.array_shape, 'Sea level array shapes dont match')


class MathematicsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_derivative_time(self):
        sea_level = egads.EgadsData(value=[1,4,9,16,25,36,49,64,81], # f(x^2)
                                    units='mm',
                                    long_name='sea level anomalies')
        time = egads.EgadsData(value=[1,2,3,4,5,6,7,8,9],
                               units='s',
                               long_name='time')
        deriv_sea_level = [2,4,6,8,10,12,14,16,18] # f(2x)
        array_test = numpy.zeros(9) + 10
        array_shape = array_test.shape
        res_deriv = mathematics.DerivativeWrtTime().run(sea_level, time)
        self.assertListEqual(res_deriv.value.tolist()[1:-1], deriv_sea_level[1:-1], 'The test vector and derivated vector dont match')
        res_deriv = mathematics.DerivativeWrtTime().run(array_test, time)
        self.assertEqual(res_deriv.shape, array_shape, 'Sea level array shapes dont match')
        

class TransformsTestCase(unittest.TestCase):
    def setUp(self):
        self.sea_level = egads.EgadsData(value=[1.0,2.0,4.0,5.0,6.0,8.0,11.0,12.0],
                                         units='mm',
                                         long_name='sea level anomalies')
        
        self.sea_level_nan = egads.EgadsData(value=[nan,nan,1.0,2.0,nan,4.0,5.0,6.0,nan,8.0,nan,nan,11.0,12.0,nan,nan],
                                             units='mm',
                                             long_name='sea level anomalies')
        
        self.sea_level_lite = egads.EgadsData(value=[2.0,4.0,5.0,6.0,8.0,11.0],
                                         units='mm',
                                         long_name='sea level anomalies')
        
        self.time = egads.EgadsData(value=[2.0,3.0,5.0,6.0,7.0,9.0,12.0,13.0],
                                    units='s',
                                    long_name='time')
        
        self.time_nan = egads.EgadsData(value=[0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0],
                                    units='s',
                                    long_name='time')
        
        self.time_lite = egads.EgadsData(value=[3.0,5.0,6.0,7.0,9.0,12.0],
                                    units='s',
                                    long_name='time')
        
        self.new_time = egads.EgadsData(value=[2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0],
                                    units='s',
                                    long_name='time')
        
        self.interp_sea_level = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0]
        self.complex_sea_level = [1.0,1.6,3.2,4.8,6.2,7.6,9.7,11.0]
        self.array_test = numpy.zeros(8) + 10
        self.array_test_nan = numpy.zeros(12) + 10
        self.array_test_lite = numpy.zeros(6) + 10
    
    def test_interpolation_linear_simple(self):
        res_interp = transforms.InterpolationLinear().run(self.time, self.sea_level, self.new_time)
        self.assertListEqual(res_interp.value.tolist(), self.interp_sea_level, 'The test vector and interpolated vector dont match')
        res_interp = transforms.InterpolationLinear().run(self.time, self.array_test, self.new_time)
        self.assertEqual(res_interp.shape, self.array_test_nan.shape, 'Sea level array shapes dont match')
        
    def test_interpolation_linear_nan(self):
        res_interp = transforms.InterpolationLinear().run(self.time_nan, self.sea_level_nan, self.new_time)
        self.assertListEqual(res_interp.value.tolist(), self.interp_sea_level, 'The test vector and interpolated vector dont match')
        res_interp = transforms.InterpolationLinear().run(self.time_nan, self.array_test_nan, self.new_time)
        self.assertEqual(res_interp.shape, self.array_test_nan.shape, 'Sea level array shapes dont match')
    
    def test_interpolation_linear_lr(self):
        res_interp = transforms.InterpolationLinear().run(self.time_lite, self.sea_level_lite, self.new_time, 1.0, 12.0)
        self.assertListEqual(res_interp.value.tolist(), self.interp_sea_level, 'The test vector and interpolated vector dont match')
        res_interp = transforms.InterpolationLinear().run(self.time_lite, self.array_test_lite, self.new_time, 10, 10)
        self.assertEqual(res_interp.shape, self.array_test_nan.shape, 'Sea level array shapes dont match')
        
    def test_interpolation_linear_complex(self):
        sea_level = egads.EgadsData(value=[0.5,3.0,4.0,7.0,5.0,2.0,-1.0,4.0,-5.0,1.0,7.0,12.0],
                                units='mm',
                                long_name='sea level anomalies')
        interp_sea_level = [0.5,3.0,4.0,5.5,7.0,5.0,2.0,-1.0,1.5,4.0,-5.0,1.0,7.0,12.0]
        time = egads.EgadsData(value=[1.0,2.0,3.0,5.0,6.0,7.0,8.0,10.0,11.0,12.0,13.0,14.0],
                               units='s',
                               long_name='time')
        new_time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0],
                               units='s',
                               long_name='time')
        res_interp = transforms.InterpolationLinear().run(time, sea_level, new_time)
        self.assertListEqual(res_interp.value.tolist(), interp_sea_level, 'The test vector and interpolated vector dont match')
        
    def test_isotime_to_elements(self):
        y, m, d, h, mm, s = transforms.IsotimeToElements().run(['2017-01-04T13:43:11'])
        self.assertEqual(y, 2017, 'Test year and converted year dont match')
        self.assertEqual(m, 1, 'Test month and converted month dont match')
        self.assertEqual(d, 4, 'Test day and converted day dont match')
        self.assertEqual(h, 13, 'Test hour and converted hour dont match')
        self.assertEqual(mm, 43, 'Test minute and converted minute dont match')
        self.assertEqual(s, 11, 'Test second and converted second dont match')
        
    def test_isotime_to_seconds(self):
        seconds = transforms.IsotimeToSeconds().run(['2017-01-04T13:43:11'])
        self.assertEqual(seconds, 1483537391, 'Test seconds and converted seconds dont match')
        
    def test_seconds_to_isotime(self):
        string = transforms.SecondsToIsotime().run([1483537391], '19700101T000000', 'yyyy-mm-ddTHH:MM:ss')
        self.assertEqual(string, '2017-01-04T13:43:11', 'Test ISO time and converted ISO time dont match')


'''class ComparisonsTestCase(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_compare_param_lcss(self):
        
        data1 = [-1.5172,-0.33272,-0.12522,-0.3104,-0.13724,0.28505,-0.11167,-0.46538,-0.2738,0.13651,0.25486,-0.86224,-0.083357,
                   -0.46314,-0.22711,-1.3034,-0.85209,0.054911,0.30538,-0.6027,-0.52178,-0.78222,-0.2223,0.046834,-0.32184,-0.62855,
                   -1.0539,-0.73235,0.67703,-0.3284,0.071781,-0.68856,-0.075448,0.61032,-0.13596,-0.64326,0.25181,0.8214,0.25438,
                   0.53026,1.3177,0.57967,-0.16434,0.98128,1.4554,1.4296,1.1765,0.7296,1.4243,1.7796,1.2024,1.9604,1.617,1.2329,
                   1.3621,2.6736,1.8309,1.0942,2.2502,2.2233,2.6356,2.1655,2.482,2.87,3.0771,0.0107,-0.78338,0.14068,0.15359,-0.98876,
                   -1.0022,-0.67754,-1.7875,-1.095,-0.71648,0.07308,-0.93186,-1.0799,-0.099759,-0.77861,-0.27506,0.12639,-1.242,0.1089,
                   0.13348,-0.60698,-0.43464,-0.59908,-0.413,-1.1651,-1.0596,0.10793,-0.088707,-0.0094974,-1.6825,-0.91131,-0.30536,
                   -0.53197,-0.26168,-0.16455,-0.77672,0.10404,0.25662,-0.17581,-0.67316,-0.91099,-0.59982,0.084302,-0.10657,-0.57009,
                   -0.11042,-0.68912,-1.2998,-0.91324,-1.1426,-0.44292,-0.62034,-0.12458,0.060589,-0.65982,-0.84775,-1.1151,-0.78318,
                   -0.30291,-0.16949,0.23132,-0.13145,-0.61866]

        data2 = [-0.70281,-1.2401,-1.3004,-1.8328,-0.93417,-0.94227,-0.43864,-1.1694,-1.2902,-1.0329,-0.088765,-0.36676,-0.96574,
                   -1.1283,-1.1112,-1.9358,-1.4638,-0.43026,-0.54867,-0.32914,-1.9888,-0.27097,-1.2067,-0.51132,-0.50017,0.090712,
                   -0.87432,-0.44734,0.19236,-0.024114,-0.45766,-1.3617,0.16255,0.068816,0.1141,-0.22301,-0.064289,-1.0861,-0.53292,
                   -0.78467,0.65523,-0.29036,-0.0082413,-1.3085,0.54746,-0.85729,0.73174,-0.0078086,0.077377,0.43619,0.38731,0.70604,
                   -0.25129,0.64354,0.070845,0.053106,0.9959,0.35918,0.11124,0.78497,0.41933,0.89163,0.41593,0.21421,-0.5698,0.50703,
                   0.97914,0.2075,0.32864,0.7327,1.3112,0.24135,0.73056,0.89427,0.74366,1.0054,-0.19462,1.4015,1.1858,0.60837,1.8864,
                   0.49625,0.92484,0.83994,1.6714,1.1941,1.4736,1.3218,1.0127,0.89724,1.3582,2.0839,1.6153,1.5368,2.065,1.1122,2.2286,
                   1.5779,1.7803,1.9165,2.0079,1.8882,-0.34513,-0.46982,-0.73287,-1.0143,-1.107,-0.47688,-1.0202,-0.74534,-0.39751,
                   -0.66843,-0.40262,-0.32728,-1.4322,-0.96598,-0.32218,-1.2928,-1.2376,-0.98361,-1.6413,0.13562,-1.1402,-1.0966,-0.4398,
                   -0.95645,-0.70907,-0.032284]
        

        vector1 = egads.EgadsData(value=data1,
                               units='mm',
                               long_name='test1')
        
        vector2 = egads.EgadsData(value=data2,
                               units='mm',
                               long_name='test2')
        
        res = comparisons.CompareParamLcss().run(vector1, vector2, 20)'''
        

def suite():
    egads_corr_suite = unittest.TestLoader().loadTestsFromTestCase(CorrectionsTestCase)
    egads_math_suite = unittest.TestLoader().loadTestsFromTestCase(MathematicsTestCase)
    egads_transform_suite = unittest.TestLoader().loadTestsFromTestCase(TransformsTestCase)
    #egads_comparisons_suite = unittest.TestLoader().loadTestsFromTestCase(ComparisonsTestCase)
    return unittest.TestSuite([egads_corr_suite, egads_math_suite, egads_transform_suite])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

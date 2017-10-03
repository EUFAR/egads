"""
Test suite to verify complete functioning of EgadsAlgorithm class and associated metadata.
Creates a dummy algorithm following the EGADS algorithm template, and tests for functionality.
"""

__author__ = "mfreer, henry"
__date__ = "2016-12-6 11:35"
__version__ = "1.2"

import unittest
import egads
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

IN1 = 100.0
IN2 = 5.0
OUT1 = 0.001
OUT2 = 0.72
IN_UNITS1 = 'cm'
IN_UNITS2 = 's'
OUT_UNITS1 = 'km'
OUT_UNITS2 = 'km/h'
LONG_NAME1 = 'distance'
LONG_NAME2 = 'speed'
DATE = __date__.replace('$', '').replace('#', '').replace('Date::', '').strip()
VERSION = __version__.replace('$', '').replace('Revision::', '').strip()


class AlgorithmModuleTestCase(unittest.TestCase):
    """ Test features of algorithm module"""

    def setUp(self):
        self.single_alg = TestAlgorithmSingleIO()
        self.single_alg_no_egads = TestAlgorithmSingleIO(return_Egads=False)
        self.double_alg = TestAlgorithmDualIO()
        self.single_passunits_alg = TestAlgorithmSingleIOPassUnits()
        self.single_set_units_alg = TestAlgorithmSingleIOSetUnits()
        self.dual_set_units_alg = TestAlgorithmDualIOSetUnits()

    def test_alg_single_input_output(self):
        """ Test sample algorithm with single input and output"""
        
        out1 = self.single_alg.run(IN1)
        self.assertEqual(out1, OUT1, "Single algorithm value not equal")
        self.assertEqual(out1.units, OUT_UNITS1, "Single algorithm output units not equal")
        self.assertEqual(out1.metadata.parent['Processor'], "TestAlgorithmSingleIO", "Single algorithm processor name does not match")
        self.assertEqual(out1.metadata.parent['ProcessorDate'], DATE, "Single algorithm processed date does not match")
        self.assertEqual(out1.metadata.parent['ProcessorVersion'], VERSION, "Single algorithm processor version does not match")

    def test_alg_double_input_output(self):
        """ Test sample algorithm with multiple inputs and outputs."""
        
        [out1, out2] = self.double_alg.run(IN1, IN2)
        self.assertEqual(out1, OUT1, "Double algorithm value not equal")
        self.assertEqual(out1.units, OUT_UNITS1, "Double algorithm output units not equal")
        self.assertEqual(out1.metadata.parent['Processor'], "TestAlgorithmDualIO", "Double algorithm processor name does not match")
        self.assertEqual(out1.metadata.parent['ProcessorDate'], DATE, "Double algorithm processed date does not match")
        self.assertEqual(out1.metadata.parent['ProcessorVersion'], VERSION, "Double algorithm processor version does not match")
        self.assertEqual(out2, OUT2, "Double algorithm value not equal")
        self.assertEqual(out2.units, OUT_UNITS2, "Double algorithm output units not equal")
        self.assertEqual(out2.metadata.parent['Processor'], "TestAlgorithmDualIO", "Double algorithm processor name does not match")
        self.assertEqual(out2.metadata.parent['ProcessorDate'], DATE, "Double algorithm processed date does not match")
        self.assertEqual(out2.metadata.parent['ProcessorVersion'], VERSION, "Double algorithm processor version does not match")

    def test_alg_single_no_egads(self):
        """ Test sample algorithm with single input and single non-egads output"""
        
        out1 = self.single_alg_no_egads.run(IN1)
        self.assertEqual(out1, OUT1, "Single algorithm no egads value not equal")
        self.assert_(not isinstance(out1, egads.EgadsData), "Returned value is EgadsData instance")

    def test_call_alg_directly(self):
        """ Test sample algorithm bypassing run call"""
        
        self.assert_(self.single_alg._algorithm(IN1) == OUT1, "Direct call to single algorithm failed")
        [out1, out2] = self.double_alg._algorithm(IN1, IN2)
        self.assertEqual(out1, OUT1, "Direct call to double algorithm first parameter not equal")
        self.assertAlmostEqual(out2, OUT2, 2, "Direct call to double algorithm second paramater not equal")

    def test_alg_pass_units(self):
        """ Test sample algorithm passing input units"""
        
        out1 = self.single_passunits_alg.run(IN1)
        self.assertEqual(out1, OUT1, "Single algorithm passing units value not equal")
        self.assertEqual(out1.units, 'dimensionless', "Single algorithm passing units output units not equal")

    def test_alg_pass_other_units(self):
        """ Test sample algorithm auto-conversion"""

        in_egads = egads.EgadsData(IN1 * 10, 'mm')
        out1 = self.single_alg.run(in_egads)
        self.assertEqual(out1, OUT1, "Single algorithm auto-conversion value not equal")
        self.assertEqual(out1.units, OUT_UNITS1, "Single algorithm auto-conversion output units not equal")
        self.assertEqual(out1.metadata.parent['Processor'], "TestAlgorithmSingleIO", "Single algorithm auto-conversion processor name does not match")
        self.assertEqual(out1.metadata.parent['ProcessorDate'], DATE, "Single algorithm auto-conversion processed date does not match")
        self.assertEqual(out1.metadata.parent['ProcessorVersion'], VERSION, "Single algorithm processor auto-conversion version does not match")

    def test_alg_set_other_units(self):
        """ Test sample algorithm modifying passed input units """

        in_egads = egads.EgadsData(IN1, IN_UNITS1, {'long_name':LONG_NAME1})
        out1 = self.single_set_units_alg.run(in_egads)
        self.assertEqual(out1, OUT1, "Single algorithm setting units value not equal")
        self.assertEqual(out1.units, IN_UNITS1 + '/s', "Single algorithm setting units output units not equal, returned {0}".format(out1.units))
        self.assertEqual(out1.metadata['long_name'], 'first derivative of ' + LONG_NAME1, 'Single algorithm setting units output long name not equal, returned {0}'.format(out1.metadata['long_name']))
    
    def test_alg_set_dual_other_units(self):
        """ Test sample algorithm modifying dual passed input units"""

        in_egads1 = egads.EgadsData(IN1, IN_UNITS1, {'long_name':LONG_NAME1})
        in_egads2 = egads.EgadsData(IN2, IN_UNITS2, {'long_name':LONG_NAME2})
        out1 = self.dual_set_units_alg.run(in_egads2, in_egads1)
        self.assertEqual(out1.units, IN_UNITS1 + '/' + IN_UNITS2, "Dual algorithm setting units output units not equal, expected {0}, received {1}".format(IN_UNITS1 + '/' + IN_UNITS2, out1.units))


class TestAlgorithmSingleIO(egads_core.EgadsAlgorithm):

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':OUT_UNITS1,
                                                               'long_name':LONG_NAME1,
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[LONG_NAME1],
                                                          'InputUnits':[IN_UNITS1],
                                                          'Outputs':[LONG_NAME1],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x):
        return egads_core.EgadsAlgorithm.run(self, x)

    def _algorithm(self, x):
        result = x * 1e-5
        return result


class TestAlgorithmDualIO(egads_core.EgadsAlgorithm):

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = []
        self.output_metadata.append(egads_metadata.VariableMetadata({'units':OUT_UNITS1,
                                                               'long_name':LONG_NAME1,
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.output_metadata.append(egads_metadata.VariableMetadata({'units':OUT_UNITS2,
                                                               'long_name':LONG_NAME2,
                                                               'standard_name':'',
                                                               'Category':['']}))

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[LONG_NAME1, LONG_NAME2],
                                                          'InputUnits':[IN_UNITS1, IN_UNITS2],
                                                          'Outputs':[LONG_NAME1, LONG_NAME2],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x, t):
        return egads_core.EgadsAlgorithm.run(self, x, t)

    def _algorithm(self, x, t):
        result1 = x * 1e-5
        result2 = result1 / (t / (60 * 60))
        return result1, result2


class TestAlgorithmSingleIOPassUnits(egads_core.EgadsAlgorithm):

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0',
                                                               'long_name':LONG_NAME1,
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[LONG_NAME1],
                                                          'InputUnits':[None],
                                                          'Outputs':[LONG_NAME1],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x):
        return egads_core.EgadsAlgorithm.run(self, x)

    def _algorithm(self, x):
        result = x * 1e-5
        return result


class TestAlgorithmSingleIOSetUnits(egads_core.EgadsAlgorithm):

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0/sec',
                                                               'long_name':'first derivative of input0',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[LONG_NAME1],
                                                          'InputUnits':[None],
                                                          'Outputs':[LONG_NAME1],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x):
        return egads_core.EgadsAlgorithm.run(self, x)

    def _algorithm(self, x):
        result = x * 1e-5
        return result


class TestAlgorithmDualIOSetUnits(egads_core.EgadsAlgorithm):

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input1/input0',
                                                               'long_name':'first derivative of input0',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':[LONG_NAME2, LONG_NAME1],
                                                          'InputUnits':[IN_UNITS2, None],
                                                          'Outputs':[LONG_NAME1],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)
        
    

    def run(self, t, x):
        return egads_core.EgadsAlgorithm.run(self, t, x)

    def _algorithm(self, t, x):
        result = x / t
        return result
    

def suite():
    algorithm_module_test_suite = unittest.TestLoader().loadTestsFromTestCase(AlgorithmModuleTestCase)
    return unittest.TestSuite([algorithm_module_test_suite])


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=5).run(suite())

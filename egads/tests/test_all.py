# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest

import input_tests
import thermodynamics_tests
import egads_tests
import algorithm_module_tests

def test():
    suite = unittest.TestSuite()
    suite.addTest(input_tests.suite())
    suite.addTest(egads_tests.suite())
    suite.addTest(thermodynamics_tests.suite())
    suite.addTest(algorithm_module_tests.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)

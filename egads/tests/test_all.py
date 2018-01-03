"""
Initiate all functions to test EGADS functionality.
"""

import unittest, logging
import input_tests
import thermodynamics_tests
import corrections_mathematics_transforms_tests
import egads_tests
import algorithm_module_tests
import metadata_tests
import microphysics_tests
import radiation_tests

def test():
    logging.info('egads - test_all.py - test - egads tests are starting ...')
    suite = unittest.TestSuite()
    suite.addTest(egads_tests.suite())
    suite.addTest(metadata_tests.suite())
    suite.addTest(input_tests.suite())
    suite.addTest(algorithm_module_tests.suite())
    suite.addTest(thermodynamics_tests.suite())
    suite.addTest(corrections_mathematics_transforms_tests.suite())
    suite.addTest(microphysics_tests.suite())
    suite.addTest(radiation_tests.suite())
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    logging.info('egads - test_all.py - test - egads tests are finished.')
    logging.debug('egads - test_all.py - test - tests run ' + str(result.testsRun))
    if result.errors:
        logging.debug('egads - test_all.py - test - errors ' + str(len(result.errors)))
        for i in result.errors:
            logging.debug('...........................' + str(i))
    else:
        logging.debug('egads - test_all.py - test - no error')
    if result.failures:
        logging.debug('egads - test_all.py - test - failures ' + str(len(result.failures)))
        for i in result.failures:
            logging.debug('.............................' + str(i[0]) + ' -> ' + str(i[-1]))
    else:
        logging.debug('egads - test_all.py - test - no failure')

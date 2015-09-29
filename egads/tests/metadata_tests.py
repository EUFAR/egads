"""
Test suite for Metadata classes.

"""
from test import test_gl, test_al
__author__ = "mfreer"
__date__ = "$Date:: 2012-02-17 18:01#$"
__version__ = "$Revision:: 129       $"


import unittest
import egads.core.metadata as metadata

TEST_GLOBAL_METADATA_DICT = {'Conventions':'N6SP',
                             'title':'test',
                             'source':'testfile',
                             'institution':'EUFAR',
                             'project':'N6SP',
                             'date_created':'20110920',
                             'geospatial_lat_min':0,
                             'geospatial_lat_max':90,
                             'geospatial_lon_min':0,
                             'geospatial_lon_max':90,
                             'geospatial_vertical_min':0,
                             'geospatial_vertical_max':1000,
                             'time_coverage_start':0,
                             'time_coverage_end':1,
                             'history':'for the test file',
                             'references':'none',
                             'comment':'this is a test'}

TEST_VARIABLE_METADATA_DICT = {'units':'m',
                               '_FillValue':-9999,
                               'long_name':'test variable metadata dict',
                               'valid_min':0,
                               'valid_max':1,
                               'SampledRate':10,
                               'Category':'Other'}

TEST_ALGORITHM_METADATA_DICT = {'Inputs':['test'],
                                'InputUnits':['m'],
                                'Outputs':['test_out'],
                                'Processor':'test processor',
                                'ProcessorDate':'20110919',
                                'ProcessorVersion':'1.0',
                                'DateProcessed':'20110920'}


class MetadataCreationTestCase(unittest.TestCase):
    """ Test creation of metadata instances """

    def setUp(self):
        pass

    def test_creation_of_metadata_object(self):
        """ Test creation of metadata instance via direct dictionary assignment """
        file_metadata = metadata.FileMetadata(TEST_GLOBAL_METADATA_DICT)
        alg_metadata = metadata.AlgorithmMetadata(TEST_ALGORITHM_METADATA_DICT)
        variable_metadata = metadata.VariableMetadata(TEST_VARIABLE_METADATA_DICT)

        self.assertEqual(file_metadata, TEST_GLOBAL_METADATA_DICT, 'Global metadata not properly assigned to file metadata instance')
        self.assertEqual(alg_metadata, TEST_ALGORITHM_METADATA_DICT, 'Algorithm metadata not properly assigned to algorithm metadata instance')
        self.assertEqual(variable_metadata, TEST_VARIABLE_METADATA_DICT, 'Variable metadata not properly assigned to variable metadata instance')

        self.assertEqual(file_metadata._conventions, TEST_GLOBAL_METADATA_DICT['Conventions'], 'Global metadata conventions object doesnt match')
        self.assertEqual(alg_metadata._conventions, 'EGADS Algorithm', 'Algorithm conventions abject doesnt match')


    def test_add_items(self):
        """ Test creation of metadata, assigning metadat using add_items method"""
        file_metadata = metadata.FileMetadata()
        alg_metadata = metadata.AlgorithmMetadata()
        variable_metadata = metadata.VariableMetadata()

        file_metadata.add_items(TEST_GLOBAL_METADATA_DICT)
        alg_metadata.add_items(TEST_ALGORITHM_METADATA_DICT)
        variable_metadata.add_items(TEST_VARIABLE_METADATA_DICT)

        self.assertEqual(file_metadata, TEST_GLOBAL_METADATA_DICT, 'Global metadata not properly assigned to file metadata instance')
        self.assertEqual(alg_metadata, TEST_ALGORITHM_METADATA_DICT, 'Algorithm metadata not properly assigned to algorithm metadata instance')
        self.assertEqual(variable_metadata, TEST_VARIABLE_METADATA_DICT, 'Variable metadata not properly assigned to variable metadata instance')

        def test_set_conventions(self):
            pass


class MetadataConventionComplianceTestCase(unittest.TestCase):
    """ Test compliance checker functionality in metadata cases. """

    def setUp(self):
        cf_var_metadata_dict = {'_FillValue':'',
                                'valid_min':'',
                                'valid_max':'',
                                'valid_range':'',
                                'scale_factor':'',
                                'add_offset':'',
                                'units':'',
                                'long_name':'',
                                'standard_name':'',
                                'ancillary_variables':'',
                                'flag_values':'',
                                'flag_masks':'',
                                'flag_meanings':''
                                }
        raf_var_metadata_dict = {'_FillValue':'',
                                'units':'',
                                'long_name':'',
                                'standard_name':'',
                                'SampledRate':'',
                                'CalibrationCoefficients':'',
                                'Category':'',
                                'Dependencies':''
                                }
        iwgadts_var_metadata_dict = {'':'',
                                     '':'',
                                     '':'',
                                     '':'',
                                     '':'',
                                     '':'',
                                     '':''
                                     }
        n6sp_var_metadata_dict = {'':'',
                                  '':'',
                                  '':'',
                                  '':'',
                                  '':'',
                                  '':'',
                                  '':'',
                                  }
        nasa_ames_var_metadata_dict = {'':'',
                                       '':'',
                                       '':'',
                                       '':'',
                                       '':'',
                                       }

        var_metadata = metadata.VariableMetadata();

    def test_provide_convention_compliance_string(self):
        #TODO: Complete test class 
        pass

    def test_provide_convention_compliance_list(self):
        #TODO: Complete test class 
        pass

    def test_provide_convention_compliance_none(self):
        #TODO: Complete test class 
        pass

    def test_provide_nonexisting_convention_compliance(self):
        #TODO: Complete test class 
        pass

    def test_metadata_with_no_conventions(self):
        #TODO: Complete test class 
        pass

    def test_variable_metadata(self):
        #TODO: Complete test class 
        pass

    def test_file_metadata(self):
        #TODO: Complete test class 
        pass

    def test_complete_metadata(self):
        #TODO: Complete test class 
        pass

    def test_incomplete_metadata(self):
        #TODO: Complete test class 
        pass



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

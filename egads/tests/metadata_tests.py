"""
Test suite for Metadata classes.
"""

__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 11:45"
__version__ = "1.2"

import unittest
import egads.core.metadata as metadata

TEST_GLOBAL_METADATA_DICT = {'Conventions':'EUFAR',
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

TEST_GLOBAL_METADATA_LITE_DICT = {'Conventions':'EUFAR',
                             'title':'test',
                             'source':'testfile',
                             'institution':'EUFAR',
                             'project':'N6SP',
                             'date_created':'20110920',
                             'geospatial_vertical_min':0,
                             'geospatial_vertical_max':1000,
                             'time_coverage_start':0,
                             'time_coverage_end':1,
                             'history':'for the test file',
                             'references':'none',
                             'comment':'this is a test'}

ADD_GLOBAL_METADATA_DICT = {'geospatial_lat_min':0,
                             'geospatial_lat_max':90,
                             'geospatial_lon_min':0,
                             'geospatial_lon_max':90}

TEST_VARIABLE_METADATA_DICT = {'units':'m',
                               '_FillValue':-9999,
                               'long_name':'test variable metadata dict',
                               'valid_min':0,
                               'valid_max':1,
                               'SampledRate':10,
                               'Category':'Other'}

TEST_VARIABLE_METADATA_LITE_DICT = {'units':'m',
                               '_FillValue':-9999,
                               'long_name':'test variable metadata dict',
                               'SampledRate':10,
                               'Category':'Other'}

ADD_VARIABLE_METADATA_DICT = {'valid_min':0,
                               'valid_max':1}

TEST_ALGORITHM_METADATA_DICT = {'Inputs':['test'],
                                'InputUnits':['m'],
                                'InputTypes':['vector'],
                                'InputDescription':['Test'],
                                'Outputs':['test_out'],
                                'OutputDescription':['Test out'],
                                'Purpose':'Test',
                                'Description':'Test',
                                'Processor':'test processor',
                                'ProcessorDate':'20110919',
                                'ProcessorVersion':'1.0',
                                'DateProcessed':'20110920'}

TEST_ALGORITHM_METADATA_LITE_DICT = {'Inputs':['test'],
                                'InputUnits':['m'],
                                'InputTypes':['vector'],
                                'InputDescription':['Test'],
                                'Outputs':['test_out'],
                                'OutputDescription':['Test out'],
                                'Purpose':'Test',
                                'Description':'Test',
                                'Processor':'test processor',
                                'DateProcessed':'20110920'}

ADD_ALGORITHM_METADATA_DICT = {'ProcessorDate':'20110919',
                                'ProcessorVersion':'1.0'}


class MetadataCreationTestCase(unittest.TestCase):
    """ Test creation of metadata instances """

    def setUp(self):
        pass

    def test_creation_of_metadata_object(self):
        """ Test creation of metadata instance via direct dictionary assignment """
        
        file_metadata = metadata.FileMetadata(TEST_GLOBAL_METADATA_DICT, filename=None)
        alg_metadata = metadata.AlgorithmMetadata(TEST_ALGORITHM_METADATA_DICT)
        variable_metadata = metadata.VariableMetadata(TEST_VARIABLE_METADATA_DICT)
        self.assertEqual(file_metadata, TEST_GLOBAL_METADATA_DICT, 'Global metadata not properly assigned to file metadata instance')
        self.assertEqual(alg_metadata, TEST_ALGORITHM_METADATA_DICT, 'Algorithm metadata not properly assigned to algorithm metadata instance')
        self.assertEqual(variable_metadata, TEST_VARIABLE_METADATA_DICT, 'Variable metadata not properly assigned to variable metadata instance')
        self.assertEqual(file_metadata._conventions[0], TEST_GLOBAL_METADATA_DICT['Conventions'], 'Global metadata conventions object doesnt match')
        self.assertEqual(alg_metadata._conventions, 'EGADS Algorithm', 'Algorithm conventions abject doesnt match')

    def test_add_items(self):
        """ Test creation of metadata, assigning metadat using add_items method"""
        
        file_metadata = metadata.FileMetadata(TEST_GLOBAL_METADATA_LITE_DICT, filename=None)
        alg_metadata = metadata.AlgorithmMetadata(TEST_ALGORITHM_METADATA_LITE_DICT)
        variable_metadata = metadata.VariableMetadata(TEST_VARIABLE_METADATA_LITE_DICT)
        file_metadata.add_items(ADD_GLOBAL_METADATA_DICT)
        alg_metadata.add_items(ADD_ALGORITHM_METADATA_DICT)
        variable_metadata.add_items(ADD_VARIABLE_METADATA_DICT)
        self.assertEqual(file_metadata, TEST_GLOBAL_METADATA_DICT, 'Global metadata not properly assigned to file metadata instance')
        self.assertEqual(alg_metadata, TEST_ALGORITHM_METADATA_DICT, 'Algorithm metadata not properly assigned to algorithm metadata instance')
        self.assertEqual(variable_metadata, TEST_VARIABLE_METADATA_DICT, 'Variable metadata not properly assigned to variable metadata instance')


def suite():
    metadata_creation_test_suite = unittest.TestLoader().loadTestsFromTestCase(MetadataCreationTestCase)
    return unittest.TestSuite([metadata_creation_test_suite])


if __name__ == "__main__":
    unittest.main()

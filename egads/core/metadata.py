__author__ = "mfreer, ohenry"
__date__ = "2017-01-11 16:05"
__version__ = "1.3"
__all__ = ['Metadata', 'FileMetadata', 'VariableMetadata', 'AlgorithmMetadata']

import logging

FILE_ATTR_LIST = ['Conventions',
                  'title',
                  'source',
                  'institution',
                  'project',
                  'date_created',
                  'geospatial_lat_min',
                  'geospatial_lat_max',
                  'geospatial_lon_min',
                  'geospatial_lon_max',
                  'geospatial_vertical_min',
                  'geospatial_vertical_max',
                  'geospatial_vertical_positive',
                  'geospatial_vertical_units',
                  'time_coverage_start',
                  'time_coverage_end',
                  'time_coverage_duration',
                  'history',
                  'references',
                  'comment']

VAR_ATTR_LIST = ['units',
                 '_FillValue',
                 'long_name',
                 'standard_name',
                 'valid_range',
                 'valid_min',
                 'valid_max',
                 'SampledRate',
                 'Category',
                 'CalibrationCoefficients',
                 'InstrumentLocation',
                 'instrumentCoordinates',
                 'Dependencies',
                 'Processor',
                 'Comments',
                 'ancillary_variables',
                 'flag_values',
                 'flag_masks',
                 'flag_meanings']

ALG_ATTR_LIST = ['Inputs',
                 'InputUnits',
                 'Outputs',
                 'Processor',
                 'ProcessorDate',
                 'ProcessorVersion',
                 'DateProcessed']

# Table of metadata elements used to convert between vocabularies.
# List is [CF, RAF, IWGADTS, EUFAR, NASA AMES]
METADATA_GLOBAL_CONVERT_TABLE = [['title', '', 'title', 'title', ''],
                                 ['references', '', '', 'references', ''],
                                 ['', 'Address', '', '', ''],
                                 ['', 'Phone', '', '', ''],
                                 ['', 'Categories', '', '', ''],
                                 ['', 'geospatial_lat_min', '', 'geospatial_lat_min', ''],
                                 ['', 'geospatial_lat_max', '', 'geospatial_lat_max', ''],
                                 ['', 'geospatial_lon_min', '', 'geospatial_lon_min', ''],
                                 ['', 'geospatial_lon_max', '', 'geospatial_lon_max', ''],
                                 ['', 'geospatial_vertical_min', '', 'geospatial_vertical_min', ''],
                                 ['', 'geospatial_vertical_max', '', 'geospatial_vertical_max', ''],
                                 ['', 'time_coverage_start', '', 'time_coverage_start', ''],
                                 ['', 'time_coverage_end', '', 'time_coverage_end', ''],
                                 ['', 'TimeInterval', '', 'time_duration', ''],
                                 ['', 'DateProcessed', '', '', 'RDATE'],
                                 ['', 'date_created', '', 'date_created', 'DATE'],
                                 ['', 'FlightDate', '', '', ''],
                                 ['history', 'DataQuality', 'data_quality', 'history', ''],
                                 ['institution', 'institution', 'institution', 'institution', ''],
                                 ['source', '', 'source', 'source', 'ONAME'],
                                 ['', 'creator_url', '', '', ''],
                                 ['', 'ConventionsURL', '', '', ''],
                                 ['', 'ConventionsVersion', '', '', ''],
                                 ['', 'Metadata_Conventions', '', '', ''],
                                 ['', 'Standard_name_vocabulary', '', '', ''],
                                 ['comment', '', '', 'comment', 'COMMENTS'],
                                 ['', 'ProcessorRevision', '', '', ''],
                                 ['', 'ProcessorURL', '', '', ''],
                                 ['', 'ProjectName', '', '', 'MNAME'],
                                 ['', 'Platform', '', '', ''],
                                 ['', 'ProjectNumber', 'project', 'project', ''],
                                 ['', 'FlightNumber', '', '', ''],
                                 ['', 'InterpolationMethod', '', '', ''],
                                 ['', 'latitude_coordinate', '', '', ''],
                                 ['', 'longitude_coodrinate', '', '', ''],
                                 ['', 'zaxis_coordinate', '', '', ''],
                                 ['', 'time_coordinate', '', '', ''],
                                 ['', 'wind_field', '', '', ''],
                                 ['', 'landmarks', '', '', ''],
                                 ['', 'geospatial_vertical_positive', '', '', ''],
                                 ['', 'geopsatial_vertical_units', '', '', '']]

# Table of metadata elements used to convert between vocabularies on a per-variable basis.
# List is [CF, RAF, IWGADTS, EUFAR, NASA AMES]
METADATA_VARIABLE_CONVERT_TABLE = [['_FillValue', '_FillValue', 'missing_value', '_FillValue', 'AMISS'],
                                   ['valid_min', '', '', 'valid_min', ''],
                                   ['valid_max', '', '', 'valid_max', ''],
                                   ['valid_range', '', 'valid_range', 'valid_range', ''],
                                   ['scale_factor', '', '', '', 'ASCAL'],
                                   ['add_offset', '', '', '', ''],
                                   ['units', 'units', 'units', 'units', ''],
                                   ['long_name', 'long_name', 'long_name', 'long_name', 'ANAME'],
                                   ['standard_name', 'standard_name', 'standard_name', 'standard_name', ''],
                                   ['ancillary_variables', '', '', 'ancillary_variables', ''],
                                   ['flag_values', '', '', 'flag_values', ''],
                                   ['flag_masks', '', '', 'flag_masks', ''],
                                   ['flag_meanings', '', '', 'flag_meanings', ''],
                                   ['', 'SampledRate', '', 'SampledRate', ''],
                                   ['', 'CalibrationCoefficients', '', 'CalibrationCoefficients', ''],
                                   ['', 'Category', '', 'Category', ''],
                                   ['', '', '', 'InstrumentCoordinates', ''],
                                   ['', '', '', 'InstrumentLocation', ''],
                                   ['', 'Dependencies', '', 'Dependencies', ''],
                                   ['', '', '', 'Processor', ''],
                                   ['', '', '', 'Comments', ''],
                                   ['', '', 'source', '', 'SNAME']]

CF_TABLE_COLUMN = 0
RAF_TABLE_COLUMN = 1
IWGADTS_TABLE_COLUMN = 2
EUFAR_TABLE_COLUMN = 3
NASA_AMES_TABLE_COLUMN = 4


class Metadata(dict):
    """
    This is a generic class designed to provide basic metadata storage and handling
    capabilities.
    """

    def __init__(self, metadata_dict={}, conventions=None, metadata_list=None):
        """
        Initialize Metadata instance with given metadata in dict form.

        :param dict metadata_dict:
            Dictionary object containing metadata names and values.
        """

        logging.debug('egads - metadata.py - Metadata - __init__ - dict ' + str(metadata_dict) + ', conventions ' + str(conventions))
        dict.__init__(self, metadata_dict)
        self._metadata_list = metadata_list
        self._conventions = conventions

    def add_items(self, metadata_dict):
        """
        Method to add metadata items to current Metadata instance.

        :param metadata_dict:
            Dictionary object containing metadata names and values.
        """
        
        logging.debug('egads - metadata.py - Metadata - add_items - dict ' + str(metadata_dict))
        for key, var in metadata_dict.iteritems():
            self[key] = var
        return

    def set_conventions(self, conventions):
        """
        Sets conventions to be used in current Metadata instance

        :param list conventions:
            List of conventions used in current metadata instance.
        """
        
        logging.debug('egads - metadata.py - Metadata - set_conventions - conventions ' + str(conventions))
        self._conventions = conventions

    def parse_dictionary_objs(self):
        pass

    def compliance_check(self, conventions=None):
        """
        Checks for compliance with metadata conventions. If no specific 
        conventions are provided, then compliance check will be based on 
        metadata conventions listed in Conventions metadata field.
        
        :param string|list conventions:
            Optional - Comma separated string or list of coventions to use for 
            conventions check. Current conventions recognized are ``CF``, 
            ``RAF``, ``IWGADTS``, ``EUFAR``, ``NASA Ames``
        """

        logging.debug('egads - metadata.py - Metadata - compliance_check - conventions ' + str(conventions))
        if conventions is None:
            if self.has_key('Conventions'):
                conventions = self['Conventions']
            else:
                logging.error('egads - metadata.py - Metadata - compliance_check - AttributeError, no convention found')
                raise AttributeError('No convention found. Please specify a convention.')
        if isinstance(conventions, str):
            conventions = conventions.split(',')
        convention_num = None
        for convention in conventions:
            if 'CF' in convention:
                convention_num = CF_TABLE_COLUMN
            elif 'RAF' in convention:
                convention_num = RAF_TABLE_COLUMN
            elif 'IWGADTS' in convention:
                convention_num = IWGADTS_TABLE_COLUMN
            elif 'EUFAR' in convention:
                convention_num = EUFAR_TABLE_COLUMN
            elif 'NASA' in convention:
                convention_num = NASA_AMES_TABLE_COLUMN
            else:
                logging.error('egads - metadata.py - Metadata - compliance_check - AttributeError, unknown convention')
                raise AttributeError('Unknown convention. Please specify a convention from the EUFAR list.')
            param_missing_list = self._parse_metadata_compliance(convention_num)
            return param_missing_list
        
    def _parse_metadata_compliance(self, convention_num):
        """ 
        Private method to parse through a metadata parameter list to determine
        compliance with standard.
        
        :param int convention_num:
            Number specifying which convention standard to use in comparison.
        """
        
        logging.debug('egads - metadata.py - Metadata - _parse_metadata_compliance - convention_num ' + str(convention_num))
        use_table = None
        if isinstance(self, FileMetadata):
            use_table = METADATA_GLOBAL_CONVERT_TABLE
        if isinstance(self, VariableMetadata):
            use_table = METADATA_VARIABLE_CONVERT_TABLE
        if use_table is None:
            logging.error('egads - metadata.py - Metadata - _parse_metadata_compliance - AttributeError, metadata couldn''t be parsed')
            raise AttributeError('A problem occured: the metadata couldn''t be parsed')
        param_missing_list = []
        for parameter in use_table:
            if parameter[convention_num] not in self and parameter[convention_num] is not '':
                param_missing_list.append(parameter[convention_num])
        return param_missing_list
    
    logging.info('egads - metadata.py - Metadata has been loaded')


class FileMetadata(Metadata):
    """
    This class is designed to provide basic storage and handling capabilities
    for file metadata.
    """

    def __init__(self, metadata_dict, filename, conventions_keyword='Conventions', conventions=[]):
        """
        Initialize Metadata instance with given metadata in dict form. Tries to
        determine which conventions are used by the metadata. The user can optionally
        supply which conventions the metadata uses.

        :param dict metadata_dict:
            Dictionary object containing metadata names and values.
        :param string filename:
            Filename for origin of file metadata.
        :param string conventions_keyword: Optional -
            Keyword contained in metadata dictionary used to detect which metadata
            conventions are used.
        :param list conventions: Optional -
            List of metadata conventions used in provided metadata dictionary.
        """
        
        logging.debug('egads - metadata.py - FileMetadata - __init__ - dict ' + str(metadata_dict) + 
                      ', filename ' + str(filename) + 'conventions_keyword ' + 
                      str(conventions_keyword) + ', conventions ' + str(conventions))
        if not conventions:
            try:
                conventions = [s.strip() for s in metadata_dict[conventions_keyword].split(',')]
            except KeyError:
                conventions = []
        Metadata.__init__(self, metadata_dict, conventions, metadata_list=FILE_ATTR_LIST)
        if filename is None:
            self._filename = None
        else:
            self._filename = filename
        self.update()

    def set_filename(self, filename):
        """
        Sets file object used for current FileMetadata instance.

        :param string filename:
            Filename of provided metadata.
        """
        
        logging.debug('egads - metadata.py - FileMetadata - set_filename - filename ' + str(filename))
        self._filename = filename

    def parse_dictionary_objs(self):
        pass

    logging.info('egads - metadata.py - FileMetadata has been loaded')


class VariableMetadata(Metadata):
    """
    This class is designed to provide storage and handling capabilities for
    variable metadata.
    """

    def __init__(self, metadata_dict, parent_metadata_obj=None, conventions=None):
        """
        Initialize VariableMetadata instance with given metadata in dict form.
        If VariableMetadata comes from a file, the file metadata object can be
        provided to auto-detect conventions. Otherwise, the user can specify which
        conventions are used in the variable metadata.

        :param dict metadata_dict:
            Dictionary object contaning variable metadata names and values
        :param Metadata parent_metadata_obj: Metadata, optional
            Metadata object for the parent object of current variable (file,
            algorithm, etc). This field is optional.
        :param list conventions: Optional -
            List of metadata conventions used in provided metadata dictionary.
        """

        logging.debug('egads - metadata.py - VariableMetadata - __init__ - dict ' + str(metadata_dict) + 
                      ', parent_metadata_obj ' + str(parent_metadata_obj) + ', conventions ' + 
                      str(conventions))
        Metadata.__init__(self, metadata_dict, metadata_list=VAR_ATTR_LIST)
        if conventions is None:
            if parent_metadata_obj is None:
                self._conventions = None
                self.parent = None
            else:
                self._conventions = parent_metadata_obj._conventions
                self.parent = parent_metadata_obj
        else:
            self._conventions = conventions

    def set_parent(self, parent_metadata_obj):
        """
        Sets parent object of VariableMetadata instance.

        :param Metadata parent_metadata_obj: Optional -
            Metadata object for the parent object of the current variable (file,
            algorithm, etc)
        """

        logging.debug('egads - metadata.py - VariableMetadata - set_parent - parent_metadata_obj ' + str(parent_metadata_obj))
        self.parent = parent_metadata_obj

    def compliance_check(self, conventions=None):
        if conventions is None:
            conventions = self.parent.get("Conventions", None)
        return super(VariableMetadata, self).compliance_check(conventions)

    def parse_dictionary_objs(self):
        pass

    logging.info('egads - metadata.py - VariableMetadata has been loaded')


class AlgorithmMetadata(Metadata):
    """
    This class is designed to provide storage and handling capabilities for 
    EGADS algorithm metadata. Stores instances of VariableMetadata objects
    to use to populate algorithm variable outputs.
    """

    def __init__(self, metadata_dict, child_variable_metadata=None):
        """
        Initialize AlgorithmMetadata instance with given metadata in dict form and
        any child variable metadata.

        :param dict metadata_dict:
            Dictionary object containing variable metadata names and values
        :param list child_varable_metadata: Optional -
            List containing VariableMetadata
        """
        
        logging.debug('egads - metadata.py - AlgorithmMetadata - __init__ - metadata_dict ' + str(metadata_dict) + 
                      ', child_variable_metadata' + str(child_variable_metadata))
        if 'ProcessorDate' in metadata_dict:
            replace_dic = {'$':'', '#':'', 'Date::':''}
            processor_date_value = metadata_dict['ProcessorDate']
            for i, j in replace_dic.iteritems():
                processor_date_value = processor_date_value.replace(i, j)
            metadata_dict['ProcessorDate'] = processor_date_value.strip()

        if 'ProcessorVersion' in metadata_dict:
            replace_dic = {'$':'', 'Revision::':''}
            processor_version_value = metadata_dict['ProcessorVersion']
            for i, j in replace_dic.iteritems():
                processor_version_value = processor_version_value.replace(i, j)
            metadata_dict['ProcessorVersion'] = processor_version_value.strip()

        Metadata.__init__(self, metadata_dict, conventions='EGADS Algorithm', metadata_list=ALG_ATTR_LIST)
        self.child_metadata = []
        if isinstance(child_variable_metadata, list):
            for child in child_variable_metadata:
                self.assign_children(child)
        elif child_variable_metadata is not None:
            self.assign_children(child_variable_metadata)

    def assign_children(self, child):
        """
        Assigns children to current AlgorithmMetadata instance. Children are
        typically VariableMetadata instances. If VariableMetadata instance is
        used, this method also assigns current AlgorithmMetadata instance
        as parent in VariableMetadata child.

        :param VariableMetadata child:
            Child metadata object to add to current instance children.
        """

        logging.debug('egads - metadata.py - AlgorithmMetadata - assign_children - child ' + str(child))
        self.child_metadata.append(child)
        if isinstance(child, VariableMetadata):
            child.set_parent(self)

    logging.info('egads - metadata.py - AlgorithmMetadata has been loaded')
    

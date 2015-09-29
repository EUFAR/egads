__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__version__ = "$Revision:: 125       $"
__all__ = ["NetCdf", "EgadsNetCdf"]

import netCDF4
import egads
import nappy

from egads.input import FileCore

class NetCdf(FileCore):
    """
    EGADS class for reading and writing to generic NetCDF files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python NetCDF4 0.8.2
    library to the EGADS file-access methods.

    """

    TYPE_DICT = {'char':'c',
        'byte':'b',
        'short':'i2',
        'int':'i4',
        'float':'f4',
        'double':'f8'}



    def __del__(self):
        """
        If NetCDF file is still open on deletion of object, close it.
        """

        if self.f is not None:
            self.f.close()

    def open(self, filename, perms=None):
        """
        Opens NetCDF file given filename.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
        """

        FileCore.open(self, filename, perms)


    def get_attribute_list(self, varname=None):
        """
        Returns a dictionary of attributes and values found in current NetCDF file
        either globally, or attached to a given variable.

        :param string varname: Optional -
            Name of variable to get list of attributes from. If no variable name is
            provided, the function returns top-level NetCDF attributes.

        """

        return self._get_attribute_list(varname)

    def get_attribute_value(self, attrname, varname=None):
        """
        Returns value of an attribute given its name. If a variable name is provided,
        the attribute is returned from the variable specified, otherwise the global
        attribute is examined.

        :param string name:
            Name of attribute to examine
        :param string varname: Optional -
            Name of variable attribute is attached to. If none specified, global
            attributes are examined.

        :returns:
            Value of attribute examined
        :rtype:  string

        """

        attrs = self._get_attribute_list(varname)

        return attrs[attrname]

    def get_dimension_list(self, varname=None):
        """
        Returns a dictionary of dimensions and their sizes found in the current
        NetCDF file. If a variable name is provided, the dimension names and
        lengths associated with that variable are returned.


        :param string varname: Optional -
            Name of variable to get list of associated dimensions for. If no variable
            name is provided, the function returns all dimensions in the NetCDF file.

        """

        return self._get_dimension_list(varname)

    def get_variable_list(self):
        """
        Returns a list of variables found in the current NetCDF file.

        """

        return self._get_variable_list()


    def get_perms(self):
        """
        Returns the current permissions on the file that is open. Returns None if
        no file is currently open. Options are ``w`` for write (overwrites
        data in file),``a`` and ``r+`` for append, and ``r`` for read.


        """

        if self.f is not None:
            return self.perms
        else:
            return



    def read_variable(self, varname, input_range=None):
        """
        Reads a variable from currently opened NetCDF file.
        
        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range: Optional -
            Range of values in each dimension to input. TODO add example

        :returns:
            Values from specified variable read in from NetCDF file.
        :rtype: array
        """

        try:
            varin = self.f.variables[varname]
        except KeyError:
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            print "Error: Unexpected error"
            raise

        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)

            value = varin[eval(obj)]

        return value

    def write_variable(self, value, varname, dims=None, type='double', fill_value=None):
        """
        Writes/creates variable in currently opened NetCDF file.


        :param array value:
            Array of values to output to NetCDF file.
        :param string varname:
            Name of variable to create/write to.
        :param tuple dims: Optional -
            Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables,
            pass an empty tuple.
        :param string type: Optional -
            Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``,
            ``int``, ``short``, ``char``, and ``byte``
        :param float fill_value: Optional -
            Overrides default NetCDF _FillValue, if provided.

        """

        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                try:
                    varout = self.f.createVariable(varname, self.TYPE_DICT[type], dims)
                except KeyError:
                    varout = self.f.createVariable(varname, type, dims)

            varout[:] = value


    def add_dim(self, name, size):
        """
        Adds dimension to currently open file.

        :param string name:
            Name of dimension to add
        :param integer size:
            Integer size of dimension to add.

        """

        if self.f is not None:
            self.f.createDimension(name, size)
        else:
            raise # TODO add file execption

    def add_attribute(self, attrname, value, varname=None):
        """
        Adds attribute to currently open file. If varname is included, attribute
        is added to specified variable, otherwise it is added to global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string value:
            Value to assign to attribute name.
        :param string varname: Optional -
            If varname is provided, attribute name and value are added to specified
            variable in the NetCDF file.
        """

        if self.f is not None:
            if varname is not None:
                varin = self.f.variables[varname]
                setattr(varin, attrname, value)
            else:
                setattr(self.f, attrname, value)
        else:
            print 'ERROR: No file open'

    def convert_to_nasa_ames(self, na_file=None, var_ids=None, na_items_to_override={},
                             only_return_file_names=False, exclude_vars=[],
                             requested_ffi=None, delimiter='    ', float_format='%g',
                             size_limit=None, annotation=False, no_header=False):
        """
        Convert currently open NetCDF file to one or more NASA Ames files
        using the Nappy API.

        :param string na_file:
            Optional - Name of output NASA Ames file. If none is provided, name of
            current NetCDF file is used and suffix changed to .na
        :param list var_ids:
            List of variables (as ids) to include in the output file.
        :param dict na_items_to_override:
            Optional - Dictionary of NASA Ames keyword items with corresponding values
            to override in output file. NASA Ames keywords are: DATE, RDATE,
            ANAME, MNAME, ONAME, ORG, SNAME, VNAME
        :param bool only_return_file_names:
            Optional - If true, only return list of file names that would be written.
            Default - False
        :param list exclude_vars:
            Optional - List of variables (as ids) to exclude from the output NASA
            Ames file.
        :param int requested_ffi:
            The NASA Ames File Format Index (FFI) you wish to write to. Options
            are limited depending on the data structures found.
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - Tab.
        :param string float_format:
            Optional - The formatting string used for formatting floats when writing
            to output file. Default - %g
        :param int size_limit:
            Optional - If format FFI is 1001 then chop files into size_limit rows of data.
        :param bool annotation:
            Optional - If set to true, write the output file with an additional left-hand
            column describing the contents of each header line. Default - False.
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.


        """

        nappy.convertNCToNA(self.filename, na_file, var_ids, na_items_to_override,
                            only_return_file_names, exclude_vars, requested_ffi,
                            delimiter, float_format, size_limit, annotation,
                            no_header)

    def convert_to_csv(self, csv_file=None):
        """
        Converts currently open NetCDF file to CSV file using Nappy API.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        """

        nappy.convertNCToCSV(self.filename, csv_file)


    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        self.close()

        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            print "ERROR: Unexpected error"
            raise


    def _get_attribute_list(self, var=None):
        """
        Private method for getting attributes from a NetCDF file. Gets global
        attributes if no variable name is provided, otherwise gets attributes
        attached to specified variable. Function returns dictionary of values.
        """

        if self.f is not None:
            if var is not None:
                varin = self.f.variables[var]
                return varin.__dict__
            else:
                return self.f.__dict__
        else:
            raise # TODO add specific file exception

    def _get_dimension_list(self, var=None):
        """
        Private method for getting list of dimension names and lengths. If
        variable name is provided, method returns list of dimension names
        attached to specified variable, if none, returns all dimensions in the file.
        """

        dimdict = {}

        if self.f is not None:
            file_dims = self.f.dimensions

            if var is not None:
                varin = self.f.variables[var]
                dims = varin.dimensions

                for dimname in dims:
                    dimobj = file_dims[dimname]
                    dimdict[dimname] = len(dimobj)
            else:
                dims = file_dims

                for dimname, dimobj in dims.iteritems():
                    dimdict[dimname] = len(dimobj)

            return dimdict
        else:
            raise # TODO add specific file exception

        return None


    def _get_variable_list(self):
        """
        Private method for getting list of variable names.
        """

        if self.f is not None:
            return self.f.variables.keys()
        else:
            raise # TODO Add specific file exception




class EgadsNetCdf(NetCdf):
    """
    EGADS class for reading and writing to NetCDF files following EUFAR
    conventions. Inherits from the general EGADS NetCDF module.

    """


    FILE_ATTR_DICT = {'Conventions':'conventions',
                      'title':'title',
                      'source':'source',
                      'institution':'institution',
                      'project':'project',
                      'date_created':'date_created',
                      'geospatial_lat_min':'geospatial_lat_min',
                      'geospatial_lat_max':'geospatial_lat_max',
                      'geospatial_lon_min':'geospatial_lon_min',
                      'geospatial_lon_max':'geospatial_lon_max',
                      'geospatial_vertical_min':'geospatial_vertical_min',
                      'geospatial_vertical_max':'geospatial_vertical_max',
                      'geospatial_vertical_positive':'geospatial_vertical_positive',
                      'geospatial_vertical_units':'geospatial_vertical_units',
                      'time_coverage_start':'time_coverage_start',
                      'time_coverage_end':'time_coverage_end',
                      'time_coverage_duration':'time_coverage_duration',
                      'history':'history',
                      'references':'references',
                      'comment':'comment'}



    VAR_ATTR_DICT = {'units':'units',
                     '_FillValue':'fill_value',
                     'long_name':'long_name',
                     'standard_name':'standard_name',
                     'valid_range':'valid_range',
                     'valid_min':'valid_min',
                     'valid_max':'valid_max',
                     'SampledRate':'sampled_rate',
                     'Category':'category',
                     'CalibrationCoefficients':'calibration_coefficients',
                     'InstrumentLocation':'instrument_location',
                     'instrumentCoordinates':'instrument_coordinates',
                     'Dependencies':'dependencies',
                     'Processor':'processor',
                     'Comments':'comments',
                     'ancillary_variables':'ancillary_variables',
                     'flag_values':'flag_values',
                     'flag_masks':'flag_masks',
                     'flag_meanings':'flag_meanings'}

    RAF_GLOBAL_DICT = {'institution':'institution',
                'Address':None,
                'Phone':None,
                'creator_url':None,
                'Conventions':'Conventions',
                'ConventionsURL':None,
                'ConventionsVersion':None,
                'Metadata_Conventions':None,
                'standard_name_vocabulary':None,
                'ProcessorRevision':None,
                'ProcessorURL':None,
                'date_created':'date_created',
                'ProjectName':'project',
                'Platform':None,
                'ProjectNumber':None,
                'FlightNumber':None,
                'FlightDate':None,
                'TimeInterval':None,
                'InterpolationMethod':None,
                'latitude_coordinate':'reference_latitude',
                'longitude_coordinate':'reference_longitude',
                'zaxis_coordinate':'reference_altitude',
                'time_coordinate':None,
                'geospatial_lat_min':'geospatial_lat_min',
                'geospatial_lat_max':'geospatial_lat_max',
                'geospatial_lon_min':'geospatial_lon_min',
                'geospatial_lon_max':'geospatial_lon_max',
                'geospatial_vertical_min':'geospatial_vertical_min',
                'geospatial_vertical_max':'geospatial_vertical_max',
                'geospatial_vertical_positive':'geospatial_vertical_positive',
                'geospatial_vertical_units':'geospatial_vertical_units',
                'wind_field':None,
                'landmarks':None,
                'Categories':None,
                'time_coverage_start':'time_coverage_start',
                'time_coverage_end':'time_coverage_end'}

    RAF_VARIABLE_DICT = {'_FillValue':'_FillValue',
                         'units':'units',
                         'long_name':'long_name',
                         'standard_name':'standard_name',
                         'valid_range':'valid_range',
                         'actual_min':None,
                         'actual_max':None,
                         'Category':'Category',
                         'SampledRate':'SampledRate',
                         'TimeLag':None,
                         'TimeLagUnits':None,
                         'DataQuality':None,
                         'CalibrationCoefficients':'CalibrationCoefficients',
                         'Dependencies':'Dependencies'}

    CF_GLOBAL_DICT = {'title':'title',
                      'references':'references',
                      'history':'history',
                      'Conventions':'Conventions',
                      'institution':'institution',
                      'source':'source',
                      'comment':'comment'}

    CF_VARIABLE_DICT = {'_FillValue':'_FillValue',
                        'valid_min':'valid_min',
                        'valid_max':'valid_max',
                        'valid_range':'valid_range',
                        'scale_factor':'scale_factor',
                        'add_offset':'add_offset',
                        'units':'units',
                        'long_name':'long_name',
                        'standard_name':'standard_name',
                        'ancillary_variables':'ancillary_variables',
                        'flag_values':'flag_values',
                        'flag_masks':'flag_masks',
                        'flag_meanings':'flag_meanings'}

    def __init__(self, filename=None, perms='r'):
        """
        Initializes NetCDF instance.

        :param string filename:
            Optional - Name of NetCDF file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default
            value.
        """

        self.file_metadata = None

        FileCore.__init__(self, filename, perms)




    def read_variable(self, varname, input_range=None):
        """
        Reads in a variable from currently opened NetCDF file and maps the NetCDF
        attributies to an :class:`~egads.core.EgadsData` instance.


        :param string varname:
            Name of NetCDF variable to read in.

        :param vector input_range:
            Optional -- Range of values in each dimension to input. :TODO: add example


        :returns: Values and metadata of the specified variable in an EgadsData instance.
        :rtype: EgadsData

        """

        try:
            varin = self.f.variables[varname]
        except KeyError:
            print "ERROR: Variable %s does not exist in %s" % (varname, self.filename)
            raise KeyError
        except Exception:
            print "Error: Unexpected error"
            raise

        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)

            value = varin[eval(obj)]

        variable_attrs = self.get_attribute_list(varname)

        variable_attrs['cdf_name'] = varname
        variable_metadata = egads.core.metadata.VariableMetadata(variable_attrs,
                                                                 self.file_metadata)

        data = egads.EgadsData(value, variable_metadata=variable_metadata)

        return data

    def write_variable(self, data, varname=None, dims=None, type='double'):
        """
        Writes/creates varible in currently opened NetCDF file.


        :param EgadsData data:
            Instance of EgadsData object to write out to file.
            All data and attributes will be written out to the file.

        :param string varname: Optional -
            Name of variable to create/write to. If no varname is provided,
            and if cdf_name attribute in EgadsData object is defined, then the
            variable will be written to cdf_name.
        :param tuple dims: Optional - 
            Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables,
            pass an empty tuple.
        :param string type: Optional - 
            Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``,
            ``int``, ``short``, ``char``, and ``byte``

        """

        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                varout = self.f.createVariable(varname, self.TYPE_DICT[type.lower()], dims)

            varout[:] = data.value

            for key, val in self.VAR_ATTR_DICT.iteritems():
                attribute = getattr(data, val)
                setattr(varout, key, attribute)

    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        self.close()

        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self.perms = perms
            attr_dict = self.get_attribute_list()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename)
        except RuntimeError:
            print "ERROR: File %s doesn't exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise





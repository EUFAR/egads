__author__ = "mfreer, ohenry"
__date__ = "$Date:: 2016-12-6 15:47#$"
__version__ = "$Revision:: 126       $"
__all__ = ["NetCdf", "EgadsNetCdf"]

import logging
import netCDF4
import egads
import nappy  # @UnresolvedImport
from egads.input import FileCore

class NetCdf(FileCore):
    """
    EGADS class for reading and writing to generic NetCDF files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python NetCDF4
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
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write 
            (overwrites data in file), ``a`` and ``r+`` for append, and ``r`` for 
            read. ``r`` is the default value
        """

        FileCore.open(self, filename, perms)

    def get_attribute_list(self, varname=None):
        """
        Returns a dictionary of attributes and values found in current NetCDF file
        either globally, or attached to a given variable.

        :param string varname:
            Optional - Name of variable to get list of attributes from. If no variable name is
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
        :param string varname:
            Optional - Name of variable attribute is attached to. If none specified, global
            attributes are examined.
        """
        
        logging.debug('egads.input.get_attribute_value invocked: attrname ' + str(attrname) + ', varname ' + str(varname))
        attrs = self._get_attribute_list(varname)
        logging.debug('................................................attrs[attrname] ' + 
                          str(attrs[attrname]))
        return attrs[attrname]

    def get_dimension_list(self, varname=None):
        """
        Returns a dictionary of dimensions and their sizes found in the current
        NetCDF file. If a variable name is provided, the dimension names and
        lengths associated with that variable are returned.

        :param string varname:
            Optional - Name of variable to get list of associated dimensions for. If no variable
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
        
        logging.debug('egads.input.get_perms invocked')
        if self.f is not None:
            return self.perms
        else:
            logging.error('egads.input.get_perms invocked: AttributeError, no file open')
            raise AttributeError('No file open')

    def read_variable(self, varname, input_range=None):
        """
        Reads a variable from currently opened NetCDF file.
        
        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input. TODO add example
        """
        
        logging.debug('egads.input.read_variable invocked: varname ' + str(varname) + ', input_range ' + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.error('egads.input.NetCdf.read_variable invocked: KeyError, variable does not exist in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.error('egads.input.NetCdf.read_variable invocked: Exception, unexpected error')
            raise Exception("Error: Unexpected error")
        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        logging.debug('egads.input.NetCdf.read_variable invoked: varname ' + str(varname) + ' -> data read OK')
        return value
    
    def change_variable_name(self, varname, newname):
        """
        Change the variable name in currently opened NetCDF file.
        
        :param string varname:
            Name of variable to rename.
        :param string oldname:
            the new name.
        """
        
        logging.debug('egads.input.change_variable_name invocked: varname ' + str(varname) + ', newname ' + str(newname))
        if self.f is not None:
            self.f.renameVariable(varname, newname)
        else:
            logging.error('egads.input.change_variable_name invocked: AttributeError, no file open')
            raise AttributeError('No file open')

    def write_variable(self, value, varname, dims=None, ftype='double', fillvalue=None):
        """
        Writes/creates variable in currently opened NetCDF file.

        :param array value:
            Array of values to output to NetCDF file.
        :param string varname:
            Name of variable to create/write to.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables, pass an empty tuple.
        :param string type:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``, 
            ``short``, ``char``, and ``byte``
        :param float fill_value:
            Optional - Overrides default NetCDF _FillValue, if provided.
        """

        logging.debug('egads.input.NetCdf.write_variable invoked: varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype) + ', fillvalue ' + str(fillvalue))
        if self.f is not None:
            try:
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype], dims, fill_value = fillvalue)
            except KeyError:
                varout = self.f.createVariable(varname, ftype, dims, fillvalue)
            varout[:] = value
        else:
            logging.error('egads.input.change_variable_name invocked: AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads.input.NetCdf.write_variable invoked: varname ' + str(varname) + ' -> data write OK')

    def add_dim(self, name, size):
        """
        Adds dimension to currently open file.

        :param string name:
            Name of dimension to add
        :param integer size:
            Integer size of dimension to add.
        """

        logging.debug('egads.input.NetCdf.add_dim invoked: name ' + str(name) + ', size ' + str(size))
        if self.f is not None:
            self.f.createDimension(name, size)
        else:
            logging.error('egads.input.change_variable_name invocked: AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads.input.NetCdf.add_dim invoked: name ' + str(name) + ' -> dim add OK')

    def add_attribute(self, attrname, value, varname=None):
        """
        Adds attribute to currently open file. If varname is included, attribute
        is added to specified variable, otherwise it is added to global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string value:
            Value to assign to attribute name.
        :param string varname:
            Optional - If varname is provided, attribute name and value are added to specified
            variable in the NetCDF file.
        """
        
        logging.debug('egads.input.NetCdf.add_attribute invoked: attrname ' + str(attrname) + 
                      ', value ' + str(value) + ', varname ' + str(varname))
        if self.f is not None:
            if varname is not None:
                varin = self.f.variables[varname]
                setattr(varin, attrname, value)
            else:
                setattr(self.f, attrname, value)
        else:
            logging.error('egads.input.change_variable_name invocked: AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads.input.NetCdf.add_attribute invoked: attrname ' + str(attrname) + ' -> dim add OK')

    '''def convert_to_nasa_ames(self, na_file=None, requested_ffi=None, delimiter='    ', float_format='%g',
                             size_limit=None, annotation=False, no_header=False):
        """
        Convert currently open NetCDF file to one or more NASA Ames files
        using  Nappy.

        :param string na_file:
            Optional - Name of output NASA Ames file. If none is provided, name of
            current NetCDF file is used and suffix changed to .na
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
        
        na_dict = {"A":"","AMISS":"","ANAME":"","ASCAL":"","DATE":"","DX":"",
                     "FFI":"","IVOL":"","LENA":"","LENX":"","MNAME":"","NAUXC":"",
                     "NAUXV":"","NCOM":"","NIV":"","NLHEAD":"","NNCOML":"",
                     "NSCOML":"","NV":"","NVOL":"","NVPM":"","NX":"","NXDEF":"",
                     "ONAME":"","ORG":"","RDATE":"","SCOM":"","SNAME":"","V":"",
                     "VMISS":"","VNAME":"","VSCAL":"","X":"","XNAME":""}
        
        
        """Conventions = None
        source = SNAME
        title = MNAME
        institution = ONAME&ORG
        references = None
        comment = SCOM&NCOM
        history = RDATE
        file_format_index = FFI
        no_of_nasa_ames_header_lines = NLHEAD
        total_files_in_set = NVOL
        file_number_in_set = IVOL
        first_valid_date_of_data = DATE"""
        
        
        
        
        if na_file is None:
            na_file = self.filename
        
        self.f_out = nappy.openNAFile(na_file, mode="w", na_dict=na_dict)
        self.f_out.write()
        self.f_out.close()'''


    '''def convert_to_csv(self, csv_file=None, temp_file = False):
        """
        Converts currently open NetCDF file to CSV file using Nappy API.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        """
        
        if temp_file:
            filename = temp_file
        else:
            filename = self.filename
        nappy.convertNCToCSV(filename, csv_file)'''


    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        logging.debug('egads.input.NetCdf._open_file invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            self.f = netCDF4.Dataset(filename, perms)  # @UndefinedVariable
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            logging.error('egads.input.NetCdf._open_file invoked: RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.error('egads.input.NetCdf._open_file invoked: IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.error('egads.input.NetCdf._open_file invoked: Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

    def _get_attribute_list(self, var=None):
        """
        Private method for getting attributes from a NetCDF file. Gets global
        attributes if no variable name is provided, otherwise gets attributes
        attached to specified variable. Function returns dictionary of values.
        """
        
        logging.debug('egads.input.NetCdf._get_attribute_list invoked: var ' + str(var))
        if self.f is not None:
            if var is not None:
                varin = self.f.variables[var]
                logging.debug('................................................attr_list ' + str(varin.__dict__))
                return varin.__dict__
            else:
                logging.debug('................................................attr_list ' + str(self.f.__dict__))
                return self.f.__dict__
        else:
            logging.error('egads.input.NetCdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_dimension_list(self, var=None):
        """
        Private method for getting list of dimension names and lengths. If
        variable name is provided, method returns list of dimension names
        attached to specified variable, if none, returns all dimensions in the file.
        """
        
        logging.debug('egads.input.NetCdf._get_dimension_list invoked: var ' + str(var))
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
            logging.debug('................................................dimdict ' + str(dimdict))
            return dimdict
        else:
            logging.error('egads.input.NetCdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')
        return None

    def _get_variable_list(self):
        """
        Private method for getting list of variable names.
        """

        logging.debug('egads.input.NetCdf._get_variable_list invoked')
        if self.f is not None:
            return self.f.variables.keys()
        else:
            logging.error('egads.input.NetCdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    logging.info('egads.input.NetCdf has been loaded')


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
            Options are ``w`` for write (overwrites data), ``a`` and ``r+`` for append, and ``r`` 
            for read. ``r`` is the default value.
        """

        logging.debug('egads.input.EgadsNetCdf.__init__ invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    def read_variable(self, varname, input_range=None):
        """
        Reads in a variable from currently opened NetCDF file and maps the NetCDF
        attributies to an :class:`~egads.core.EgadsData` instance.

        :param string varname:
            Name of NetCDF variable to read in.

        :param vector input_range:
            Optional - Range of values in each dimension to input. :TODO: add example
        """
        
        logging.debug('egads.input.EgadsNetCdf.read_variable invoked: varname ' + str(varname) + 
                      ', input_range ' + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.error('egads.input.EgadsNetCdf.read_variable invocked: KeyError, variable does not exist in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.error('egads.input.EgadsNetCdf.read_variable invocked: Exception, unexpected error')
            raise Exception("Error: Unexpected error")
        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        variable_attrs = self.get_attribute_list(varname)
        variable_attrs['cdf_name'] = varname
        variable_metadata = egads.core.metadata.VariableMetadata(variable_attrs, self.file_metadata)
        data = egads.EgadsData(value, variable_metadata=variable_metadata)
        logging.debug('egads.input.EgadsNetCdf.read_variable invoked: varname ' + str(varname) + ' -> data read OK')
        return data

    def write_variable(self, data, varname=None, dims=None, ftype='double'):
        """
        Writes/creates varible in currently opened NetCDF file.

        :param EgadsData data:
            Instance of EgadsData object to write out to file.
            All data and attributes will be written out to the file.
        :param string varname:
            Optional - Name of variable to create/write to. If no varname is provided,
            and if cdf_name attribute in EgadsData object is defined, then the variable will be 
            written to cdf_name.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables, pass an empty tuple.
        :param string type:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``, 
            ``short``, ``char``, and ``byte``
        """

        logging.debug('egads.input.EgadsNetCdf.write_variable invoked: varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype))
        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype.lower()], dims)
            varout[:] = data.value
            for key, val in self.VAR_ATTR_DICT.iteritems():
                attribute = getattr(data, val)
                setattr(varout, key, attribute)
        logging.debug('egads.input.EgadsNetCdf.write_variable invoked: varname ' + str(varname) + ' -> data write OK')

    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads.input.EgadsNetCdf._open_file invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            self.f = netCDF4.Dataset(filename, perms)  # @UndefinedVariable
            self.filename = filename
            self.perms = perms
            attr_dict = self.get_attribute_list()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename)
        except RuntimeError:
            logging.error('egads.input.EgadsNetCdf._open_file invoked: RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.error('egads.input.EgadsNetCdf._open_file invoked: IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.error('egads.input.EgadsNetCdf._open_file invoked: Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")
        
    logging.info('egads.input.EgadsNetCdf has been loaded')


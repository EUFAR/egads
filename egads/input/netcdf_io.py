__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 15:47"
__version__ = "1.18"
__all__ = ["NetCdf", "EgadsNetCdf"]

import logging
import netCDF4
import egads
import datetime
import operator
import os
import collections
import dateutil
import numpy
from egads.input import FileCore


class NetCdf(FileCore):
    """
    EGADS class for reading and writing to generic NetCDF files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python NetCDF4
    library to the EGADS file-access methods.
    """

    TYPE_DICT = {'char': 'c',
                 'byte': 'b',
                 'short': 'i2',
                 'int': 'i4',
                 'float': 'f4',
                 'double': 'f8'}

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
        
        logging.debug('egads - netcdf_io.py - NetCdf - open')
        FileCore.open(self, filename, perms)

    def get_attribute_list(self, varname=None):
        """
        Returns a dictionary of attributes and values found in current NetCDF file
        either globally, or attached to a given variable.

        :param string varname:
            Optional - Name of variable to get list of attributes from. If no variable name is
            provided, the function returns top-level NetCDF attributes.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_attribute_list - varname ' + str(varname))
        return self._get_attribute_list(varname)

    def get_attribute_value(self, attrname, varname=None):
        """
        Returns value of an attribute given its name. If a variable name is provided,
        the attribute is returned from the variable specified, otherwise the global
        attribute is examined.

        :param string attrname:
            Name of attribute to examine
        :param string varname:
            Optional - Name of variable attribute is attached to. If none specified, global
            attributes are examined.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_attribute_value - attrname ' + str(attrname)
                      + ', varname ' + str(varname))
        attrs = self._get_attribute_list(varname)
        return attrs[attrname]

    def get_dimension_list(self, varname=None):
        """
        Returns an ordered dictionary of dimensions and their sizes found in the current
        NetCDF file. If a variable name is provided, the dimension names and
        lengths associated with that variable are returned.

        :param string varname:
            Optional - Name of variable to get list of associated dimensions for. If no variable
            name is provided, the function returns all dimensions in the NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_dimension_list - varname ' + str(varname))
        return self._get_dimension_list(varname)

    def get_variable_list(self):
        """
        Returns a list of variables found in the current NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_variable_list')
        return self._get_variable_list()

    def get_perms(self):
        """
        Returns the current permissions on the file that is open. Returns None if
        no file is currently open. Options are ``w`` for write (overwrites
        data in file),``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_perms')
        if self.f is not None:
            return self.perms
        else:
            logging.exception('egads - netcdf_io.py - NetCdf - get_perms - AttributeError, no file open')
            raise AttributeError('No file open')

    def read_variable(self, varname, input_range=None, read_as_float=False, replace_fill_value=False):
        """
        Reads a variable from currently opened NetCDF file.
        
        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN,
            if one of those attributes exists in the NetCDF file.
            ``False`` is the default value.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - read_variable - varname ' + str(varname) + ', input_range '
                      + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.exception('egads - netcdf_io.py - NetCdf - read_variable - KeyError, variable does not exist in '
                              'netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.exception('egads - netcdf_io.py - NetCdf - read_variable - Exception, unexpected error')
            raise Exception("Error: Unexpected error")
        if input_range is None:
            value = varin[:]
            if read_as_float:
                value = [float(item) for item in value]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in range(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
            if read_as_float:
                value = [float(item) for item in value]
        if replace_fill_value:
            _fill_value = None
            try:
                _fill_value = self.get_attribute_value('_FillValue', varname)
            except KeyError:
                try:
                    _fill_value = self.get_attribute_value('missing_value', varname)
                except KeyError:
                    logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname)
                                  + ', no _FillValue or missing_value attribute found.')
            if _fill_value is not None:
                value[value == _fill_value] = numpy.nan
        logging.debug('egads - netcdf_io.py - NetCdf - read_variable - varname ' + str(varname) + ' -> data read OK')
        return value
    
    def change_variable_name(self, varname, newname):
        """
        Change the variable name in currently opened NetCDF file.
        
        :param string varname:
            Name of variable to rename.
        :param string newname:
            The new name.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - change_variable_name - varname ' + str(varname)
                      + ', newname ' + str(newname))
        if self.f is not None:
            self.f.renameVariable(varname, newname)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - .change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')

    def write_variable(self, data, varname, dims=None, ftype='double', fillvalue=None):
        """
        Writes/creates variable in currently opened NetCDF file.

        :param array data:
            Array of values to output to NetCDF file.
        :param string varname:
            Name of variable to create/write to.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables, pass an empty tuple.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``, 
            ``short``, ``char``, and ``byte``
        :param float fillvalue:
            Optional - Overrides default NetCDF _FillValue, if provided.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - write_variable - varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype) + ', fillvalue ' + str(fillvalue))
        if self.f is not None:
            try:
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype], dims, fill_value=fillvalue)
            except KeyError:
                varout = self.f.createVariable(varname, ftype, dims, fillvalue)
            varout[:] = data
        else:
            logging.error('egads - netcdf_io.py - NetCdf - change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - write_variable - varname ' + str(varname) + ' -> data write OK')

    def add_dim(self, name, size):
        """
        Adds dimension to currently open file.

        :param string name:
            Name of dimension to add
        :param integer size:
            Integer size of dimension to add.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - add_dim - name ' + str(name) + ', size ' + str(size))
        if self.f is not None:
            self.f.createDimension(name, size)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - add_dim - name ' + str(name) + ' -> dim add OK')

    def add_attribute(self, attrname, value, varname=None):
        """
        Adds attribute to currently open file. If varname is included, attribute
        is added to specified variable, otherwise it is added to global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string|float|int value:
            Value to assign to attribute name.
        :param string varname:
            Optional - If varname is provided, attribute name and value are added to specified
            variable in the NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - add_attribute - attrname ' + str(attrname) + ', varname '
                      + str(varname))
        if self.f is not None:
            if isinstance(value, list):
                tmp = ''
                for item in value:
                    tmp += item + ', '
                value = tmp[:-2]
            if varname is not None:
                varin = self.f.variables[varname]
                setattr(varin, attrname, value)
            else:
                setattr(self.f, attrname, value)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - add_attribute - attrname ' + str(attrname)
                      + ' -> attribute add OK')
        
    def delete_attribute(self, attrname, varname=None):
        """
        Deletes attribute to currently open file. If varname is included, attribute
        is removed from specified variable, otherwise it is removed from global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string varname:
            Optional - If varname is provided, attribute removed from specified
            variable in the NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - delete_attribute - attrname ' + str(attrname) + 
                      ', varname ' + str(varname))
        if self.f is not None:
            if varname is not None:
                delattr(self.f.variables[varname], attrname)
            else:
                delattr(self.f, attrname)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - delete_attribute - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - delete_attribute - attrname ' + str(attrname)
                      + ' -> attribute delete OK')

    def convert_to_nasa_ames(self, na_file=None, float_format=None, delimiter='    ', no_header=False):
        """
        Convert currently open NetCDF file to one or more NASA Ames files.
        For now can only process NetCdf files to NASA/Ames FFI 1001 : 
        only time as an independant variable.

        :param string na_file:
            Optional - Name of output NASA Ames file. If none is provided, name of
            current NetCDF file is used and suffix changed to .na
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - Tab.
        :param string float_format:
            Optional - The format of float numbers to be saved. If no string is entered, values are
            not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - '    ' (four spaces).
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames - float_format ' + str(float_format)
                      + ', delimiter ' + str(delimiter) + ', no_header ' + str(no_header))

        if not na_file:
            na_file = os.path.splitext(self.filename)[0] + '.na'

        # read dimensions and variables, try to check if ffi = 1001
        dim_list = self.get_dimension_list()
        var_list = self.get_variable_list()
        if len(dim_list) > 1:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - the actual convert_to_nasa_ames cant '
                              'process file with multiple dimensions, FFI is set to 1001')
            raise Exception('the actual convert_to_nasa_ames cant process file with multiple dimensions, '
                            'FFI is set to 1001')

        # create NASA/Ames dictionary
        f = egads.input.NasaAmes()
        na_dict = f.create_na_dict()
        missing_attributes = []

        # populate NLHEAD, FFI, ONAME, ORG, SNAME, MNAME, RDATE, DX, IVOL, NVOL
        nlhead, ffi, org, oname, sname, mname, dx = -999, 1001, '', '', '', '', 0.0
        ivol, nvol, date, niv, nv = 1, 1, None, 0, 0
        try:
            org = self.get_attribute_value('institution')
        except KeyError:
            org = 'no institution'
            missing_attributes.append('institution')
        try:
            oname = self.get_attribute_value('authors')
        except KeyError:
            try:
                oname = self.get_attribute_value('institution')
                missing_attributes.append('authors - replaced by institution')
            except KeyError:
                oname = 'no author'
                missing_attributes.append('authors')
        try:
            sname = self.get_attribute_value('source')
        except KeyError:
            sname = 'no source'
            missing_attributes.append('source')
        try:
            mname = self.get_attribute_value('title')
        except KeyError:
            mname = 'no title'
            missing_attributes.append('title')
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]

        # read independant variables
        independant_variables = []
        for key in dim_list:
            try:
                var = self.read_variable(key).tolist()
                attr_dict = {}
                for attr in self.get_attribute_list(key):
                    attr_dict[attr] = self.get_attribute_value(attr, key)
                independant_variables.append([key, var, attr_dict])
                niv += 1
            except KeyError:
                independant_variables.append([key, None, None])

        # populate DATE if time is in independant_variables
        for sublist in independant_variables:
            if 'time' in sublist[0]:
                try:
                    index = sublist[2]['units'].index(' since ')
                    ref_time = dateutil.parser.parse(sublist[2]['units'][index + 7:]).strftime("%Y%m%dT%H%M%S")
                    isotime = egads.algorithms.transforms.SecondsToIsotime().run(sublist[1], ref_time)
                    y, m, d, _, _, _ = egads.algorithms.transforms.IsotimeToElements().run(isotime)
                    date = [y.value[0], m.value[0], d.value[0]]
                except Exception:
                    date = [999, 999, 999]
        if not date:
            date = [999, 999, 999]

        # add first global metadata to na file
        f.write_attribute_value('NLHEAD', nlhead, na_dict=na_dict)
        f.write_attribute_value('FFI', ffi, na_dict=na_dict)
        f.write_attribute_value('ONAME', oname, na_dict=na_dict)
        f.write_attribute_value('ONAME', oname, na_dict=na_dict)
        f.write_attribute_value('ORG', org, na_dict=na_dict)
        f.write_attribute_value('SNAME', sname, na_dict=na_dict)
        f.write_attribute_value('MNAME', mname, na_dict=na_dict)
        f.write_attribute_value('DATE', date, na_dict=na_dict)
        f.write_attribute_value('RDATE', rdate, na_dict=na_dict)
        f.write_attribute_value('NIV', niv, na_dict=na_dict)
        f.write_attribute_value('DX', dx, na_dict=na_dict)
        f.write_attribute_value('NVOL', nvol, na_dict=na_dict)
        f.write_attribute_value('IVOL', ivol, na_dict=na_dict)

        # read variables
        variables = []
        for var in var_list:
            if var not in dim_list:
                dim = self.get_dimension_list(var)
                value = self.read_variable(var).tolist()
                attr_dict = {}
                all_attr = self.get_attribute_list(var)
                for index, item in enumerate(value):
                    if item is None:
                        value[index] = all_attr['_FillValue']
                for attr in all_attr:
                    attr_dict[attr] = self.get_attribute_value(attr, var)
                variables.append([var, value, dim, attr_dict])

        # prepare and set NCOM and SCOM
        name_string = ''
        ncom = ['==== Normal Comments follow ====']
        ncom = ['The NA file has been converted from a NetCDF file by EGADS']
        for attr in self.get_attribute_list():
            if attr != 'institution' and attr != 'authors' and attr != 'source' and attr != 'title':
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
        ncom.append('==== Normal Comments end ====')
        ncom.append('=== Data Section begins on the next line ===')
        for name in dim_list:
            name_string += name + '    '
        scom = ['==== Special Comments follow ====',
                '=== Additional Variable Attributes defined in the source file ===',
                '== Variable attributes from source (NetCDF) file follow ==']
        for var in variables:
            if var[0] not in dim_list:
                first_line = True
                for metadata in var[3]:
                    if metadata != '_FillValue' and metadata != 'scale_factor' and metadata != 'units' and metadata \
                            != 'var_name':
                        if first_line:
                            first_line = False
                            scom.append('  Variable ' + var[0] + ':')
                        try:
                            scom.append('    ' + metadata + ' = ' + str(var[3][metadata]))
                        except TypeError:
                            logging.exception('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - an error '
                                              + 'occurred when trying to add variable metadata in SCOM - metadata '
                                              + str(metadata))
                name_string += var[0] + '    '
        name_string = name_string[:-4]
        ncom.append(name_string)
        scom.append('== Variable attributes from source (NetCDF) file end ==')
        scom.append('==== Special Comments end ====')
        f.write_attribute_value('SCOM', scom, na_dict=na_dict)
        f.write_attribute_value('NCOM', ncom, na_dict=na_dict)
        f.write_attribute_value('NSCOML', len(scom), na_dict=na_dict)
        f.write_attribute_value('NNCOML', len(ncom), na_dict=na_dict)

        # write independant variable
        xname, x = None, None
        for ivar in independant_variables:
            x = ivar[1]
            try:
                units = ivar[2]['units']
            except KeyError:
                units = 'no units'
            xname = ivar[0] + ' (' + units + ')'
        f.write_attribute_value('XNAME', xname, na_dict=na_dict)
        f.write_attribute_value('X', x, na_dict=na_dict)

        # write main variables
        vmiss, vscal, vname, v = [], [], [], []
        for var in variables:
            try:
                units = var[3]['units']
            except KeyError:
                units = ''
            try:
                miss = var[3]['_FillValue']
            except KeyError:
                try:
                    miss = var[3]['missing_value']
                except KeyError:
                    miss = None
            vmiss.append(miss)
            vscal.append(1)
            vname.append(var[0] + ' (' + units + ')')
            v.append(var[1])
            nv += 1

        f.write_attribute_value('VMISS', vmiss, na_dict=na_dict)
        f.write_attribute_value('VSCAL', vscal, na_dict=na_dict)
        f.write_attribute_value('XNAME', xname, na_dict=na_dict)
        f.write_attribute_value('VNAME', vname, na_dict=na_dict)
        f.write_attribute_value('V', v, na_dict=na_dict)
        f.write_attribute_value('X', x, na_dict=na_dict)
        f.write_attribute_value('NV', nv, na_dict=na_dict)

        # write na file
        f.save_na_file(na_file, na_dict=na_dict, float_format=float_format, delimiter=delimiter, no_header=no_header)
        f.close()
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ' -> file conversion OK')
      
    def convert_to_csv(self, csv_file=None, float_format=None, no_header=False):
        """
        Converts currently open NetCDF file to CSV file using the NasaAmes class.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        :param string float_format:
            Optional - The format of float numbers to be saved. If no string is entered, values are
            not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ', float_format ' + str(float_format) + ', no_header ' + str(no_header))
        if not csv_file:
            csv_file = os.path.splitext(self.filename)[0] + '.csv'
        
        self.convert_to_nasa_ames(na_file=csv_file, float_format=float_format,delimiter=',', no_header=no_header)
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ' -> file conversion OK')

    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _open_file')
        self.close()
        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            logging.exception('egads - netcdf_io.py - NetCdf - _open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - netcdf_io.py - NetCdf - _open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)
        except Exception:
            logging.exception('egads - netcdf_io.py - NetCdf - _open_file - Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

    def _get_attribute_list(self, var=None):
        """
        Private method for getting attributes from a NetCDF file. Gets global
        attributes if no variable name is provided, otherwise gets attributes
        attached to specified variable. Function returns dictionary of values.
        If multiple white spaces exist, they are removed.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - _get_attribute_list - var ' + str(var))
        if self.f is not None:
            if var is not None:
                attr_dict = {}
                varin = self.f.variables[var]
                for key, value in varin.__dict__.items():
                    if isinstance(value, str):
                        value = " ".join(value.split())
                    attr_dict[key] = value
                return attr_dict
            else:
                attr_dict = {}
                for key, value in self.f.__dict__.items():
                    if isinstance(value, str):
                        value = " ".join(value.split())
                    attr_dict[key] = value
                return attr_dict
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _get_attribute_list - AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_dimension_list(self, var=None):
        """
        Private method for getting list of dimension names and lengths. If
        variable name is provided, method returns list of dimension names
        attached to specified variable, if none, returns all dimensions in the file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - _get_dimension_list - var ' + str(var))
        dimdict = collections.OrderedDict()
        if self.f is not None:
            file_dims = self.f.dimensions
            if var:
                varin = self.f.variables[var]
                dims = varin.dimensions
                for dimname in dims:
                    dimobj = file_dims[dimname]
                    dimdict[dimname] = len(dimobj)
            else:
                dims = file_dims
                for dimname, dimobj in reversed(sorted(dims.items())):
                    dimdict[dimname] = len(dimobj)
            return dimdict
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _get_attribute_list - AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_variable_list(self):
        """
        Private method for getting list of variable names.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_variable_list')
        if self.f is not None:
            return list(self.f.variables.keys())
        else:
            logging.error('egads.input.NetCdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    logging.info('egads - netcdf_io.py - NetCdf has been loaded')


class EgadsNetCdf(NetCdf):
    """
    EGADS class for reading and writing to NetCDF files following EUFAR
    conventions. Inherits from the general EGADS NetCDF module.
    """

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

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - __init__')
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    def read_variable(self, varname, input_range=None, read_as_float=False, replace_fill_value=False):
        """
        Reads in a variable from currently opened NetCDF file and maps the NetCDF
        attributies to an :class:`~egads.core.EgadsData` instance.

        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input. ``None`` is the default value.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file. ``False`` is the default value.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN.
            ``False`` is the default value.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname) + 
                      ', input_range ' + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - read_variable - KeyError, variable does not exist'
                              ' in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - read_variable - Exception, unexpected error')
            raise Exception("Error: Unexpected error")
        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in range(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        if read_as_float:
            value = [float(item) for item in value]
        variable_attrs = self.get_attribute_list(varname)
        value = numpy.array(value)
        if replace_fill_value:
            if '_FillValue' in variable_attrs.keys():
                _fill_value = variable_attrs['_FillValue']
                value[value == _fill_value] = numpy.nan
            else:
                if 'missing_value' in variable_attrs.keys():
                    _fill_value = variable_attrs['missing_value']
                    value[value == _fill_value] = numpy.nan
                else:
                    logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname)
                                  + ', no _FillValue or missing_value attribute found.')
        variable_metadata = egads.core.metadata.VariableMetadata(variable_attrs, self.file_metadata)
        data = egads.EgadsData(value, variable_metadata=variable_metadata)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname)
                      + ' -> data read OK')
        return data

    def write_variable(self, data, varname=None, dims=None, ftype='double'):
        """
        Writes/creates variable in currently opened NetCDF file.

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
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``, 
            ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - write_variable - varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype))
        fillvalue = None
        if self.f is not None:
            try:
                varout = self.f.variables[varname]
            except KeyError:
                try:
                    fillvalue = data.metadata['_FillValue']
                except KeyError:
                    try:
                        fillvalue = data.metadata['missing_value']
                    except KeyError:
                        pass
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype.lower()], dims, fill_value=fillvalue)
            if fillvalue is not None:
                varout[:] = numpy.where(numpy.isnan(data.value), fillvalue, data.value)
            else:
                varout[:] = data.value
            for key, val in data.metadata.items():
                if key != '_FillValue':
                    if val:
                        if isinstance(val, list):
                            tmp = ''
                            for item in val:
                                tmp += item + ', '
                            setattr(varout, str(key), tmp[:-2])
                        else:
                            setattr(varout, str(key), val)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - write_variable - varname ' + str(varname)
                      + ' -> data write OK')
        
    def convert_to_nasa_ames(self, na_file=None, float_format=None, delimiter='    ', no_header=False):
        """
        Convert currently open EGADS NetCDF file to one or more NASA Ames files.
        For now can only process NetCdf files to NASA/Ames FFI 1001 : variables
        can only be dependant to one independant variable at a time.

        :param string na_file:
            Optional - Name of output NASA Ames file. If none is provided, name of
            current NetCDF file is used and suffix changed to .na
        :param string float_format:
            Optional - The format of float numbers to be saved. If no string is entered, values are
            not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - '    ' (four spaces).
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - float_format '
                      + str(float_format) + ', delimiter ' + str(delimiter) + ', no_header ' + str(no_header))
        if not na_file:
            na_file = os.path.splitext(self.filename)[0] + '.na'

        # read dimensions and variables, try to check if ffi = 1001
        dim_list = self.get_dimension_list()
        var_list = self.get_variable_list()
        if len(dim_list) > 1:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - the actual convert_to_nasa_ames cant '
                              'process file with multiple dimensions, FFI is set to 1001')
            raise Exception('the actual convert_to_nasa_ames cant process file with multiple dimensions, '
                            'FFI is set to 1001')

        # create NASA/Ames dictionary
        f = egads.input.EgadsNasaAmes()
        na_dict = f.create_na_dict()
        missing_attributes = []
        
        # populate NLHEAD, FFI, ONAME, ORG, SNAME, MNAME, RDATE, DX, IVOL, NVOL
        nlhead, ffi, org, oname, sname, mname, dx = -999, 1001, '', '', '', '', 0.0
        ivol, nvol, date, niv = 1, 1, None, 0
        try:
            org = self.get_attribute_value('institution')
        except KeyError:
            org = 'no institution'
            missing_attributes.append('institution')
        try:
            oname = self.get_attribute_value('authors')
        except KeyError:
            try:
                oname = self.get_attribute_value('institution')
                missing_attributes.append('authors - replaced by institution')
            except KeyError:
                oname = 'no author'
                missing_attributes.append('authors')
        try:
            sname = self.get_attribute_value('source')
        except KeyError:
            sname = 'no source'
            missing_attributes.append('source')
        try:
            mname = self.get_attribute_value('title')
        except KeyError:
            mname = 'no title'
            missing_attributes.append('title')
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]

        # read and write independant variables and set DATE
        for ivar in dim_list:
            data = self.read_variable(ivar)
            f.write_variable(data, ivar, vartype='independant', na_dict=na_dict)
            niv += 1
            if 'time' in ivar:
                units = data.metadata['units']
                ref_time = None
                try:
                    index = units.index(' since ')
                    ref_time = units[index + 7:]
                except (KeyError, ValueError):
                    pass
                try:
                    ref_time = dateutil.parser.parse(ref_time).strftime("%Y%m%dT%H%M%S")
                    isotime = egads.algorithms.transforms.SecondsToIsotime().run(data, ref_time)
                    y, m, d, _, _, _ = egads.algorithms.transforms.IsotimeToElements().run(isotime)
                    date = [y.value[0], m.value[0], d.value[0]]
                    if not date:
                        date = [999, 999, 999]
                except Exception:
                    date = [999, 999, 999]

        # add first global metadata to na file
        f.write_attribute_value('NLHEAD', nlhead, na_dict=na_dict)
        f.write_attribute_value('FFI', ffi, na_dict=na_dict)
        f.write_attribute_value('ONAME', oname, na_dict=na_dict)
        f.write_attribute_value('ONAME', oname, na_dict=na_dict)
        f.write_attribute_value('ORG', org, na_dict=na_dict)
        f.write_attribute_value('SNAME', sname, na_dict=na_dict)
        f.write_attribute_value('MNAME', mname, na_dict=na_dict)
        f.write_attribute_value('DATE', date, na_dict=na_dict)
        f.write_attribute_value('RDATE', rdate, na_dict=na_dict)
        f.write_attribute_value('NIV', niv, na_dict=na_dict)
        f.write_attribute_value('DX', dx, na_dict=na_dict)
        f.write_attribute_value('NVOL', nvol, na_dict=na_dict)
        f.write_attribute_value('IVOL', ivol, na_dict=na_dict)

        # prepare and set NCOM and SCOM
        name_string = ''
        ncom = ['==== Normal Comments follow ====']
        ncom = ['The NA file has been converted from a NetCDF file by EGADS']
        for attr in self.get_attribute_list():
            if attr != 'institution' and attr != 'authors' and attr != 'source' and attr != 'title':
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
        ncom.append('==== Normal Comments end ====')
        ncom.append('=== Data Section begins on the next line ===')
        for name in dim_list:
            name_string += name + '    '
        scom = ['==== Special Comments follow ====',
                '=== Additional Variable Attributes defined in the source file ===',
                '== Variable attributes from source (NetCDF) file follow ==']
        for var in var_list:
            if var not in dim_list:
                data = self.read_variable(var)
                f.write_variable(data, var, na_dict=na_dict)
                first_line = True
                for metadata in data.metadata:
                    if metadata != '_FillValue' and metadata != 'scale_factor' and metadata != 'units' and metadata \
                            != 'var_name':
                        if first_line:
                            first_line = False
                            scom.append('  Variable ' + var + ':')
                        try:
                            scom.append('    ' + metadata + ' = ' + str(data.metadata[metadata]))
                        except TypeError:
                            logging.exception('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - an error '
                                              + 'occurred when trying to add variable metadata in SCOM - metadata '
                                              + str(metadata))
                name_string += var + '    '
        name_string = name_string[:-4]
        ncom.append(name_string)
        scom.append('== Variable attributes from source (NetCDF) file end ==')
        scom.append('==== Special Comments end ====')
        f.write_attribute_value('SCOM', scom, na_dict=na_dict)
        f.write_attribute_value('NCOM', ncom, na_dict=na_dict)
        f.write_attribute_value('NSCOML', len(scom), na_dict=na_dict)
        f.write_attribute_value('NNCOML', len(ncom), na_dict=na_dict)

        # write na file
        f.save_na_file(na_file, na_dict=na_dict, float_format=float_format, delimiter=delimiter, no_header=no_header)
        f.close()
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ' -> file conversion OK')
      
    def convert_to_csv(self, csv_file=None, float_format=None, no_header=False):
        """
        Converts currently open NetCDF file to CSV file using Nappy API.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        :param string float_format:
            Optional - The format of float numbers to be saved. If no string is entered, values are
            not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ', float_format ' + str(float_format) + ', no_header ' + str(no_header))
        if not csv_file:
            filename, _ = os.path.splitext(self.filename)
            csv_file = filename + '.csv'
        self.convert_to_nasa_ames(na_file=csv_file, float_format=float_format, delimiter=',', no_header=no_header)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ' -> file conversion OK')
    
    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.

        :param string filename:
            Name of NetCDF file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _open_file - filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            self.f = netCDF4.Dataset(filename, perms)
            self.filename = filename
            self.perms = perms
            attr_dict = self.get_attribute_list()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename)
        except RuntimeError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)
        except Exception:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")
        
    logging.info('egads - netcdf_io.py - EgadsNetCdf has been loaded')

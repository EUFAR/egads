__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 15:47"
__version__ = "1.27"
__all__ = ["NetCdf", "EgadsNetCdf"]

import logging
import netCDF4
import egads
import datetime
import operator
import os
import dateutil
import numpy
import collections
from egads.input import FileCore


class NetCdf(FileCore):
    """
    EGADS class for reading and writing to generic NetCDF files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python NetCDF4
    library to the EGADS file-access methods.
    """

    TYPE_DICT = {'char': 'c', 'byte': 'b', 'short': 'i2', 'int': 'i4', 'float': 'f4', 'double': 'f8', 'int16': 'i2',
                 'int32': 'i4', 'float32': 'f4', 'float64': 'f8', 'S1': 'S1', 'S2': 'S2'}

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
        either globally, or attached to a given variable or to a given group.

        :param string varname:
            Optional - Name of variable or group to get list of attributes from. If no
            variable name is provided, the function returns top-level NetCDF attributes.
        :return: dictionary of attributes.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - get_attribute_list - varname ' + str(varname))
        return self._get_attribute_list(varname)

    def get_attribute_value(self, attrname, varname=None):
        """
        Returns value of an attribute given its name. If a variable name or a group
        name is provided, the attribute is returned from the variable or the group
        specified, otherwise the global attribute is examined.

        :param string attrname:
            Name of attribute to examine
        :param string varname:
            Optional - Name of variable or group attribute is attached to. If none
            specified, global attributes are examined.
        :return: value of an attribute.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - get_attribute_value - attrname ' + str(attrname)
                      + ', varname ' + str(varname))
        attrs = self._get_attribute_list(varname)
        return attrs[attrname]

    def get_dimension_list(self, varname=None, group_walk=False, details=False):
        """
        Returns an ordered dictionary of dimensions and their sizes found in the current
        NetCDF file. If a variable name or a group name is provided, the dimension names
        and lengths associated with that variable or group are returned.

        :param string varname:
            Optional - Name of variable or group to get list of associated dimensions for.
            If no variable name is provided, the function returns all dimensions at the
            root of the NetCDF file.
        :param bool group_walk:
            Optional - if True, the function visits all groups (if at least one exists)
            to list all dimensions. False by default.
        :param bool details:
            Optional - if True, the dimension name is given with their respective path.
            False by default.
        :return: ordered dictionary of dimensions.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - get_dimension_list - varname ' + str(varname))
        return self._get_dimension_list(varname, group_walk, details)

    def get_variable_list(self, groupname=None, group_walk=False, details=False):
        """
        Returns a list of variables found in the current NetCDF file. if a groupname is
        provided, a list of variables found in the group is returned.

        :param string groupname:
            Optional - the name of the group to get the list from.
        :param bool group_walk:
            Optional - if True, the function visits all groups (if at least one exists)
            to list all variables. False by default.
        :param bool details:
            Optional - if True, the name of the variable is given with their respective path.
            False by default.
        :return: list of variables.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - get_variable_list')
        return self._get_variable_list(groupname, group_walk, details)

    def get_group_list(self, groupname=None, details=False):
        """
        Returns a list of groups found in the current NetCDF file.

        :param string groupname:
            Optional - the name of the group to get the list from. It should represent a path to
            the group. None by default.
        :param bool details:
            Optional - if details is True, the name of each group is given with their respective path.
            False by default.
        :return: list of groups.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - get_group_list')
        return self._get_group_list(groupname, details)

    def read_variable(self, varname, input_range=None, read_as_float=False, replace_fill_value=False):
        """
        Reads a variable from currently opened NetCDF file or from a group.

        :param string varname:
            Name of NetCDF variable to read in. If the variable is in a group, varname must include
            the path + the variable.
        :param vector input_range:
            Optional - Range of values in each dimension to input.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN,
            if one of those attributes exists in the NetCDF file.
            ``False`` is the default value.
        :return: variable as a numpy array.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - read_variable - varname ' + str(varname) + ', input_range '
                      + str(input_range))
        return self._read_variable(varname, input_range, read_as_float, replace_fill_value)

    def change_variable_name(self, varname, newname):
        """
        Change the variable name in currently opened NetCDF file or in a group.

        :param string varname:
            Name of variable to rename. If the variable is in a group, varname must include
            the path + the variable.
        :param string newname:
            The new name. The path of the group is not necessary here.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - change_variable_name - varname ' + str(varname)
                      + ', newname ' + str(newname))
        self._change_variable_name(varname, newname)

    def write_variable(self, data, varname, dims=None, ftype='double', fillvalue=None, scale_factor=None,
                       add_offset=None):
        """
        Writes/creates variable in currently opened NetCDF file.

        :param array|ndarray data:
            Array of values to output to NetCDF file.
        :param string varname:
            Name of variable to create/write to. If path to a group is in the name, the variable
            will be created/written in this group.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. If variable already exists
            in NetCDF file, this parameter is optional. For scalar variables, pass an empty tuple.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``,
            ``short``, ``char``, and ``byte``
        :param float fillvalue:
            Optional - Overrides default NetCDF _FillValue, if provided.
        :param float scale_factor:
            Optional - If data must be scaled, use this parameter.
        :param float add_offset:
            Optional - If an offset must be added to data, use this parameter.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - write_variable - varname ' + str(varname) +
                      ', dims ' + str(dims) + ', ftype ' + str(ftype) + ', fillvalue ' + str(fillvalue))
        self._write_variable(data, varname, dims, ftype, fillvalue, scale_factor, add_offset)

    def add_dim(self, name, size):
        """
        Adds dimension to currently open file or to a group.

        :param string name:
            Name of dimension to add. If path to a group is included, the dimension is
            added to the group.
        :param integer size:
            Integer size of dimension to add.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - add_dim - name ' + str(name) + ', size ' + str(size))
        self._add_dim(name, size)

    def add_attribute(self, attrname, value, objname=None):
        """
        Adds attribute to currently open file. If objname is included, attribute
        is added to specified variable or group, otherwise it is added to global
        file attributes.

        :param string attrname:
            Attribute name.
        :param string|float|int value:
            Value to assign to attribute name.
        :param string objname:
            Optional - If objname is provided, attribute name and value are added
            to specified variable or group in the Hdf file.
        """

        logging.debug('egads - hdf_io.py - Hdf - add_attribute - attrname ' + str(attrname) + ', varname '
                      + str(objname))
        self._add_attribute(attrname, value, objname)

    def add_group(self, groupname):
        """
        Adds group to currently open file.

        :param string groupname:
            Group name, or path + group name.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - add_group - groupname ' + str(groupname))
        self._add_group(groupname)

    def delete_attribute(self, attrname, varname=None):
        """
        Deletes attribute to currently open file. If varname is included, attribute
        is removed from specified variable or group, otherwise it is removed from global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string varname:
            Optional - If varname is provided, attribute removed from specified
            variable or group in the NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - delete_attribute - attrname ' + str(attrname) + 
                      ', varname ' + str(varname))
        self._delete_attribute(attrname, varname)

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
        self._convert_to_nasa_ames(na_file, float_format, delimiter, no_header)
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames -> file conversion OK')
      
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
        self._convert_to_nasa_ames(na_file=csv_file, float_format=float_format, delimiter=',', no_header=no_header)
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ' -> file conversion OK')

    def convert_to_hdf(self, hdf_file=None):
        """
        Convert currently open NetCDF file to Hdf5 file format.

        :param string hdf_file:
            Optional - Name of output Hdf5 file. If none is provided, name of
            current NetCDF file is used and suffix changed to .h5
        """

        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_hdf')
        self._convert_to_hdf(hdf_file)

    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.
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

    def _get_attribute_list(self, var):
        """
        Private method for getting attributes from a NetCDF file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_attribute_list - var ' + str(var))
        if self.f is not None:
            attr_dict = {}
            orig_group = self.f
            if var is not None:
                for group in var.rstrip('/').lstrip('/').split('/'):
                    orig_group = orig_group[group]
            for key, value in orig_group.__dict__.items():
                if isinstance(value, str):
                    value = ' '.join(value.split())
                attr_dict[key] = value
            return attr_dict
        else:
            logging.error('egads.input.NetCdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_dimension_list(self, var, group_walk, details):
        """
        Private method for getting list of dimension names and lengths. If
        variable name or group name is provided, method returns list of dimension
        names attached to specified variable or group, if none, returns all
        dimensions in the file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_dimension_list - var ' + str(var))
        dimdict = collections.OrderedDict()
        if self.f is not None:
            if var is None:
                if not group_walk:
                    for dimname, dimobj in reversed(sorted(self.f.dimensions.items())):
                        if details:
                            dimdict['/' + dimname] = len(dimobj)
                        else:
                            dimdict[dimname] = len(dimobj)
                else:
                    dim_list = []
                    for dimname, dimobj in reversed(sorted(self.f.dimensions.items())):
                        dim_list.append([dimname, len(dimobj), ''])
                    group_list = self.get_group_list(details=True)
                    for group_path in group_list:
                        orig_group = self.f
                        for item in group_path.lstrip('/').split('/'):
                            orig_group = orig_group[item]
                        if orig_group.dimensions:
                            for dimname, dimobj in reversed(sorted(orig_group.dimensions.items())):
                                dim_list.append([dimname, len(dimobj), group_path])
                    for dim in dim_list:
                        if details:
                            if not dim[2]:
                                dimdict['/' + dim[0]] = dim[1]
                            else:
                                dimdict[dim[2] + '/' + dim[0]] = dim[1]
                        else:
                            dimdict[dim[0]] = dim[1]
            else:
                orig_group = self.f
                dim_list = []
                var_name = ''
                group_path = ''
                for item in var.lstrip('/').rstrip('/').split('/'):
                    try:
                        if isinstance(orig_group[item], netCDF4.Group):
                            orig_group = orig_group[item]
                            group_path += '/' + item
                        else:
                            var_name = item
                            break
                    except IndexError:
                        var_name = item
                        break
                for dimname, dimobj in reversed(sorted(orig_group.dimensions.items())):
                    dim_list.append([dimname, len(dimobj), group_path])
                if group_walk:
                    group_list = self.get_group_list(group_path, details=True)
                    for group_path in group_list:
                        group = self.f
                        for item in group_path.lstrip('/').split('/'):
                            group = group[item]
                        if group.dimensions:
                            for dimname, dimobj in reversed(sorted(group.dimensions.items())):
                                dim_list.append([dimname, len(dimobj), group_path])
                if var_name:
                    for dimname in orig_group[var_name].dimensions:
                        idx = [sublist[0] for sublist in dim_list].index(dimname)
                        if details:
                            dimdict[dim_list[idx][2] + '/' + dim_list[idx][0]] = dim_list[idx][1]
                        else:
                            dimdict[dim_list[idx][0]] = dim_list[idx][1]
                else:
                    for sublist in dim_list:
                        if details:
                            dimdict[sublist[2] + '/' + sublist[0]] = sublist[1]
                        else:
                            dimdict[sublist[0]] = sublist[1]
            return dimdict
        else:
            logging.error('egads.input.NetCdf._get_dimension_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_variable_list(self, groupname, group_walk, details):
        """
        Private method for getting list of variable names associated to a file or to group.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_variable_list')
        if self.f is not None:

            def set_folder(grouppath, base_group):
                for item in grouppath.lstrip('/').rstrip('/').split('/'):
                    base_group = base_group.groups[item]
                return base_group

            if groupname is not None:
                if groupname[0] != '/':
                    groupname = '/' + groupname
                orig_group = set_folder(groupname, self.f)
            else:
                orig_group = self.f
            if group_walk:
                var_list = []
                if details:
                    for var in list(orig_group.variables.keys()):
                        if groupname is not None:
                            var_list.append(groupname + '/' + var)
                        else:
                            var_list.append('/' + var)
                else:
                    var_list = var_list + list(orig_group.variables.keys())
                group_list = self.get_group_list(groupname, True)
                for path in group_list:
                    group_obj = set_folder(path, self.f)
                    if list(group_obj.variables.keys()):
                        if details:
                            for var in list(group_obj.variables.keys()):
                                var_list.append(path + '/' + var)
                        else:
                            var_list = var_list + list(group_obj.variables.keys())
                return var_list
            else:
                var_list = []
                if details:
                    for var in list(orig_group.variables.keys()):
                        if groupname is not None:
                            if groupname != '/':
                                var_list.append(groupname + '/' + var)
                            else:
                                var_list.append(groupname + var)
                        else:
                            var_list.append('/' + var)
                else:
                    var_list = var_list + list(orig_group.variables.keys())
                return var_list
        else:
            logging.error('egads.input.NetCdf._get_variable_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_group_list(self, groupname, details):
        """
        Private method for getting list of group names.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_group_list')
        if self.f is not None:
            orig_group = self.f
            group_list = []
            if groupname is not None:
                for group in groupname.rstrip('/').lstrip('/').split('/'):
                    orig_group = orig_group.groups[group]

            def _walktree(orig):
                groups = orig.groups
                for _, obj in groups.items():
                    if details:
                        group_list.append(obj.path)
                    else:
                        group_list.append(obj.name)
                    _walktree(obj)

            _walktree(orig_group)
            return group_list
        else:
            logging.error('egads.input.NetCdf._get_group_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _add_group(self, groupname):
        """
        Private method for adding a group.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _add_group')
        if self.f is not None:
            if groupname[0] != '/':
                groupname = '/' + groupname
            self.f.createGroup(groupname)
        else:
            logging.error('egads.input.NetCdf._add_group: AttributeError, No file open')
            raise AttributeError('No file open')

    def _add_dim(self, name, size):
        """
        Private method to add dimension to currently open file or to a group.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _add_dim')
        if self.f is not None:
            orig_group = self.f
            for group in name.rstrip('/').lstrip('/').split('/'):
                try:
                    if isinstance(orig_group[group], netCDF4.Group):
                        orig_group = orig_group[group]
                    else:
                        name = group
                except IndexError:
                    name = group
            orig_group.createDimension(name, size)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - add_dim - name ' + str(name) + ' -> dim add OK')

    def _add_attribute(self, attrname, value, varname):
        """
        Private method to add attribute to currently open file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _add_attribute')
        if self.f is not None:
            orig_group = self.f
            if isinstance(value, list):
                tmp = ''
                for item in value:
                    tmp += item + ', '
                value = tmp[:-2]
            if varname is not None:
                for group in varname.rstrip('/').lstrip('/').split('/'):
                    orig_group = orig_group[group]
            setattr(orig_group, attrname, value)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _add_attribute - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - _add_attribute - attrname ' + str(attrname)
                      + ' -> attribute add OK')

    def _delete_attribute(self, attrname, varname):
        """
        Private method to delete attribute in currently open file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _delete_attribute')
        if self.f is not None:
            orig_group = self.f
            if varname is not None:
                for group in varname.rstrip('/').lstrip('/').split('/'):
                    orig_group = orig_group[group]
            delattr(orig_group, attrname)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _delete_attribute - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - _delete_attribute - attrname ' + str(attrname)
                      + ' -> attribute delete OK')

    def _change_variable_name(self, varname, newname):
        """
        Private method to change the variable name in currently opened NetCDF file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _change_variable_name')
        if self.f is not None:
            orig_group = self.f
            for group in varname.rstrip('/').lstrip('/').split('/'):
                if isinstance(orig_group[group], netCDF4.Group):
                    orig_group = orig_group[group]
                else:
                    varname = group
            orig_group.renameVariable(varname, newname)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - .change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')

    def _read_variable(self, varname, input_range, read_as_float, replace_fill_value):
        """
        Private method to read a variable from currently opened NetCDF file or from a group.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _read_variable')
        try:
            orig_group = self.f
            for group in varname.lstrip('/').split('/'):
                orig_group = orig_group[group]
            varin = orig_group
        except (KeyError, IndexError):
            logging.exception('egads - netcdf_io.py - NetCdf - read_variable - KeyError, variable does not exist in '
                              'netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        if input_range is None:
            value = varin[:]
            if read_as_float:
                value = [float(item) for item in value]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in range(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        value = numpy.array(value)
        if read_as_float:
            value = value.astype('float')
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

    def _write_variable(self, data, varname, dims, ftype, fillvalue, scale_factor, add_offset):
        """
        Private method to write/create variable in currently opened NetCDF file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _write_variable')
        if self.f is not None:
            orig_group = self.f
            varname = varname.rstrip('/')
            if '/' in varname.lstrip('/'):
                var = varname.split('/')
                for group in var:
                    try:
                        orig_group = orig_group.groups[group]
                    except KeyError:
                        varname = group
            try:
                varout = orig_group.createVariable(varname, self.TYPE_DICT[ftype], dims, fill_value=fillvalue)
            except KeyError:
                varout = orig_group.createVariable(varname, ftype, dims, fill_value=fillvalue)

            if scale_factor is not None:
                setattr(varout, 'scale_factor', scale_factor)
            if add_offset is not None:
                setattr(varout, 'add_offset', add_offset)

            varout[:] = data
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _write_variable - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - _write_variable - varname ' + str(varname) + ' -> data write OK')

    def _convert_to_nasa_ames(self, na_file, float_format, delimiter, no_header):
        """
        Private method to convert currently open NetCDF file to one or more NASA Ames files.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _convert_to_nasa_ames')

        if not na_file:
            na_file = os.path.splitext(self.filename)[0] + '.na'

        # read dimensions and variables, try to check if ffi = 1001
        dim_list = self.get_dimension_list()
        var_list = self.get_variable_list()

        if len(dim_list) > 1:
            logging.exception('egads - netcdf_io.py - NetCdf - the actual convert_to_nasa_ames cant '
                              'process file with multiple dimensions, FFI is set to 1001')
            raise Exception('the actual convert_to_nasa_ames cant process file with multiple dimensions, '
                            'FFI is set to 1001')
        elif len(dim_list) == 0:
            logging.exception('egads - netcdf_io.py - NetCdf - there is no dimensions at the root of '
                              'the opened netcdf file.')
            raise Exception('there is no dimensions at the root of the opened netcdf file.')

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
        ncom = ['==== Normal Comments follow ====', 'The NA file has been converted from a NetCDF file by EGADS']
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
                            logging.exception('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames - an error '
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

    def _convert_to_hdf(self, hdf_file):
        """
        Private method to convert currently open NetCDF file to Hdf5 file format.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _convert_to_hdf')
        if self.f is not None:
            if hdf_file is None:
                hdf_file = os.path.splitext(self.filename)[0] + '.h5'

            # get groups
            group_list = self.get_group_list(details=True)

            # get global attributes
            global_attributes = self.get_attribute_list()

            # get dimensions
            dimension_list = self.get_dimension_list(group_walk=True, details=True)

            # get variables
            variable_list = self.get_variable_list(group_walk=True, details=True)
            var_dim_list = {}
            for path in variable_list:
                var_dim_list[path] = self.get_dimension_list(path)

            # get variables and groups attributes
            variable_attributes = {}
            group_attributes = {}
            for path in variable_list:
                variable_attributes[path] = self.get_attribute_list(varname=path)
            for path in group_list:
                group_attributes[path] = self.get_attribute_list(varname=path)

            # create hdf file
            f = egads.input.Hdf(hdf_file, 'w')

            # add global attributes
            add_history = False
            dt = datetime.datetime.now()
            for key, value in global_attributes.items():
                if key == 'history':
                    add_history = True
                    value += ' ; converted to Hdf by EGADS, ' + str(dt)
                f.add_attribute(key, value)
            if not add_history:
                f.add_attribute('history', 'converted to Hdf by EGADS, ' + str(dt))

            # add groups
            for path in group_list:
                f.add_group(path)

            # add dimensions
            dim_list = []
            for dim_path, _ in dimension_list.items():
                dim_list.append(dim_path)
                data = self.read_variable(dim_path)
                ftype = str(data.dtype)
                f.add_dim(dim_path, data, ftype)

            # add variables
            for full_var in variable_list:
                if full_var not in dim_list:
                    data = self.read_variable(full_var)
                    dims = tuple([key for key, _ in var_dim_list[full_var].items()])
                    ftype = str(data.dtype)
                    f.write_variable(data, full_var, dims, ftype)

            # add variables and groups attributes
            for var, metadata in variable_attributes.items():
                if metadata:
                    for attr_name, attr_value in metadata.items():
                        f.add_attribute(attr_name, attr_value, var)
            for group, metadata in group_attributes.items():
                if metadata:
                    for attr_name, attr_value in metadata.items():
                        f.add_attribute(attr_name, attr_value, group)

            f.close()
            logging.debug('egads - netcdf_io.py - NetCdf - _convert_to_hdf -> file conversion OK')
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _convert_to_hdf - AttributeError, no file open')
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
        Reads in a variable from currently opened NetCDF file or from a group, and maps the NetCDF
        attributes to an :class:`~egads.core.EgadsData` instance.

        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input. ``None`` is the default value.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file. ``False`` is the default value.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN.
            False is the default value.
        :return: variable in a EgadsData instance.
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname) +
                      ', input_range ' + str(input_range))
        return self._read_variable(varname, input_range, read_as_float, replace_fill_value)

    def write_variable(self, data, varname=None, dims=None, ftype='double'):
        """
        Writes/creates variable in currently opened NetCDF file.

        :param EgadsData data:
            Instance of EgadsData object to write out to file.
            All data and attributes will be written out to the file.
        :param string varname:
            Optional - Name of variable to create/write to. If no varname is provided,
            and if cdf_name attribute in EgadsData object is defined, then the variable will be
            written to cdf_name. If path to a group is in varname, the variable will be
            created in this group. In that case, varname is mandatory as the function will
            not take into account path in varname metadata of the EgadsData instance.
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
        self._write_variable(data, varname, dims, ftype)

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
        self._convert_to_nasa_ames(na_file, float_format, delimiter, no_header)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames -> file conversion OK')

    def convert_to_csv(self, csv_file=None, float_format=None, no_header=False):
        """
        Converts currently open NetCDF file to Nasa Ames CSV file.

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

    def convert_to_hdf(self, hdf_file=None):
        """
        Convert currently open NetCDF file to Hdf5 file format.

        :param string hdf_file:
            Optional - Name of output Hdf5 file. If none is provided, name of
            current NetCDF file is used and suffix changed to .h5
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_hdf')
        self._convert_to_hdf(hdf_file)

    def _convert_to_nasa_ames(self, na_file, float_format, delimiter, no_header):
        """
        Private method to convert currently open EGADS NetCDF file to one or more NASA
        Ames files. For now can only process NetCdf files to NASA/Ames FFI 1001:
        variables can only be dependant to one independant variable at a time.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _convert_to_nasa_ames')
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
        ncom = ['==== Normal Comments follow ====', 'The NA file has been converted from a NetCDF file by EGADS']
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
    
    def _open_file(self, filename, perms):
        """
        Private method for opening NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _open_file')
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

    def _read_variable(self, varname, input_range, read_as_float, replace_fill_value):
        """
        Private method to read in a variable from currently opened NetCDF file or from a group,
        and maps the NetCDF attributes to an :class:`~egads.core.EgadsData` instance.

        :param string varname:
            Name of NetCDF variable to read in. If path to a group is in varname, the variable is
            read in the group.
        :param vector input_range:
            Optional - Range of values in each dimension to input. ``None`` is the default value.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file. ``False`` is the default value.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN.
            False is the default value.
        :return: variable in a EgadsData instance.
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _read_variable')
        try:
            orig_group = self.f
            for group in varname.lstrip('/').split('/'):
                orig_group = orig_group[group]
            varin = orig_group
        except KeyError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _read_variable - KeyError, variable does not exist'
                              ' in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in range(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        variable_attrs = self.get_attribute_list(varname)
        value = numpy.array(value)
        if read_as_float:
            value = value.astype('float')
        if replace_fill_value:
            if '_FillValue' in variable_attrs.keys():
                _fill_value = variable_attrs['_FillValue']
                value[value == _fill_value] = numpy.nan
            else:
                if 'missing_value' in variable_attrs.keys():
                    _fill_value = variable_attrs['missing_value']
                    value[value == _fill_value] = numpy.nan
                else:
                    logging.warning('egads - netcdf_io.py - EgadsNetCdf - _read_variable - varname ' + str(varname)
                                    + ', no _FillValue or missing_value attribute found. Fill value not replaced by '
                                    + 'NaN.')
        variable_metadata = egads.core.metadata.VariableMetadata(variable_attrs, self.file_metadata)
        data = egads.EgadsData(value, variable_metadata=variable_metadata)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _read_variable - varname ' + str(varname)
                      + ' -> data read OK')
        return data

    def _write_variable(self, data, varname, dims, ftype):
        """
        Private method to write/create variable in currently opened NetCDF file or in group.
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _write_variable')
        fillvalue = None
        if self.f is not None:
            orig_group = self.f
            if varname is not None:
                varname = varname.lstrip('/').rstrip('/')
                if '/' in varname:
                    var = varname.split('/')
                    for group in var:
                        try:
                            orig_group = orig_group.groups[group]
                        except KeyError:
                            varname = group
            try:
                varout = orig_group.variables[varname]
            except KeyError:
                try:
                    fillvalue = data.metadata['_FillValue']
                except KeyError:
                    try:
                        fillvalue = data.metadata['missing_value']
                    except KeyError:
                        pass

                varout = orig_group.createVariable(varname, self.TYPE_DICT[ftype], dims, fill_value=fillvalue)

            for key, val in data.metadata.items():
                if key != '_FillValue':
                    if isinstance(val, list):
                        tmp = ''
                        for item in val:
                            tmp += item + ', '
                        setattr(varout, str(key), tmp[:-2])
                    else:
                        setattr(varout, str(key), val)

            if fillvalue is not None:
                varout[:] = numpy.where(numpy.isnan(data.value), fillvalue, data.value)
            else:
                varout[:] = data.value

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - _write_variable - varname ' + str(varname)
                      + ' -> data write OK')

    def _convert_to_hdf(self, hdf_file):
        """
        Private method to convert currently open NetCDF file to Hdf5 file format.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _convert_to_hdf')
        if self.f is not None:
            if hdf_file is None:
                hdf_file = os.path.splitext(self.filename)[0] + '.h5'

            # get groups
            group_list = self.get_group_list(details=True)

            # get global attributes
            global_attributes = self.get_attribute_list()

            # get dimensions
            dimension_list = self.get_dimension_list(group_walk=True, details=True)

            # get variables
            variable_list = self.get_variable_list(group_walk=True, details=True)
            var_dim_list = {}
            for full_var in variable_list:
                var_dim_list[full_var] = self.get_dimension_list(full_var)

            # get groups attributes
            group_attributes = {}
            for path in group_list:
                group_attributes[path] = self.get_attribute_list(varname=path)

            # create hdf file
            f = egads.input.EgadsHdf(hdf_file, 'w')

            # add global attributes
            add_history = False
            dt = datetime.datetime.now()
            for key, value in global_attributes.items():
                if key == 'history':
                    add_history = True
                    value += ' ; converted to Hdf by EGADS, ' + str(dt)
                f.add_attribute(key, value)
            if not add_history:
                f.add_attribute('history', 'converted to Hdf by EGADS, ' + str(dt))

            # add groups
            for path in group_list:
                f.add_group(path)
                metadata = group_attributes[path]
                if metadata:
                    for attr_name, attr_value in metadata.items():
                        f.add_attribute(attr_name, attr_value, path)

            # add dimensions
            dim_list = []
            for dim_path, dim_size in dimension_list.items():
                dim_list.append(dim_path)
                data = self.read_variable(dim_path)
                f.add_dim(dim_path, data, str(data.dtype))

            # add variables
            for path in variable_list:
                if path not in dim_list:
                    data = self.read_variable(path)
                    dims = tuple([key for key, _ in var_dim_list[path].items()])
                    ftype = str(data.dtype)
                    f.write_variable(data, path, dims, ftype)

            f.close()
            logging.debug('egads - netcdf_io.py - EgadsNetCdf - _convert_to_hdf -> file conversion OK')
        else:
            logging.error('egads - netcdf_io.py - EgadsNetCdf - _convert_to_hdf - AttributeError, no file open')
            raise AttributeError('No file open')

    logging.info('egads - netcdf_io.py - EgadsNetCdf has been loaded')

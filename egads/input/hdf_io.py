__author__ = "ohenry"
__date__ = "2019-11-22 07:09"
__version__ = "1.2"
__all__ = ["Hdf", "EgadsHdf"]


import logging
import h5py
import collections
import itertools
import numpy
import egads
import os
import datetime
from egads.input import FileCore


class Hdf(FileCore):
    """
    EGADS class for reading and writing to generic Hdf5 files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python h5py
    library to the EGADS file-access methods.
    """

    TYPE_DICT = {'char': 'c', 'byte': 'b', 'short': 'i2', 'int': 'i4', 'float': 'f4', 'double': 'f8', 'int16': 'i2',
                 'int32': 'i4', 'float32': 'f4', 'float64': 'f8'}

    def __del__(self):
        """
        If Hdf5 file is still open on deletion of object, close it.
        """

        if self.f is not None:
            self.f.close()

    def open(self, filename, perms=None):
        """
        Opens Hdf5 file given filename.

        :param string filename:
            Name of Hdf5 file to open.
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write
            (overwrites data in file), ``a`` and ``r+`` for append, and ``r`` for
            read. ``r`` is the default value
        """

        logging.debug('egads - hdf_io.py - Hdf - open')
        FileCore.open(self, filename, perms)

    def get_file_structure(self, from_group=None):
        """
        Returns a view of the file structure, groups and datasets.

        :param str from_group:
            if from_group is provided, returs file structure from the group from_group.
        :return: file structure.
        """

        return self._get_file_structure(from_group=from_group)

    def get_group_list(self, groupname=None, details=False):
        """
        Returns a list of groups found in the current Hdf file.

        :param string groupname:
            Optional - the name of the group to get the list from. It should represent a path to
            the group. None by default.
        :param bool details:
            If details is true, it will return a list of all groups in the Hdf file, or from
            groupname if groupname is not None, and their path. In that case, each element of
            the list is a small dict containing as key/value the name of the group and the path
            of the group in the file. False by default.
        :return: list of groups.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_group_list')
        return self._get_group_list(groupname, details)

    def get_variable_list(self, groupname=None, group_walk=False, details=False):
        """
        Returns a list of variables found in the current Hdf file.

        :param string groupname:
            Optional - the name of the group to get the list from.
        :param bool group_walk:
            Optional - if True, the function visits all groups (if at least one exists)
            to list all variables. False by default.
        :param bool details:
            Optional - if True, the function returns a list of dictionaries, with
            variable name as key and variable path as value. False by default, returns a
            list of string.
        :return: list of variables.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_variable_list')
        return self._get_variable_list(groupname, group_walk, details)

    def get_attribute_list(self, objectname=None):
        """
        Returns a dictionary of attributes and values found in current Hdf file
        either globally, or attached to a given object, Group or Dataset.

        :param string objectname:
            Optional - Name of object to get list of attributes from. If no object name is
            provided, the function returns top-level Hdf attributes.
        :return: list of attribute.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_attribute_list - objectname ' + str(objectname))
        return self._get_attribute_list(objectname)

    def get_attribute_value(self, attrname, objectname=None):
        """
        Returns value of an attribute given its name. If an object name is provided,
        the attribute is returned from the object specified, otherwise the global
        attribute is examined.

        :param string attrname:
            Name of attribute to examine
        :param string objectname:
            Optional - Name of object attribute is attached to. If none specified, global
            attributes are examined.
        :return: attribute value.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_attribute_value - attrname ' + str(attrname)
                      + ', varname ' + str(objectname))
        attrs = self._get_attribute_list(objectname)
        return attrs[attrname]

    def get_dimension_list(self, varname=None, group_walk=False, details=False):
        """
        Returns an ordered dictionary of dimensions and their sizes found in the current
        Hdf file. If an object name is provided, the dimension names and lengths associated
        with that object are returned.

        :param string varname:
            Name of variable or group to get list of associated dimensions for. If no variable
            name is provided, the function returns all dimensions at the root of the Hdf file.
        :param bool group_walk:
            Optional - if True, the function visits all groups (if at least one exists)
            to list all dimensions. False by default.
        :param bool details:
            Optional - if True, dimension path is provided in the dictionary. False by default.
        :return: list of dimension.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_dimension_list - varname ' + str(varname))
        return self._get_dimension_list(varname, group_walk, details)

    def read_variable(self, varname, input_range=None, read_as_float=False, replace_fill_value=False):
        """
        Reads a variable from currently opened Hdf file.

        :param string varname:
            Name of Hdf variable to read in. Can include a path to the variable.
        :param vector input_range:
            Optional - Range of values in each dimension to input.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN,
            if one of those attributes exists in the Hdf file. False is the default value.
        :return: variable.
        """

        logging.debug('egads - hdf_io.py - Hdf - read_variable - varname ' + str(varname) + ', input_range '
                      + str(input_range))
        return self._read_variable(varname, input_range, read_as_float, replace_fill_value)

    def add_group(self, groupname):
        """
        Adds group to currently open file.

        :param string|list groupname:
            Group name, or path name, or sequence of groups.
        """

        logging.debug('egads - hdf_io.py - Hdf - add_group - groupname ' + str(groupname))
        self._add_group(groupname)

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

    def add_dim(self, name, data, ftype='double'):
        """
        Adds dimension to currently open file or to a group.

        :param string name:
            Name of dimension to add, it can includes a path to the group where to add
            the dimension.
        :param data:
            A numpy array or ndarray containing values of the dimension, dimensions are considered
            as datasets.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. Options
            for type are ``double``, ``float``, ``int``, ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - hdf_io.py - Hdf - add_dim - name ' + str(name))
        self._add_dim(name, data, ftype)

    def write_variable(self, data, varname, dims=None, ftype='double'):
        """
        Writes/creates variable in currently opened Hdf file.

        :param array|ndarray data:
            Array of values to output to Hdf file.
        :param string varname:
            Name of variable to create/write to. If path to a group is in the name, the variable
            will be created/written in this group.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. Dimensions should be present
            in the group where the variable is stored. No path is required in dimension name.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``.Options for type
            are ``double``, ``float``, ``int``, ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - hdf_io.py - Hdf - write_variable - varname ' + str(varname) +
                      ', dims ' + str(dims) + ', ftype ' + str(ftype))
        self._write_variable(data, varname, dims, ftype)

    def delete_attribute(self, attrname, objectname=None):
        """
        Deletes attribute to currently open file. If objectname is included, attribute
        is removed from specified variable or group, otherwise it is removed from global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string objectname:
            Optional - If objectname is provided, attribute removed from specified
            variable or group in the Hdf file.
        """

        logging.debug('egads - hdf_io.py - Hdf - delete_attribute - attrname ' + str(attrname) +
                      ', objectname ' + str(objectname))
        self._delete_attribute(attrname, objectname)

    def delete_group(self, groupname):
        """
        Deletes group in currently open file.

        :param string groupname:
            Group name.
        """

        logging.debug('egads - hdf_io.py - Hdf - delete_group - groupname ' + str(groupname))
        self._delete_group(groupname)

    def delete_variable(self, varname):
        """
        Deletes group in currently open file.

        :param string varname:
            Variable name.
        """

        logging.debug('egads - hdf_io.py - Hdf - delete_variable - varname ' + str(varname))
        self._delete_variable(varname)

    def convert_to_netcdf(self, filename=None):
        """
        Converts the opened Hdf file to NetCdf format following the EUFAR and EGADS
        convention. If groups exist, they are preserved in the new NetCDF file.

        :param string filename:
            Optional - if only a name is given, a NetCDF file named ``filename`` is
            created in the HDF file folder ; if a path and a name are given, a NetCDF
            file named ``name`` is created in the folder ``path``.
        """

        logging.debug('egads - hdf_io.py - Hdf - convert_to_netcdf - filename ' + str(filename))
        self._convert_to_netcdf(filename)

    def convert_to_nasa_ames(self, na_file=None, float_format=None, delimiter='    ', no_header=False):
        """
        Convert currently open Hdf file to one or more NASA Ames files.
        For now can only process Hdf files to NASA/Ames FFI 1001 :
        only time as an independant variable. If groups exist, they are not converted to NA file.

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

        logging.debug('egads - hdf_io.py - Hdf - convert_to_nasa_ames - float_format ' + str(float_format)
                      + ', delimiter ' + str(delimiter) + ', no_header ' + str(no_header))
        self._convert_to_nasa_ames(na_file, float_format, delimiter, no_header)

    def convert_to_csv(self, csv_file=None, float_format=None, no_header=False):
        """
        Converts currently open Hdf file to CSV file using the NasaAmes class.

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

        logging.debug('egads - hdf_io.py - Hdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ', float_format ' + str(float_format) + ', no_header ' + str(no_header))
        if not csv_file:
            csv_file = os.path.splitext(self.filename)[0] + '.csv'
        self._convert_to_nasa_ames(na_file=csv_file, float_format=float_format, delimiter=',', no_header=no_header)

    def _open_file(self, filename, perms):
        """
        Private method for opening Hdf5 file.

        :param string filename:
            Name of Hdf5 file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        logging.debug('egads - hdf_io.py - Hdf - _open_file')
        self.close()
        try:
            self.f = h5py.File(filename, perms)
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            logging.exception('egads - hdf_io.py - Hdf - _open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - hdf_io.py - Hdf - _open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)
        except Exception:
            logging.exception('egads - hdf_io.py - Hdf - _open_file - Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

    def _get_file_structure(self, from_group):
        """
        Private method for getting a view of the file structure, groups and datasets.
        """

        logging.debug('egads - hdf_io.py - Hdf - _get_file_structure')
        file_structure = collections.OrderedDict()

        def _h5py_get_file_structure(name, obj):
            file_structure[name] = {'object': obj, 'type': type(obj)}

        if from_group is None:
            self.f.visititems(_h5py_get_file_structure)
        else:
            self.f[from_group].visititems(_h5py_get_file_structure)
        return file_structure

    def _get_group_list(self, groupname, details):
        """
        Private method for getting list of group names.
        """

        logging.debug('egads - hdf_io.py - Hdf - _get_group_list')
        if self.f is not None:
            group_list = []
            for key, value in self._get_file_structure(from_group=groupname).items():
                if isinstance(value['object'], h5py.Group):
                    if details:
                        group_list.append('/' + key)
                    else:
                        group_list.append(os.path.basename(key))
            return group_list
        else:
            logging.error('egads.input.Hdf._get_group_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_variable_list(self, groupname, group_walk, details):
        """
        Private method for getting list of dataset names.
        """

        logging.debug('egads - hdf_io.py - Hdf - _get_variable_list')
        if self.f is not None:
            orig_group = self.f
            if groupname is not None:
                groupname = groupname.rstrip('/')
                if groupname[0] != '/':
                    groupname = '/' + groupname
                orig_group = orig_group[groupname]
            else:
                groupname = ''
            var_list = []

            def _h5py_get_file_structure(name, obj):
                if isinstance(obj, h5py.Dataset):
                    var_path, var_name = os.path.split(name)
                    if details:
                        if var_path:
                            var_path = groupname + '/' + var_path + '/'
                        else:
                            var_path = groupname + '/'
                        var_list.append(var_path + var_name)
                    else:
                        var_list.append(var_name)

            if group_walk:
                orig_group.visititems(_h5py_get_file_structure)
            else:
                for name in orig_group:
                    if isinstance(orig_group[name], h5py.Dataset):
                        if details:
                            var_list.append(groupname + '/' + name)
                        else:
                            var_list.append(name)
            return var_list
        else:
            logging.error('egads.input.Hdf._get_variable_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_attribute_list(self, obj=None):
        """
        Private method for getting attributes from a Hdf file. Gets global
        attributes if no object name is provided, otherwise gets attributes
        attached to specified object. Function returns dictionary of values.
        If multiple white spaces exist, they are removed.
        """

        logging.debug('egads - netcdf_io.py - Hdf - _get_attribute_list')
        if self.f is not None:
            attr_dict = {}
            orig_group = self.f
            if obj is not None:
                orig_group = orig_group[obj]
            for key, value in orig_group.attrs.items():
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                if isinstance(value, str):
                    value = ' '.join(value.split())
                attr_dict[key] = value
            return attr_dict
        else:
            logging.error('egads.input.Hdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_dimension_list(self, varname, group_walk, details):
        """
        Private method to get an ordered dictionary of dimensions and their sizes found in the current
        Hdf file.
        """

        dim_dict = collections.OrderedDict()
        orig_group = self.f
        if group_walk:
            if varname is None:
                var_list = self.get_variable_list(group_walk=True, details=True)
                dim_list = []
                for var_path in var_list:
                    for dim in orig_group[var_path].dims:
                        dim_path = os.path.dirname(var_path)
                        dim_list.append([dim.label, orig_group[dim_path + '/' + dim.label].shape[0], dim_path])
                for dim in [list(x) for x in set(tuple(x) for x in dim_list)]:
                    if details:
                        if dim[2] == '/':
                            dim_dict['/' + dim[0]] = dim[1]
                        else:
                            dim_dict[dim[2] + '/' + dim[0]] = dim[1]
                    else:
                        dim_dict[dim[0]] = dim[1]
            else:
                var = orig_group[varname]
                if isinstance(var, h5py.Dataset):
                    parent = var.parent.name
                    dim_shape = var.shape
                    for i, dim in enumerate(orig_group[varname].dims):
                        if details:
                            dim_dict[parent + dim.label] = dim_shape[i]
                        else:
                            dim_dict[dim.label] = dim_shape[i]
                else:
                    var_list = self.get_variable_list(groupname=varname, group_walk=True, details=True)
                    dim_list = []
                    for var_path in var_list:
                        dim_path = os.path.dirname(var_path)
                        for dim in orig_group[var_path].dims:
                            dim_list.append([dim.label, orig_group[dim_path + '/' + dim.label].shape[0], dim_path])
                    for dim in [list(x) for x in set(tuple(x) for x in dim_list)]:
                        if details:
                            dim_dict[dim[2] + '/' + dim[0]] = dim[1]
                        else:
                            dim_dict[dim[0]] = dim[1]
        else:
            if varname is None:
                var_list = self.get_variable_list()
                dim_list = []
                for item in var_list:
                    for dim in orig_group[item].dims:
                        dim_list.append([dim.label, orig_group[dim.label].shape[0]])
                for dim in [sublist for sublist, _ in itertools.groupby(dim_list)]:
                    if details:
                        dim_dict['/' + dim[0]] = dim[1]
                    else:
                        dim_dict[dim[0]] = dim[1]
            else:
                var = orig_group[varname]
                if isinstance(var, h5py.Dataset):
                    parent = var.parent.name
                    dim_shape = var.shape
                    for i, dim in enumerate(orig_group[varname].dims):
                        if details:
                            if parent != '/':
                                dim_dict[parent + '/' + dim.label] = dim_shape[i]
                            else:
                                dim_dict['/' + dim.label] = dim_shape[i]
                        else:
                            dim_dict[dim.label] = dim_shape[i]
                else:
                    var_list = self.get_variable_list(groupname=varname)
                    dim_list = []
                    for item in var_list:
                        for dim in var[item].dims:
                            dim_list.append([dim.label, var[dim.label].shape[0]])
                    for dim in [sublist for sublist, _ in itertools.groupby(dim_list)]:
                        if details:
                            if varname[0] != '/':
                                varname = '/' + varname
                            dim_dict[varname + '/' + dim[0]] = dim[1]
                        else:
                            dim_dict[dim[0]] = dim[1]
        return dim_dict

    def _read_variable(self, varname, input_range, read_as_float, replace_fill_value):
        """
        Private method to read a variable from currently opened Hdf file.
        """
        try:
            if input_range is None:
                var = numpy.array(self.f[varname])
            else:
                obj = 'slice(input_range[0], input_range[1])'
                for i in range(2, len(input_range), 2):
                    obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
                var = numpy.array(self.f[varname][eval(obj)])
        except KeyError:
            logging.exception('egads - hdf_io.py - Hdf - _read_variable - KeyError, variable does not exist in '
                              'hdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        if read_as_float:
            var = var.astype(float)
        if replace_fill_value:
            _fill_value = None
            var_attrs = self._get_attribute_list(varname)
            if '_FillValue' in var_attrs:
                _fill_value = var_attrs['_FillValue']
                var[var == _fill_value] = numpy.nan
            elif 'missing_value' in var_attrs:
                _fill_value = var_attrs['missing_value']
                var[var == _fill_value] = numpy.nan
            elif 'fill_value' in var_attrs:
                _fill_value = var_attrs['fill_value']
                var[var == _fill_value] = numpy.nan
            else:
                logging.warning('egads - hdf_io.py - Hdf - _read_variable - KeyError, no missing value '
                                + 'attribute has been found for the variable ' + varname + '. Missing value not '
                                + 'replaced by NaN.')
        logging.debug('egads - hdf_io.py - Hdf - _read_variable - varname ' + str(varname) + ' -> data read OK')
        return var

    def _add_group(self, groupname):
        """
        Private method to Add group to currently open file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _add_group')
        if self.f is not None:
            self.f.create_group(groupname)
        else:
            logging.error('egads.input.Hdf._add_group: AttributeError, No file open')
            raise AttributeError('No file open')

    def _add_attribute(self, attrname, value, objname):
        """
        Private method to add attribute to currently open file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _add_attribute')
        if self.f is not None:
            if objname is not None:
                self.f[objname].attrs.create(attrname, value)
            else:
                self.f.attrs.create(attrname, value)
        else:
            logging.error('egads - hdf_io.py - Hdf - _add_attribute - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - Hdf - _add_attribute - attrname ' + str(attrname)
                      + ' -> attribute add OK')

    def _add_dim(self, name, data, ftype):
        """
        Private method to add dimension to currently open file or group.
        """

        logging.debug('egads - hdf_io.py - Hdf - _add_dim')
        if self.f is not None:
            dtype = self.TYPE_DICT[ftype]
            self.f.create_dataset(name, data=data, dtype=dtype)
            self.f[name].make_scale(name)
            self.f[name].dims[0].label = os.path.split(name)[1]
        else:
            logging.error('egads - hdf_io.py - Hdf - _add_dim - AttributeError, no file open')
            raise AttributeError('No file open')

    def _write_variable(self, data, varname, dims, ftype):
        """
        Private method to write/create variable in currently opened Hdf file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _write_variable')
        if self.f is not None:
            dtype = self.TYPE_DICT[ftype]
            path, _ = os.path.split(varname)
            if dims is not None:
                for dim in dims:
                    try:
                        if path != '/':
                            self.f[path + '/' + dim]
                        else:
                            self.f[dim]
                    except KeyError:
                        logging.error("egads - hdf_io.py - Hdf - _write_variable - KeyError, the following "
                                      "dimension '" + dim + "' can\'t be found in the Hdf file")
                        raise KeyError("The following dimension '" + dim + "' can\'t be found in the Hdf file")
            self.f.create_dataset(varname, data=data, dtype=dtype)
            for i, dim in enumerate(dims):
                self.f[varname].dims[i].attach_scale(self.f[path + '/' + dim])
                self.f[varname].dims[i].label = dim
        else:
            logging.error('egads - hdf_io.py - Hdf - _write_variable - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - Hdf - _write_variable - varname ' + str(varname) + ' -> data write OK')

    def _delete_attribute(self, attrname, objectname):
        """
        Private method to delete attribute to currently open file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _delete_attribute')
        if self.f is not None:
            if objectname is not None:
                obj = self.f[objectname]
            else:
                obj = self.f
            obj.attrs.__delitem__(attrname)
        else:
            logging.error('egads - hdf_io.py - Hdf - _delete_attribute - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - Hdf - _delete_attribute - attrname ' + str(attrname)
                      + ' -> attribute delete OK')

    def _delete_group(self, groupname):
        """
        Private method to delete group in currently open file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _delete_group')
        if self.f is not None:
            obj = self.f[groupname]
            if isinstance(obj, h5py.Group):
                self.f.__delitem__(groupname)
        else:
            logging.error('egads - hdf_io.py - Hdf - _delete_group - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - Hdf - _delete_group - groupname ' + str(groupname)
                      + ' -> group delete OK')

    def _delete_variable(self, varname):
        """
        Private method to delete variable in currently open file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _delete_variable')
        if self.f is not None:
            obj = self.f[varname]
            if isinstance(obj, h5py.Dataset):
                self.f.__delitem__(varname)
        else:
            logging.error('egads - hdf_io.py - Hdf - _delete_variable - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - Hdf - _delete_variable - varname ' + str(varname)
                      + ' -> group delete OK')

    def _convert_to_netcdf(self, nc_file):
        """
        Private method to convert the opened HDF file to NetCDF format.
        """

        logging.debug('egads - hdf_io.py - Hdf - _convert_to_netcdf')
        if self.f is not None:
            if nc_file is None:
                nc_file = os.path.splitext(self.filename)[0] + '.nc'

            # netcdf file creation
            f = egads.input.NetCdf(nc_file, 'w')

            # add global attributes
            add_history = False
            dt = datetime.datetime.now()
            for key, value in self.get_attribute_list().items():
                if key == 'history':
                    add_history = True
                    value += ' ; converted to NetCdf by EGADS, ' + str(dt)
                f.add_attribute(key, value)
            if not add_history:
                f.add_attribute('history', 'converted to NetCdf by EGADS, ' + str(dt))

            # add groups
            for group in self.get_group_list(details=True):
                f.add_group(group)
                attrs = self.get_attribute_list(group)
                for attr_name, attr_val in attrs.items():
                    f.add_attribute(attr_name, attr_val, group)

            # add dimensions
            for dim_path, dim_size in self.get_dimension_list(group_walk=True, details=True).items():
                f.add_dim(dim_path, dim_size)

            # add variables
            type_dict = {'char': 'c', 'byte': 'b', 'int16': 'i2', 'int32': 'i4', 'float32': 'f4', 'float64': 'f8'}
            for var_path in self.get_variable_list(group_walk=True, details=True):
                dim_tuple = tuple([dim for dim in self.get_dimension_list(var_path)])
                data = self.read_variable(var_path)
                try:
                    dtype = type_dict[str(data.dtype)]
                except KeyError:
                    try:
                        dtype = self.TYPE_DICT[str(data.dtype)]
                    except KeyError:
                        dtype = str(data.dtype)
                attrs = self.get_attribute_list(var_path)
                try:
                    fillvalue = attrs['_FillValue']
                except KeyError:
                    try:
                        fillvalue = attrs['missing_value']
                    except KeyError:
                        fillvalue = None
                f.write_variable(data, var_path, dims=dim_tuple, ftype=dtype, fillvalue=fillvalue)
                no_metadata = ['_FillValue', 'DIMENSION_LABELS', 'NAME', 'CLASS', 'REFERENCE_LIST', 'DIMENSION_LIST']
                for attr_name, attr_val in attrs.items():
                    if attr_name not in no_metadata:
                        f.add_attribute(attr_name, attr_val, var_path)

            f.close()
            logging.debug('egads - hdf_io.py - Hdf - _convert_to_netcdf -> file conversion OK')
        else:
            logging.error('egads - hdf_io.py - Hdf - _convert_to_netcdf - AttributeError, no file open')
            raise AttributeError('No file open')

    def _convert_to_nasa_ames(self, na_file, float_format, delimiter, no_header):
        """
        Private method to convert currently open Hdf file to one or more NASA Ames files.
        """

        logging.debug('egads - hdf_io.py - Hdf - _convert_to_nasa_ames')

        if not na_file:
            na_file = os.path.splitext(self.filename)[0] + '.na'

        # read dimensions and variables, try to check if ffi = 1001
        dim_list = self.get_dimension_list()
        var_list = self.get_variable_list()

        if len(dim_list) > 1:
            logging.exception('egads - hdf_io.py - Hdf - the actual convert_to_nasa_ames cant '
                              'process file with multiple dimensions, FFI is set to 1001')
            raise Exception('the actual convert_to_nasa_ames cant process file with multiple dimensions, '
                            'FFI is set to 1001')
        elif len(dim_list) == 0:
            logging.exception('egads - hdf_io.py - Hdf - there is no dimensions at the root of '
                              'the opened netcdf file.')
            raise Exception('there is no dimensions at the root of the opened hdf file.')

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
        ncom = ['==== Normal Comments follow ====', 'The NA file has been converted from a Hdf file by EGADS']
        for attr in self.get_attribute_list():
            if attr != 'institution' and attr != 'authors' and attr != 'source' and attr != 'title':
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
        ncom.append('==== Normal Comments end ====')
        ncom.append('=== Data Section begins on the next line ===')
        for name in dim_list:
            name_string += name + '    '
        scom = ['==== Special Comments follow ====',
                '=== Additional Variable Attributes defined in the source file ===',
                '== Variable attributes from source (Hdf) file follow ==']
        for var in variables:
            if var[0] not in dim_list:
                first_line = True
                for metadata in var[3]:
                    no_metadata = ['_FillValue', 'scale_factor', 'units', 'var_name', 'DIMENSION_LABELS', 'NAME',
                                   'CLASS', 'REFERENCE_LIST', 'DIMENSION_LIST']
                    if metadata not in no_metadata:
                        if first_line:
                            first_line = False
                            scom.append('  Variable ' + var[0] + ':')
                        try:
                            scom.append('    ' + metadata + ' = ' + str(var[3][metadata]))
                        except TypeError:
                            logging.exception('egads - hdf_io.py - Hdf - convert_to_nasa_ames - an error '
                                              + 'occurred when trying to add variable metadata in SCOM - metadata '
                                              + str(metadata))
                name_string += var[0] + '    '
        name_string = name_string[:-4]
        ncom.append(name_string)
        scom.append('== Variable attributes from source (Hdf) file end ==')
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
        logging.debug('egads - hdf_io.py - Hdf - _convert_to_nasa_ames - na_file ' + str(na_file)
                      + ' -> file conversion OK')

    logging.info('egads - hdf_io.py - Hdf has been loaded')


class EgadsHdf(Hdf):
    """
    EGADS class for reading and writing to Hdf files following EUFAR
    conventions. Inherits from the general EGADS Hdf module.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes Hdf instance.

        :param string filename:
            Optional - Name of Hdf file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data), ``a`` and ``r+`` for append, and ``r``
            for read. ``r`` is the default value.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - __init__')
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    def read_variable(self, varname, input_range=None, read_as_float=False, replace_fill_value=False):
        """
        Reads a variable from currently opened Hdf file and maps the Hdf
        attributes to an :class:`~egads.core.EgadsData` instance.

        :param string varname:
            Name of Hdf variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces _FillValue (or missing_value) to NaN,
            if one of those attributes exists in the Hdf file. False is the default value.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - read_variable - varname ' + str(varname) + ', input_range '
                      + str(input_range))
        return self._read_variable(varname, input_range, read_as_float, replace_fill_value)

    def add_dim(self, name, data, ftype='double'):
        """
        Adds dimension to currently open file or to a group.

        :param string name:
            Name of dimension to add, it can includes a path to the group where to add
            the dimension.
        :param EgadsData data:
            Instance of EgadsData object to write out to file.
            All data and attributes will be written out to the file.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. Options
            for type are ``double``, ``float``, ``int``, ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - add_dim - name ' + str(name))
        self._add_dim(name, data, ftype)

    def write_variable(self, data, varname=None, dims=None, ftype='double'):
        """
        Writes/creates variable in currently opened Hdf file.

        :param EgadsData data:
            Instance of EgadsData object to write out to file.
            All data and attributes will be written out to the file.
        :param string varname:
            Optional - Name of variable to create/write to. If no varname is provided,
            and if hdf_name attribute in EgadsData object is defined, then the variable will be
            written to hdf_name. If path to a group is in varname, the variable will be
            created in this group. In that case, varname is mandatory as the function will
            not take into account path in varname metadata of the EgadsData instance.
        :param tuple dims:
            Optional - Name(s) of dimensions to assign to variable. If variable already exists
            in Hdf file, this parameter is optional. For scalar variables, pass an empty tuple.
        :param string ftype:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``,
            ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - write_variable - varname ' + str(varname) +
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

    def convert_to_netcdf(self, filename=None):
        """
        Converts the opened Hdf file to NetCdf format following the EUFAR and EGADS
        convention. If groups exist, they are preserved in the new NetCDF file.

        :param string filename:
            Optional - if only a name is given, a NetCDF file named ``filename`` is
            created in the HDF file folder ; if a path and a name are given, a NetCDF
            file named ``name`` is created in the folder ``path``.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - convert_to_netcdf - filename ' + str(filename))
        self._convert_to_netcdf(filename)

    def _open_file(self, filename, perms):
        """
        Private method for opening Hdf file.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - _open_file')
        self.close()
        try:
            self.f = h5py.File(filename, perms)
            self.filename = filename
            self.perms = perms
            attr_dict = self.get_attribute_list()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename)
        except RuntimeError:
            logging.exception('egads - hdf_io.py - EgadsHdf - _open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - hdf_io.py - EgadsHdf - _open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)
        except Exception:
            logging.exception('egads - hdf_io.py - EgadsHdf - _open_file - Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

    def _read_variable(self, varname, input_range, read_as_float, replace_fill_value):
        """
        Private method to read a variable from currently opened Hdf file.
        """

        try:
            if input_range is None:
                var = numpy.array(self.f[varname])
            else:
                obj = 'slice(input_range[0], input_range[1])'
                for i in range(2, len(input_range), 2):
                    obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
                var = numpy.array(self.f[varname][eval(obj)])
        except KeyError:
            logging.exception('egads - hdf_io.py - Hdf - _read_variable - KeyError, variable does not exist in '
                              'hdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        if read_as_float:
            var = var.astype(float)
        var_attrs = self._get_attribute_list(varname)
        if replace_fill_value:
            _fill_value = None
            if '_FillValue' in var_attrs:
                _fill_value = var_attrs['_FillValue']
                var[var == _fill_value] = numpy.nan
            elif 'missing_value' in var_attrs:
                _fill_value = var_attrs['missing_value']
                var[var == _fill_value] = numpy.nan
            elif 'fill_value' in var_attrs:
                _fill_value = var_attrs['fill_value']
                var[var == _fill_value] = numpy.nan
            else:
                logging.warning('egads - hdf_io.py - EgadsHdf - _read_variable - KeyError, no missing value '
                                + 'attribute has been found for the variable ' + varname + '. Missing value not '
                                + 'replaced by NaN.')

        for attr in ['DIMENSION_LABELS', 'NAME', 'CLASS', 'REFERENCE_LIST', 'DIMENSION_LIST']:
            try:
                del var_attrs[attr]
            except KeyError:
                pass

        variable_metadata = egads.core.metadata.VariableMetadata(var_attrs, self.file_metadata)
        data = egads.EgadsData(var, variable_metadata=variable_metadata)
        if len(var.dtype) > 1:
            data.compound_data = True
        else:
            data.compound_data = False
        logging.debug('egads - hdf_io.py - EgadsHdf - _read_variable - varname ' + str(varname)
                      + ' -> data read OK')
        return data

    def _add_dim(self, name, data, ftype):
        """
        Private method to add dimension to currently open file or group.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - _add_dim')
        if self.f is not None:
            fillvalue = None
            dtype = self.TYPE_DICT[ftype]
            try:
                fillvalue = data.metadata['_FillValue']
            except KeyError:
                try:
                    fillvalue = data.metadata['missing_value']
                except KeyError:
                    pass
            if fillvalue is not None:
                var = numpy.where(numpy.isnan(data.value), fillvalue, data.value)
            else:
                var = data.value
            self.f.create_dataset(name, data=var, dtype=dtype)
            self.f[name].make_scale(name)
            self.f[name].dims[0].label = os.path.split(name)[1]
            for key, val in data.metadata.items():
                if val:
                    if isinstance(val, list):
                        tmp = ''
                        for item in val:
                            tmp += item + ', '
                        self.add_attribute(str(key), tmp[:-2], name)
                    else:
                        self.add_attribute(str(key), val, name)
        else:
            logging.error('egads - hdf_io.py - EgadsHdf - _add_dim - AttributeError, no file open')
            raise AttributeError('No file open')

    def _write_variable(self, data, varname, dims, ftype):
        """
        Private method to write/create variable in currently opened Hdf file.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - _write_variable')
        if self.f is not None:
            fillvalue = None
            dtype = self.TYPE_DICT[ftype]
            path = os.path.dirname(varname)
            if dims is not None:
                for dim in dims:
                    try:
                        self.f[path + '/' + dim]
                    except KeyError:
                        logging.error("egads - hdf_io.py - EgadsHdf - _write_variable - KeyError, the following "
                                      "dimension '" + dim + "' can\'t be found in the Hdf file")
                        raise KeyError("The following dimension '" + dim + "' can\'t be found in the Hdf file")
            try:
                fillvalue = data.metadata['_FillValue']
            except KeyError:
                try:
                    fillvalue = data.metadata['missing_value']
                except KeyError:
                    pass
            if fillvalue is not None:
                if isinstance(fillvalue, int) and fillvalue > 1000000000000000000 or fillvalue < 1000000000000000000:
                    fillvalue = float(fillvalue)
                var = data.value
                var[var == numpy.nan] = fillvalue
            else:
                var = data.value
            self.f.create_dataset(varname, data=var, dtype=dtype)
            for i, dim in enumerate(dims):
                self.f[varname].dims[i].attach_scale(self.f[path + '/' + dim])
                self.f[varname].dims[i].label = dim
            for key, val in data.metadata.items():
                if isinstance(val, list):
                    tmp = ''
                    for item in val:
                        tmp += item + ', '
                    self.add_attribute(str(key), tmp[:-2], varname)
                else:
                    if key == '_FillValue' or key == 'missing_value':
                        if key == '_FillValue':
                            fillvalue = data.metadata['_FillValue']
                        if key == 'missing_value':
                            fillvalue = data.metadata['missing_value']
                        if fillvalue > 1000000000000000000 or fillvalue < 1000000000000000000:
                            fillvalue = float(fillvalue)
                        self.add_attribute(str(key), fillvalue, varname)
                    else:
                        self.add_attribute(str(key), val, varname)
        else:
            logging.error('egads - hdf_io.py - EgadsHdf - _write_variable - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - EgadsHdf - _write_variable - varname ' + str(varname) + ' -> data write OK')

    def _convert_to_netcdf(self, nc_file):
        """
        Private method to convert the opened HDF file to NetCDF format.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - _convert_to_netcdf')
        if self.f is not None:
            if nc_file is None:
                nc_file = os.path.splitext(self.filename)[0] + '.nc'

            # netcdf file creation
            f = egads.input.NetCdf(nc_file, 'w')

            # add global attributes
            add_history = False
            dt = datetime.datetime.now()
            for key, value in self.get_attribute_list().items():
                if key == 'history':
                    add_history = True
                    value += ' ; converted to NetCdf by EGADS, ' + str(dt)
                f.add_attribute(key, value)
            if not add_history:
                f.add_attribute('history', 'converted to NetCdf by EGADS, ' + str(dt))

            # add groups
            for group in self.get_group_list(details=True):
                f.add_group(group)
                attrs = self.get_attribute_list(group)
                for attr_name, attr_val in attrs.items():
                    f.add_attribute(attr_name, attr_val, group)

            # add dimensions
            for dim_path, dim_size in self.get_dimension_list(group_walk=True, details=True).items():
                f.add_dim(dim_path, dim_size)

            # add variables
            for var_path in self.get_variable_list(group_walk=True, details=True):
                dim_tuple = tuple([dim for dim in self.get_dimension_list(var_path)])
                data = self.read_variable(var_path)
                f.write_variable(data, var_path, dims=dim_tuple, ftype=str(data.dtype))

            f.close()
            logging.debug('egads - hdf_io.py - EgadsHdf - _convert_to_netcdf -> file conversion OK')
        else:
            logging.error('egads - hdf_io.py - EgadsHdf - _convert_to_netcdf - AttributeError, no file open')
            raise AttributeError('No file open')

    def _convert_to_nasa_ames(self, na_file, float_format, delimiter, no_header):
        """
        Private method to convert currently open EGADS Hdf file to one or more NASA
        Ames files. For now can only process Hdf files to NASA/Ames FFI 1001:
        variables can only be dependant to one independant variable at a time. Groups,
        if exist, are not converted to NA file format.
        """

        logging.debug('egads - hdf_io.py - EgadsHdf - _convert_to_nasa_ames')
        if not na_file:
            na_file = os.path.splitext(self.filename)[0] + '.na'

        # read dimensions and variables, try to check if ffi = 1001
        dim_list = self.get_dimension_list()
        var_list = self.get_variable_list()
        if len(dim_list) > 1:
            logging.exception('egads - hdf_io.py - EgadsHdf - the actual convert_to_nasa_ames cant '
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
        ncom = ['==== Normal Comments follow ====', 'The NA file has been converted from a Hdf file by EGADS']
        for attr in self.get_attribute_list():
            if attr != 'institution' and attr != 'authors' and attr != 'source' and attr != 'title':
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
        ncom.append('==== Normal Comments end ====')
        ncom.append('=== Data Section begins on the next line ===')
        for name in dim_list:
            name_string += name + '    '
        scom = ['==== Special Comments follow ====',
                '=== Additional Variable Attributes defined in the source file ===',
                '== Variable attributes from source (Hdf) file follow ==']
        for var in var_list:
            if var not in dim_list:
                data = self.read_variable(var)
                f.write_variable(data, var, na_dict=na_dict)
                first_line = True
                for metadata in data.metadata:
                    no_metadata = ['_FillValue', 'scale_factor', 'units', 'var_name', 'DIMENSION_LABELS', 'NAME',
                                   'CLASS', 'REFERENCE_LIST', 'DIMENSION_LIST']
                    if metadata not in no_metadata:
                        if first_line:
                            first_line = False
                            scom.append('  Variable ' + var + ':')
                        try:
                            scom.append('    ' + metadata + ' = ' + str(data.metadata[metadata]))
                        except TypeError:
                            logging.exception('egads - hdf_io.py - EgadsHdf - convert_to_nasa_ames - an error '
                                              + 'occurred when trying to add variable metadata in SCOM - metadata '
                                              + str(metadata))
                name_string += var + '    '
        name_string = name_string[:-4]
        ncom.append(name_string)
        scom.append('== Variable attributes from source (Hdf) file end ==')
        scom.append('==== Special Comments end ====')
        f.write_attribute_value('SCOM', scom, na_dict=na_dict)
        f.write_attribute_value('NCOM', ncom, na_dict=na_dict)
        f.write_attribute_value('NSCOML', len(scom), na_dict=na_dict)
        f.write_attribute_value('NNCOML', len(ncom), na_dict=na_dict)

        # write na file
        f.save_na_file(na_file, na_dict=na_dict, float_format=float_format, delimiter=delimiter, no_header=no_header)
        f.close()

    logging.info('egads - hdf_io.py - EgadsHdf has been loaded')

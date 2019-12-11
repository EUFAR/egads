__author__ = "ohenry"
__date__ = "2019-11-22 07:09"
__version__ = "0.8"
__all__ = ["Hdf", "EgadsHdf"]


import logging
import h5py
import collections
import itertools
import numpy
import egads
import os
from egads.input import FileCore


class Hdf(FileCore):
    """
    EGADS class for reading and writing to generic Hdf5 files.

    This module is a sub-class of :class:`~.FileCore` and adapts the Python h5py
    library to the EGADS file-access methods.
    """

    TYPE_DICT = {'char': 'c', 'byte': 'b', 'short': 'i2', 'int': 'i4', 'float': 'f4', 'double': 'f8'}

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

    def get_file_structure(self):
        """
        Returns a view of the file structure, groups and datasets.
        """

        return self._get_file_structure()

    def get_variable_list(self, details=True):
        """
        Returns a list of variables found in the current Hdf file.

        :param bool details:
            By default, True. if True, returns a list of dictionary with the name
            of the dataset and the path of the dataset in the Hdf file. If False,
            returns a list of string.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_variable_list')
        return self._get_variable_list(details)

    def get_attribute_list(self, objectname=None):
        """
        Returns a dictionary of attributes and values found in current Hdf file
        either globally, or attached to a given object, Group or Dataset.

        :param string objectname:
            Optional - Name of object to get list of attributes from. If no object name is
            provided, the function returns top-level Hdf attributes.
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
        """

        logging.debug('egads - hdf_io.py - Hdf - get_attribute_value - attrname ' + str(attrname)
                      + ', varname ' + str(objectname))
        attrs = self._get_attribute_list(objectname)
        return attrs[attrname]

    def get_dimension_list(self, varname=None):
        """
        Returns an ordered dictionary of dimensions and their sizes found in the current
        Hdf file. If an object name is provided, the dimension names and lengths associated
        with that object are returned.

        :param string varname:
            Name of variable to get list of associated dimensions for. If no variable
            name is provided, the function returns all dimensions in the Hdf file.
        """

        logging.debug('egads - hdf_io.py - Hdf - get_dimension_list - varname ' + str(varname))
        return self._get_dimension_list(varname)

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

    def delete_attribute(self, attrname, varname=None):
        """
        Deletes attribute to currently open file. If varname is included, attribute
        is removed from specified variable or group, otherwise it is removed from global file
        attributes.

        :param string attrname:
            Attribute name.
        :param string varname:
            Optional - If varname is provided, attribute removed from specified
            variable or group in the Hdf file.
        """

        logging.debug('egads - hdf_io.py - Hdf - delete_attribute - attrname ' + str(attrname) +
                      ', varname ' + str(varname))
        self._delete_attribute(attrname, varname)

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

    # def convert_to_netcdf(self, filename=None):
    #     """
    #     Converts the opened HDF file to Hdf format following the EUFAR and EGADS
    #     convention. If groups exist, they are preserved in the new Hdf file.
    #
    #     :param string filename:
    #         Optional - if only a name is given, a Hdf file named ``filename`` is
    #         created in the HDF file folder ; if a path and a name are given, a Hdf
    #         file named ``name`` is created in the folder ``path``.
    #     """
    #
    #     logging.debug('egads - hdf_io.py - Hdf - convert_to_netcdf - filename ' + str(filename))
    #     print('No function to convert to Hdf.')
    #     self._convert_to_netcdf(filename)

    # def convert_to_nasa_ames(self, na_file=None, float_format=None, delimiter='    ', no_header=False):
    #     """
    #     Convert currently open Hdf file to one or more NASA Ames files. For now can
    #     only process Hdf files to NASA/Ames FFI 1001: only time as an independant
    #     variable. Groups are not handle by the function and will lead to an error.
    #
    #     :param string na_file:
    #         Optional - Name of output NASA Ames file. If none is provided, name of
    #         current Hdf file is used and suffix changed to .na
    #     :param string delimiter:
    #         Optional - The delimiter desired for use between data items in the data
    #         file. Default - Tab.
    #     :param string float_format:
    #         Optional - The format of float numbers to be saved. If no string is entered, values are
    #         not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
    #     :param string delimiter:
    #         Optional - The delimiter desired for use between data items in the data
    #         file. Default - '    ' (four spaces).
    #     :param bool no_header:
    #         Optional - If set to true, then only the data blocks are written to file.
    #         Default - False.
    #     """
    #
    #     logging.debug('egads - hdf_io.py - Hdf - convert_to_nasa_ames - float_format ' + str(float_format)
    #                   + ', delimiter ' + str(delimiter) + ', no_header ' + str(no_header))
    #     print('No function to convert to NasaAmes.')

    # def convert_to_csv(self, csv_file=None, float_format=None, no_header=False):
    #     """
    #     Converts currently open Hdf file to CSV file using the NasaAmes class. Limitations
    #     are the same than in the ``convert_to_nasa_ames`` function.
    #
    #     :param string csv_file:
    #         Optional - Name of output CSV file. If none is provided, name of current
    #         Hdf is used and suffix changed to .csv
    #     :param string float_format:
    #         Optional - The format of float numbers to be saved. If no string is entered, values are
    #         not round up. Ex: '%.4f' to round up to 4 decimals. Default - None
    #     :param bool no_header:
    #         Optional - If set to true, then only the data blocks are written to file.
    #         Default - False.
    #     """
    #     logging.debug('egads - hdf_io.py - Hdf - convert_to_csv - csv_file ' + str(csv_file)
    #                   + ', float_format ' + str(float_format) + ', no_header ' + str(no_header))
    #     print('No function to convert to NasaAmes.')
    #     if not csv_file:
    #         csv_file = os.path.splitext(self.filename)[0] + '.csv'
    #
    #     self._convert_to_nasa_ames(na_file=csv_file, float_format=float_format, delimiter=',', no_header=no_header)
    #     logging.debug('egads - netcdf_io.py - NetCdf - convert_to_csv - csv_file ' + str(csv_file)
    #                   + ' -> file conversion OK')

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

    def _get_file_structure(self):
        """
        Private method for getting a view of the file structure, groups and datasets.
        """

        file_structure = collections.OrderedDict()

        def _h5py_get_file_structure(name, obj):
            file_structure[name] = {'object': obj, 'type': type(obj)}

        self.f.visititems(_h5py_get_file_structure)
        return file_structure

    def _get_variable_list(self, details=True):
        """
        Private method for getting list of dataset names.
        """

        logging.debug('egads - hdf_io.py - Hdf - _get_variable_list')
        if self.f is not None:
            var_list = []

            def _h5py_get_file_structure(name, obj):
                if isinstance(obj, h5py.Dataset):
                    var_path, var_name = os.path.split(name)
                    if details:
                        var_list.append({var_name: var_path})
                    else:
                        var_list.append(var_name)

            self.f.visititems(_h5py_get_file_structure)
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
            if obj is not None:
                attr_dict = {}
                for key, value in self.f[obj].attrs.items():
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    if isinstance(value, str):
                        value = ' '.join(value.split())
                    attr_dict[key] = value
                return attr_dict
            else:
                attr_dict = {}
                for key, value in self.f.attrs.items():
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    if isinstance(value, str):
                        value = ' '.join(value.split())
                    attr_dict[key] = value
                return attr_dict
        else:
            logging.error('egads.input.Hdf._get_attribute_list: AttributeError, No file open')
            raise AttributeError('No file open')

    def _get_dimension_list(self, varname):
        """
        Private method to get an ordered dictionary of dimensions and their sizes found in the current
        Hdf file.
        """

        dim_dict = collections.OrderedDict()
        if varname is None:
            var_list = self._get_variable_list(True)
            dim_list = []
            for var in var_list:
                var, path = list(var.keys())[0], var[list(var.keys())[0]]
                var_dim = [dim.label for dim in self.f[path + '/' + var].dims]
                dim_shp = self.f[path + '/' + var].shape
                for i, dim in enumerate(var_dim):
                    if dim:
                        dim_list.append([dim, dim_shp[i]])
            for dim in [sublist for sublist, _ in itertools.groupby(dim_list)]:
                dim_dict[dim[0]] = dim[1]
        else:
            dim_shape = self.f[varname].shape
            for i, dim in enumerate(self.f[varname].dims):
                dim_dict[dim.label] = dim_shape[i]
        return dim_dict

    def _read_variable(self, varname, input_range, read_as_float, replace_fill_value):
        """
        Private method to read a variable from currently opened Hdf file.
        """

        var_list = self._get_variable_list(True)
        path, var = os.path.split(varname)
        exist = False
        for item in var_list:
            if var == list(item.keys())[0] and path == item[list(item.keys())[0]]:
                exist = True
        if not exist:
            logging.exception('egads - hdf_io.py - Hdf - _read_variable - KeyError, variable does not exist in '
                              'hdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        else:
            # var_path = self._get_variable_list()[var_list.index(varname)][varname] + '/' + varname
            # var_path = path + var
            if input_range is None:
                var = numpy.array(self.f[varname])
            else:
                obj = 'slice(input_range[0], input_range[1])'
                for i in range(2, len(input_range), 2):
                    obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
                var = numpy.array(self.f[varname][eval(obj)])
            if read_as_float:
                var = var.astype(float)
            if replace_fill_value:
                _fill_value = None
                var_attrs = self._get_attribute_list(varname)
                if '_FillValue' in var_attrs:
                    _fill_value = var_attrs['_FillValue']
                elif 'missing_value' in var_attrs:
                    _fill_value = var_attrs['missing_value']
                elif 'fill_value' in var_attrs:
                    _fill_value = var_attrs['fill_value']
                else:
                    logging.exception('egads - hdf_io.py - Hdf - _read_variable - KeyError, no missing value metadata '
                                      + 'has been found for the variable ' + varname)
                    raise KeyError("ERROR: no missing value exists for Variable %s in %s" % (varname, self.filename))
                if _fill_value is not None:
                    var[var == _fill_value] = numpy.nan
            logging.debug('egads - hdf_io.py - Hdf - _read_variable - varname ' + str(varname) + ' -> data read OK')
            return var

    def _add_group(self, groupname):
        """
        Private method to Add group to currently open file.
        """

        logging.debug('egads - hdf_io.py - Hdf - _add_group')
        if self.f is not None:
            if isinstance(groupname, list):
                groupname = '/'.join(groupname)
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
                        self.f[path + '/' + dim]
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

    def _delete_attribute(self, attrname, varname):
        """
        Private method to delete attribute to currently open file.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _delete_attribute')
        if self.f is not None:
            if varname is not None:
                obj = self.f[varname]
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

    # def _convert_to_netcdf(self, filename):
    #     """
    #     Private method to convert the opened HDF file to Hdf format.
    #     """
    #
    #     logging.debug('egads - hdf_io.py - Hdf - _convert_to_netcdf')
    #
    #     if self.f is not None:
    #         pass
    #     else:
    #         logging.error('egads - hdf_io.py - Hdf - _delete_variable - AttributeError, no file open')
    #         raise AttributeError('No file open')

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

        var_list = self._get_variable_list(True)
        path, var = os.path.split(varname)
        exist = False
        for item in var_list:
            if var == list(item.keys())[0] and path == item[list(item.keys())[0]]:
                exist = True
        if not exist:
            logging.exception('egads - hdf_io.py - Hdf - _read_variable - KeyError, variable does not exist in '
                              'hdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        else:
            if input_range is None:
                var = numpy.array(self.f[varname])
            else:
                obj = 'slice(input_range[0], input_range[1])'
                for i in range(2, len(input_range), 2):
                    obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
                var = numpy.array(self.f[varname][eval(obj)])
            if read_as_float:
                var = var.astype(float)
            var_attrs = self._get_attribute_list(varname)
            if replace_fill_value:
                _fill_value = None
                if '_FillValue' in var_attrs:
                    _fill_value = var_attrs['_FillValue']
                elif 'missing_value' in var_attrs:
                    _fill_value = var_attrs['missing_value']
                elif 'fill_value' in var_attrs:
                    _fill_value = var_attrs['fill_value']
                else:
                    logging.exception('egads - hdf_io.py - EgadsHdf - _read_variable - KeyError, no missing value '
                                      'metadata has been found for the variable ' + varname)
                    raise KeyError("ERROR: no missing value exists for Variable %s in %s" % (varname, self.filename))
                if _fill_value is not None:
                    var[var == _fill_value] = numpy.nan

            variable_metadata = egads.core.metadata.VariableMetadata(var_attrs, self.file_metadata)
            data = egads.EgadsData(var, variable_metadata=variable_metadata)
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
            path, _ = os.path.split(varname)
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
                var = numpy.where(numpy.isnan(data.value), fillvalue, data.value)
            else:
                var = data.value
            self.f.create_dataset(varname, data=var, dtype=dtype)
            for i, dim in enumerate(dims):
                self.f[varname].dims[i].attach_scale(self.f[path + '/' + dim])
                self.f[varname].dims[i].label = dim
            for key, val in data.metadata.items():
                if val:
                    if isinstance(val, list):
                        tmp = ''
                        for item in val:
                            tmp += item + ', '
                        self.add_attribute(str(key), tmp[:-2], varname)
                    else:
                        self.add_attribute(str(key), val, varname)
        else:
            logging.error('egads - hdf_io.py - EgadsHdf - _write_variable - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - hdf_io.py - EgadsHdf - _write_variable - varname ' + str(varname) + ' -> data write OK')

    logging.info('egads - hdf_io.py - EgadsHdf has been loaded')

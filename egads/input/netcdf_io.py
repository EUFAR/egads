__author__ = "mfreer, ohenry"
__date__ = "2016-12-6 15:47"
__version__ = "1.11"
__all__ = ["NetCdf", "EgadsNetCdf"]

import logging
import netCDF4
import egads
import datetime
import operator
import os
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
        
        logging.debug('egads - netcdf_io.py - NetCdf - open - filename ' + str(filename) + ', perms ' + str(perms))
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

        :param string name:
            Name of attribute to examine
        :param string varname:
            Optional - Name of variable attribute is attached to. If none specified, global
            attributes are examined.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - get_attribute_value - attrname ' + str(attrname) + ', varname ' + str(varname))
        attrs = self._get_attribute_list(varname)
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

    def read_variable(self, varname, input_range=None):
        """
        Reads a variable from currently opened NetCDF file.
        
        :param string varname:
            Name of NetCDF variable to read in.
        :param vector input_range:
            Optional - Range of values in each dimension to input. TODO add example
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - read_variable - varname ' + str(varname) + ', input_range ' + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.exception('egads - netcdf_io.py - NetCdf - read_variable - KeyError, variable does not exist in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.exception('egads - netcdf_io.py - NetCdf - read_variable - Exception, unexpected error')
            raise Exception("Error: Unexpected error")
        if input_range is None:
            value = varin[:]
        else:
            obj = 'slice(input_range[0], input_range[1])'
            for i in xrange(2, len(input_range), 2):
                obj = obj + ', slice(input_range[%i], input_range[%i])' % (i, i + 1)
            value = varin[eval(obj)]
        logging.debug('egads - netcdf_io.py - NetCdf - read_variable - varname ' + str(varname) + ' -> data read OK')
        return value
    
    def change_variable_name(self, varname, newname):
        """
        Change the variable name in currently opened NetCDF file.
        
        :param string varname:
            Name of variable to rename.
        :param string oldname:
            the new name.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - change_variable_name - varname ' + str(varname) + ', newname ' + str(newname))
        if self.f is not None:
            self.f.renameVariable(varname, newname)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - .change_variable_name - AttributeError, no file open')
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

        logging.debug('egads - netcdf_io.py - NetCdf - write_variable - varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype) + ', fillvalue ' + str(fillvalue))
        if self.f is not None:
            try:
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype], dims, fill_value = fillvalue)
            except KeyError:
                varout = self.f.createVariable(varname, ftype, dims, fillvalue)
            varout[:] = value
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
        :param string value:
            Value to assign to attribute name.
        :param string varname:
            Optional - If varname is provided, attribute name and value are added to specified
            variable in the NetCDF file.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - add_attribute - attrname ' + str(attrname) + 
                      ', value ' + str(value) + ', varname ' + str(varname))
        if self.f is not None:
            if varname is not None:
                varin = self.f.variables[varname]
                setattr(varin, attrname, value)
            else:
                setattr(self.f, attrname, value)
        else:
            logging.error('egads - netcdf_io.py - NetCdf - change_variable_name - AttributeError, no file open')
            raise AttributeError('No file open')
        logging.debug('egads - netcdf_io.py - NetCdf - add_attribute - attrname ' + str(attrname) + ' -> attribute add OK')
        
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
        logging.debug('egads - netcdf_io.py - NetCdf - delete_attribute - attrname ' + str(attrname) + ' -> attribute delete OK')
    

    def convert_to_nasa_ames(self, na_file=None, requested_ffi=1001, float_format='%g', 
                             delimiter=None, annotation=False, no_header=False):
        """
        Convert currently open NetCDF file to one or more NASA Ames files
        using  Nappy. For now can only process NetCdf files to NASA/Ames FFI 1001 : 
        only time as an independant variable.

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
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - '    ' (four spaces).
        :param bool annotation:
            Optional - If set to true, write the output file with an additional left-hand
            column describing the contents of each header line. Default - False.
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ', requested_ffi ' + str(requested_ffi) + ', float_format ' + str(float_format)
                      + ', delimiter ' + str(delimiter) + ', annotation ' + str(annotation)
                      + ', no_header ' + str(no_header))
        if not na_file:
            filename, _ = os.path.splitext(self.filename)
            na_file = filename + '.na'
        
        # create NASA/Ames dictionary
        f = egads.input.NasaAmes()  # @UndefinedVariable
        na_dict = f.create_na_dict()
        missing_attributes = []
        
        # populate NLHEAD, FFI, ONAME, ORG, SNAME, MNAME, RDATE
        nlhead, ffi, org, oname, sname, mname, dx = -999, 1001, '', '', '', '', [0.0]
        try:
            org = self.get_attribute_value('institution')
        except KeyError:
            missing_attributes.append('institution')
        try:
            oname = self.get_attribute_value('authors')
        except KeyError:
            missing_attributes.append('authors - replaced by institution')
            oname = org
        try:
            sname = self.get_attribute_value('source')
        except KeyError:
            missing_attributes.append('source')
        try:
            mname = self.get_attribute_value('title')
        except KeyError:
            missing_attributes.append('title')
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]
        
        # read dimensions and variables, try to check if ffi = 1001
        var_dims = self.get_dimension_list()
        var_list = self.get_variable_list()
        variables = []
        for var in var_list:
            if var not in var_dims.keys():
                dims = self.get_dimension_list(var)
                if len(dims) > 1:
                    raise Exception('the actual convert_to_nasa_ames cant process data of multiple '
                                + 'dimensions, FFI is set to 1001')
                    logging.exception('egads - netcdf_io.py - NetCdf - the actual convert_to_nasa_ames cant process data of multiple '
                                + 'dimensions, FFI is set to 1001')
                vvar = {}
                value = self.read_variable(var).tolist()
                attr_dict = {}
                all_attr = self.get_attribute_list(var)
                for index, item in enumerate(value):
                    if item == None:
                        value[index] = all_attr['_FillValue']
                for attr in all_attr:
                    attr_dict[attr] = self.get_attribute_value(attr, var)
                vvar[var] = [value, dims.keys()[0], attr_dict]
                variables.append(vvar)
        
        # read independant variables (actual dimensions) and populate XNAME
        independant_variables = []
        niv = 0
        for key, _ in var_dims.iteritems():
            ivar = {}
            try:
                var = self.read_variable(key).tolist()
                attr_dict = {}
                all_attr = self.get_attribute_list(key)
                for attr in all_attr:
                    attr_dict[attr] = self.get_attribute_value(attr, key)
                ivar[key] = [var, attr_dict]
                independant_variables.append(ivar)
                niv += 1
            except KeyError:
                ivar[key] = None
                independant_variables.append(ivar)
        
        # populate DATE if time is in independant_variables
        date = None
        for ivar in independant_variables:
            if 'time' in ivar.keys():
                var = ivar.values()[0][0]
                ref_time = None
                try:
                    index = ivar.values()[0][1]['units'].index(' since ')
                    ref_time = ivar.values()[0][1]['units'][index + 7:]
                except (KeyError, ValueError):
                    pass
                isotime = egads.algorithms.transforms.SecondsToIsotime().run([var[0]], ref_time)  # @UndefinedVariable
                y, m, d, _, _, _ = egads.algorithms.transforms.IsotimeToElements().run(isotime) # @UndefinedVariable
                date = [y.value[0], m.value[0], d.value[0]]
        if not date:
            date = [999, 999, 999]
        
        # add global attributes to NA dict
        f.write_attribute_value('NLHEAD', nlhead, na_dict = na_dict)
        f.write_attribute_value('FFI', ffi, na_dict = na_dict)
        f.write_attribute_value('ONAME', oname, na_dict = na_dict)
        f.write_attribute_value('ONAME', oname, na_dict = na_dict)
        f.write_attribute_value('ORG', org, na_dict = na_dict)
        f.write_attribute_value('SNAME', sname, na_dict = na_dict)
        f.write_attribute_value('MNAME', mname, na_dict = na_dict)
        f.write_attribute_value('DATE', date, na_dict = na_dict)
        f.write_attribute_value('RDATE', rdate, na_dict = na_dict)
        f.write_attribute_value('NIV', niv, na_dict = na_dict)
        f.write_attribute_value('DX', dx, na_dict = na_dict)
        
        # loop on the different independant variables and save
        ivol = 0
        nvol = len(var_dims)
        for key, _ in reversed(sorted(var_dims.items(), key=operator.itemgetter(1))):
        
            # populate NVOL and filename
            ivol += 1
            if len(var_dims) > 1:
                filename, extension = os.path.splitext(na_file)
                na_file_out = filename + '_' + str(ivol) + extension
            else:
                na_file_out = na_file
            
            # populate NV, VMISS, VSCAL, VNAME, SCOM and V
            nv = 0
            vmiss = []
            vscal = []
            vname = []
            v = []
            xname = []
            x = []
            name_string = ''
            scom = ['==== Special Comments follow ====',
                    '=== Additional Variable Attributes defined in the source file ===',
                    '== Variable attributes from source (NetCDF) file follow ==']
            for var in variables:
                if key == var.values()[0][1]:
                    try:
                        units = var.values()[0][2]['units']
                    except KeyError:
                        units = 'no units'
                    name = var.keys()[0]
                    try:
                        miss = var.values()[0][2]['_FillValue']
                    except KeyError:
                        try:
                            miss = var.values()[0][2]['missing_value']
                        except KeyError:
                            miss = None
                    scom.append('  Variable ' + name + ':')
                    attr_list = self.get_attribute_list(name)
                    for attr in attr_list:
                        if attr not in ['_FillValue', 'scale_factor', 'add_offset']:
                            value = self.get_attribute_value(attr, name)
                            scom.append('    ' + attr + ' = ' + str(value))     
                    vmiss.append(miss)
                    vscal.append(1)
                    vname.append(name + ' (' + units + ')')
                    v.append(var.values()[0][0])
                    nv += 1
            scom.append('== Variable attributes from source (NetCDF) file end ==')
            scom.append('==== Special Comments end ====') 
        
            # populate NCOM
            ncom = ['==== Normal Comments follow ====']
            attr_list = self.get_attribute_list()
            for attr in attr_list:
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
            ncom.append('==== Normal Comments end ====')
            ncom.append('=== Data Section begins on the next line ===')
            for name in xname:
                if name in key:
                    name_string += name + ','
            for name in vname:
                name_string += name + ','
            name_string = name_string[:-1]
            
            # populate X and XNAME
            for ivar in independant_variables:
                if key == ivar.keys()[0]:
                    try:
                        x = ivar.values()[0][0]
                    except TypeError:
                        x = [0]
                    try:
                        units = ivar.values()[0][1]['units']
                    except (KeyError, TypeError):
                        units = 'no units'
                    xname.append(key + ' (' + units + ')')
                    name_string = key + ' (' + units + '),' + name_string
            
            # add attributes to NA dict and save
            f.write_attribute_value('NVOL', nvol, na_dict = na_dict)
            f.write_attribute_value('IVOL', ivol, na_dict = na_dict)
            f.write_attribute_value('SCOM', scom, na_dict = na_dict)
            f.write_attribute_value('NCOM', ncom, na_dict = na_dict)
            f.write_attribute_value('NSCOML', len(scom), na_dict = na_dict)
            f.write_attribute_value('NNCOML', len(ncom), na_dict = na_dict)
            f.write_attribute_value('VMISS', vmiss, na_dict = na_dict)
            f.write_attribute_value('VSCAL', vscal, na_dict = na_dict)
            f.write_attribute_value('XNAME', xname, na_dict = na_dict)
            f.write_attribute_value('VNAME', vname, na_dict = na_dict)
            f.write_attribute_value('V', v, na_dict = na_dict)
            f.write_attribute_value('X', x, na_dict = na_dict)
            f.write_attribute_value('NV', nv, na_dict = na_dict)
            f.save_na_file(na_file_out, na_dict, float_format, delimiter=delimiter, 
                           annotation=annotation, no_header=no_header)
            logging.debug('egads - netcdf_io.py - NetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ' -> file conversion OK')
      
    def convert_to_csv(self, csv_file=None, float_format='%g', annotation=False, no_header=False):
        """
        Converts currently open NetCDF file to CSV file using Nappy API.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        :param string float_format:
            Optional - The formatting string used for formatting floats when writing
            to output file. Default - %g
        :param bool annotation:
            Optional - If set to true, write the output file with an additional left-hand
            column describing the contents of each header line. Default - False.
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - NetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ', float_format ' + str(float_format) + ', annotation ' + str(annotation)
                      + ', no_header ' + str(no_header))
        if not csv_file:
            filename, _ = os.path.splitext(self.filename)
            csv_file = filename + '.csv'
        
        self.convert_to_nasa_ames(na_file=csv_file, requested_ffi=1001, float_format=float_format, 
                             delimiter=',', annotation=annotation, no_header=no_header)
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

        logging.debug('egads - netcdf_io.py - NetCdf - _open_file - filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            self.f = netCDF4.Dataset(filename, perms)  # @UndefinedVariable
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            logging.exception('egads - netcdf_io.py - NetCdf - _open_file - RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.exception('egads - netcdf_io.py - NetCdf - _open_file - IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
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
                for key, value in varin.__dict__.iteritems():
                    if isinstance(value, basestring):
                        value = " ".join(value.split())
                    attr_dict[key] = value
                return attr_dict
            else:
                attr_dict = {}
                for key, value in self.f.__dict__.iteritems():
                    if isinstance(value, basestring):
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
        dimdict = {}
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
                for dimname, dimobj in reversed(sorted(dims.iteritems())):
                    dimdict[dimname] = len(dimobj)
            return dimdict
        else:
            logging.error('egads - netcdf_io.py - NetCdf - _get_attribute_list - AttributeError, No file open')
            raise AttributeError('No file open')
        return None

    def _get_variable_list(self):
        """
        Private method for getting list of variable names.
        """

        logging.debug('egads - netcdf_io.py - NetCdf - _get_variable_list')
        if self.f is not None:
            return self.f.variables.keys()
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

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - __init__ - filename ' + str(filename) + 
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
            Optional - Range of values in each dimension to input.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname) + 
                      ', input_range ' + str(input_range))
        try:
            varin = self.f.variables[varname]
        except KeyError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - read_variable - KeyError, variable does not exist in netcdf file')
            raise KeyError("ERROR: Variable %s does not exist in %s" % (varname, self.filename))
        except Exception:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - read_variable - Exception, unexpected error')
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
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - read_variable - varname ' + str(varname) + ' -> data read OK')
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
        :param string type:
            Optional - Data type of variable to write. Defaults to ``double``. If variable exists,
            data type remains unchanged. Options for type are ``double``, ``float``, ``int``, 
            ``short``, ``char``, and ``byte``
        """

        logging.debug('egads - netcdf_io.py - EgadsNetCdf - write_variable - varname ' + str(varname) + 
                      ', dims ' + str(dims) + ', ftype ' + str(ftype))
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
                        fillvalue = None
                varout = self.f.createVariable(varname, self.TYPE_DICT[ftype.lower()], dims, fill_value=fillvalue)
            varout[:] = data.value
            for key, val in data.metadata.iteritems():
                if key != '_FillValue':
                    if val:
                        setattr(varout, str(key), val)
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - write_variable - varname ' + str(varname) + ' -> data write OK')
        
    def convert_to_nasa_ames(self, na_file=None, requested_ffi=1001, float_format='%g', 
                             delimiter=None, annotation=False, no_header=False):
        """
        Convert currently open EGADS NetCDF file to one or more NASA Ames files
        using  Nappy. For now can only process NetCdf files to NASA/Ames FFI 1001 : 
        variables can only be dependant to one independant variable at a time.

        :param string na_file:
            Optional - Name of output NASA Ames file. If none is provided, name of
            current NetCDF file is used and suffix changed to .na
        :param int requested_ffi:
            The NASA Ames File Format Index (FFI) you wish to write to. Options
            are limited depending on the data structures found.
        :param string float_format:
            Optional - The formatting string used for formatting floats when writing
            to output file. Default - %g
        :param string delimiter:
            Optional - The delimiter desired for use between data items in the data
            file. Default - '    ' (four spaces).
        :param bool annotation:
            Optional - If set to true, write the output file with an additional left-hand
            column describing the contents of each header line. Default - False.
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ', requested_ffi ' + str(requested_ffi) + ', float_format ' + str(float_format)
                      + ', delimiter ' + str(delimiter) + ', annotation ' + str(annotation)
                      + ', no_header ' + str(no_header))
        if not na_file:
            filename, _ = os.path.splitext(self.filename)
            na_file = filename + '.na'
        
        # create NASA/Ames dictionary
        f = egads.input.NasaAmes()  # @UndefinedVariable
        na_dict = f.create_na_dict()
        missing_attributes = []
        
        # populate NLHEAD, FFI, ONAME, ORG, SNAME, MNAME, RDATE
        nlhead, ffi, org, oname, sname, mname, dx = -999, 1001, '', '', '', '', [0.0]
        try:
            org = self.get_attribute_value('institution')
        except KeyError:
            missing_attributes.append('institution')
        try:
            oname = self.get_attribute_value('authors')
        except KeyError:
            missing_attributes.append('authors - replaced by institution')
            oname = org
        try:
            sname = self.get_attribute_value('source')
        except KeyError:
            missing_attributes.append('source')
        try:
            mname = self.get_attribute_value('title')
        except KeyError:
            missing_attributes.append('title')
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]
        
        # read dimensions and variables, try to check if ffi = 1001
        var_dims = self.get_dimension_list()
        var_list = self.get_variable_list()
        variables = []
        for var in var_list:
            if var not in var_dims.keys():
                dims = self.get_dimension_list(var)
                if len(dims) > 1:
                    raise Exception('the actual convert_to_nasa_ames cant process data of multiple '
                                + 'dimensions, FFI is set to 1001')
                    logging.exception('egads - netcdf_io.py - EgadsNetCdf - the actual convert_to_nasa_ames cant process data of multiple '
                                + 'dimensions, FFI is set to 1001')
                vvar = {}
                value = self.read_variable(var).value.tolist()
                attr_dict = {}
                all_attr = self.get_attribute_list(var)
                for attr in all_attr:
                    attr_dict[attr] = self.get_attribute_value(attr, var)
                vvar[var] = [value, dims.keys()[0], attr_dict]
                variables.append(vvar)
        
        # read independant variables (actual dimensions) and populate XNAME
        independant_variables = []
        niv = 0
        for key, _ in var_dims.iteritems():
            ivar = {}
            try:
                var = self.read_variable(key).value.tolist()
                attr_dict = {}
                all_attr = self.get_attribute_list(key)
                for attr in all_attr:
                    attr_dict[attr] = self.get_attribute_value(attr, key)
                ivar[key] = [var, attr_dict]
                independant_variables.append(ivar)
                niv += 1
            except KeyError:
                ivar[key] = None
                independant_variables.append(ivar)
        
        # populate DATE if time is in independant_variables
        date = None
        for ivar in independant_variables:
            if 'time' in ivar.keys():
                var = ivar.values()[0][0]
                ref_time = None
                try:
                    index = ivar.values()[0][1]['units'].index(' since ')
                    ref_time = ivar.values()[0][1]['units'][index + 7:]
                except (KeyError, ValueError):
                    pass
                isotime = egads.algorithms.transforms.SecondsToIsotime().run([var[0]], ref_time)  # @UndefinedVariable
                y, m, d, _, _, _ = egads.algorithms.transforms.IsotimeToElements().run(isotime) # @UndefinedVariable
                date = [y.value[0], m.value[0], d.value[0]]
        if not date:
            date = [999, 999, 999]
        
        # add global attributes to NA dict
        f.write_attribute_value('NLHEAD', nlhead, na_dict = na_dict)
        f.write_attribute_value('FFI', ffi, na_dict = na_dict)
        f.write_attribute_value('ONAME', oname, na_dict = na_dict)
        f.write_attribute_value('ONAME', oname, na_dict = na_dict)
        f.write_attribute_value('ORG', org, na_dict = na_dict)
        f.write_attribute_value('SNAME', sname, na_dict = na_dict)
        f.write_attribute_value('MNAME', mname, na_dict = na_dict)
        f.write_attribute_value('DATE', date, na_dict = na_dict)
        f.write_attribute_value('RDATE', rdate, na_dict = na_dict)
        f.write_attribute_value('NIV', niv, na_dict = na_dict)
        f.write_attribute_value('DX', dx, na_dict = na_dict)
        
        # loop on the different independant variables and save
        ivol = 0
        nvol = len(var_dims)
        for key, _ in reversed(sorted(var_dims.items(), key=operator.itemgetter(1))):
        
            # populate NVOL and filename
            ivol += 1
            if len(var_dims) > 1:
                filename, extension = os.path.splitext(na_file)
                na_file_out = filename + '_' + str(ivol) + extension
            else:
                na_file_out = na_file
            
            # populate NV, VMISS, VSCAL, VNAME, SCOM and V
            nv = 0
            vmiss = []
            vscal = []
            vname = []
            v = []
            xname = []
            x = []
            name_string = ''
            scom = ['==== Special Comments follow ====',
                    '=== Additional Variable Attributes defined in the source file ===',
                    '== Variable attributes from source (NetCDF) file follow ==']
            for var in variables:
                if key == var.values()[0][1]:
                    try:
                        units = var.values()[0][2]['units']
                    except KeyError:
                        units = 'no units'
                    name = var.keys()[0]
                    try:
                        miss = var.values()[0][2]['_FillValue']
                    except KeyError:
                        try:
                            miss = var.values()[0][2]['missing_value']
                        except KeyError:
                            miss = None
                    scom.append('  Variable ' + name + ':')
                    attr_list = self.get_attribute_list(name)
                    for attr in attr_list:
                        if attr not in ['_FillValue', 'scale_factor', 'add_offset']:
                            value = self.get_attribute_value(attr, name)
                            scom.append('    ' + attr + ' = ' + str(value))     
                    vmiss.append(miss)
                    vscal.append(1)
                    vname.append(name + ' (' + units + ')')
                    v.append(var.values()[0][0])
                    nv += 1
            scom.append('== Variable attributes from source (NetCDF) file end ==')
            scom.append('==== Special Comments end ====') 
        
            # populate NCOM
            ncom = ['==== Normal Comments follow ====']
            attr_list = self.get_attribute_list()
            for attr in attr_list:
                ncom.append(attr + ': ' + str(self.get_attribute_value(attr)))
            ncom.append('==== Normal Comments end ====')
            ncom.append('=== Data Section begins on the next line ===')
            for name in xname:
                if name in key:
                    name_string += name + ','
            for name in vname:
                name_string += name + ','
            name_string = name_string[:-1]
            
            # populate X and XNAME
            for ivar in independant_variables:
                if key == ivar.keys()[0]:
                    try:
                        x = ivar.values()[0][0]
                    except TypeError:
                        x = [0]
                    try:
                        units = ivar.values()[0][1]['units']
                    except (KeyError, TypeError):
                        units = 'no units'
                    xname.append(key + ' (' + units + ')')
                    name_string = key + ' (' + units + '),' + name_string
            
            # add attributes to NA dict and save
            f.write_attribute_value('NVOL', nvol, na_dict = na_dict)
            f.write_attribute_value('IVOL', ivol, na_dict = na_dict)
            f.write_attribute_value('SCOM', scom, na_dict = na_dict)
            f.write_attribute_value('NCOM', ncom, na_dict = na_dict)
            f.write_attribute_value('NSCOML', len(scom), na_dict = na_dict)
            f.write_attribute_value('NNCOML', len(ncom), na_dict = na_dict)
            f.write_attribute_value('VMISS', vmiss, na_dict = na_dict)
            f.write_attribute_value('VSCAL', vscal, na_dict = na_dict)
            f.write_attribute_value('XNAME', xname, na_dict = na_dict)
            f.write_attribute_value('VNAME', vname, na_dict = na_dict)
            f.write_attribute_value('V', v, na_dict = na_dict)
            f.write_attribute_value('X', x, na_dict = na_dict)
            f.write_attribute_value('NV', nv, na_dict = na_dict)
            f.save_na_file(na_file_out, na_dict, float_format, delimiter=delimiter, 
                           annotation=annotation, no_header=no_header)
            logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_nasa_ames - na_file ' + str(na_file)
                      + ' -> file conversion OK')
      
    def convert_to_csv(self, csv_file=None, float_format='%g', annotation=False, no_header=False):
        """
        Converts currently open NetCDF file to CSV file using Nappy API.
        
        :param string csv_file:
            Optional - Name of output CSV file. If none is provided, name of current
            NetCDF is used and suffix changed to .csv
        :param string float_format:
            Optional - The formatting string used for formatting floats when writing
            to output file. Default - %g
        :param bool annotation:
            Optional - If set to true, write the output file with an additional left-hand
            column describing the contents of each header line. Default - False.
        :param bool no_header:
            Optional - If set to true, then only the data blocks are written to file.
            Default - False.
        """
        
        logging.debug('egads - netcdf_io.py - EgadsNetCdf - convert_to_csv - csv_file ' + str(csv_file)
                      + ', float_format ' + str(float_format) + ', annotation ' + str(annotation)
                      + ', no_header ' + str(no_header))
        if not csv_file:
            filename, _ = os.path.splitext(self.filename)
            csv_file = filename + '.csv'
        self.convert_to_nasa_ames(na_file=csv_file, requested_ffi=1001, float_format=float_format, 
                             delimiter=',', annotation=annotation, no_header=no_header)
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
            self.f = netCDF4.Dataset(filename, perms)  # @UndefinedVariable
            self.filename = filename
            self.perms = perms
            attr_dict = self.get_attribute_list()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename)
        except RuntimeError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.exception('egads - netcdf_io.py - EgadsNetCdf - _open_file - Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")
        
    logging.info('egads - netcdf_io.py - EgadsNetCdf has been loaded')


__author__ = "ohenry"
__date__ = "2018-7-21 14:52"
__version__ = "1.7"
__all__ = ["NasaAmes", "EgadsNasaAmes"]

import logging
import datetime
import egads
import copy
import re
import os
import io
import numpy as np
from egads.input import FileCore


class NasaAmes(FileCore):
    """
    EGADS module for interfacing with NASA Ames files.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes NASA Ames instance.

        :param string filename:
            Optional - Name of NetCDF file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data), ``a`` and ``r+`` for append, 
            and ``r`` for read. ``r`` is the default value.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - __init__')
        self.__delimiter = None
        FileCore.__init__(self, filename, perms)

    def read_na_dict(self):
        """
        Read the dictionary from currently open NASA Ames file. Method accessible by
        the user to read the dictionary in a custom object.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_na_dict')
        return copy.deepcopy(self.na_dict)

    @staticmethod
    def create_na_dict():
        """
        Create a typical NASA/Ames dictionary. It is intended to be saved in a new file. The user
        will have to populate the dictionary with other functions.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - create_na_dict')
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]
        ffi = 1001
        nlhead = 10
        ivol = 1
        nvol = 1
        dx = 0.0
        na_dict = {"DATE": rdate,
                   "DX": dx,
                   "FFI": ffi,
                   "IVOL": ivol,
                   "MNAME": None,
                   "NAUXC": None,
                   "NAUXV": None,
                   "NCOM": None,
                   "NIV": None,
                   "NLHEAD": nlhead,
                   "NNCOML": None,
                   "NSCOML": None,
                   "NV": 0,
                   "NVOL": nvol,
                   "NX": 0,
                   "NXDEF": None,
                   "ONAME": None,
                   "ORG": None,
                   "RDATE": rdate,
                   "SCOM": None,
                   "SNAME": None,
                   "V": [],
                   "VMISS": [],
                   "VNAME": [],
                   "VSCAL": [],
                   "X": [],
                   "XNAME": []
                   }
        return na_dict
    
    def read_variable(self, varname, na_dict=None, read_as_float=False, replace_fill_value=False):
        """
        Read in variable from currently open NASA Ames file to :class: NumpyArray
        object.

        :param string|int varname:
            String name or sequential number of variable to read in from currently
            open file. If independant variable is read, sequential number is useless as
            FFI 1001 has only one independant variable.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which the variable will be read. By default,
            na_dict = None and the variable is read to the currently opened dictionary. Only
            mandatory if creating a new file or creating a new dictionary.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file. `False`` is the default value.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces missing_value to NaN.
            ``False`` is the default value.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_variable - varname ' + str(varname))
        if not na_dict:
            na_dict = self.na_dict
        try:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(na_dict=na_dict)
                varnum = var_list.index(varname)
            values = np.array(na_dict['V'][varnum])
            if read_as_float:
                values = values.astype('float')
            try:
                if replace_fill_value:
                    miss = self.get_attribute_value('_FillValue', varname)
                    values[values == miss] = np.nan
            except ValueError:
                raise Exception('cannot convert float NaN to integer')
        except ValueError:
            values = np.array(na_dict['X'])
            if read_as_float:
                values = [float(item) for item in values]
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_variable - varname ' + str(varname)
                      + ' -> data read OK')
        return values
    
    def write_variable(self, data, varname=None, vartype="main", attrdict=None, na_dict=None):
        """
        Write or update a variable in the NASA/Ames dictionary.

        :param list|NumpyArray data:
            Data to be written in the NASA/Ames dictionary. data can be a list of value or an 
            NumpyArray instance.
        :param string|int varname:
            The name or the sequential number of the variable to be written in the 
            dictionary.
        :param string vartype:
            The type of data to read, by default ``main``. Options are ``independant`` for 
            independant variables, ``main`` for main variables. ``main`` is the default value.
        :param dict attrdict:
            Optional - Dictionary of variable attribute linked to the variable to be written
            in the dictionary. Mandatory only if data is not already present in the dictionary.
            Mandatory attributes for NasaAmes: units, scale_factor, _FillValue and standard_name
            if varname is None. Other variable attributes are written in the SCOM file attribute.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which the variable will be added. By default, 
            na_dict = None and the variable is added to the currently opened dictionary. Only 
            mandatory if creating a new file or creating a new dictionary.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_variable - varname ' + str(varname) + '; vartype '
                      + str(vartype))
        if not na_dict:
            na_dict = self.na_dict
        if vartype == "main":
            try:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(na_dict=na_dict)
                    varnum = var_list.index(varname)
                na_dict['V'][varnum] = data
            except ValueError:
                if attrdict is None:
                    raise ValueError('attrdict can\'t be equal to None if varname doesn\'t exist in na_dict. ')
                value = data
                if varname is not None:
                    name = varname
                else:
                    try:
                        name = attrdict["standard_name"]
                    except KeyError:
                        try:
                            name = attrdict["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The '
                                              'EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                try:
                    units = attrdict["units"]
                except KeyError:
                    logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object'
                                      'has no units metadata')
                    raise KeyError('The EgadsData object has no units metadata')
                try:
                    scale = attrdict["scale_factor"]
                except KeyError:
                    scale = int(1)
                    logging.debug('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object'
                                  'has no scale_factor metadata')
                try:
                    miss = attrdict["_FillValue"]
                except KeyError:
                    try:
                        miss = attrdict["missing_value"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData '
                                          'object has no _FillValue or missing_value metadata')
                        raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
                na_dict['NV'] += 1
                na_dict['V'].append(value)
                na_dict['VNAME'].append(name + " (" + units + ")")
                na_dict['VMISS'].append(miss)
                na_dict['VSCAL'].append(scale)
        elif vartype == "independant":
            if na_dict['X']:
                na_dict['X'] = data
            else:
                value = data
                if varname is not None:
                    name = varname
                else:
                    try:
                        name = attrdict["standard_name"]
                    except KeyError:
                        try:
                            name = attrdict["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The '
                                              'EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                try:
                    units = attrdict["units"]
                except KeyError:
                    logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object'
                                      'has no units metadata')
                    raise KeyError('The EgadsData object has no units metadata')
                na_dict['NX'] = 1
                na_dict['X'] = value
                na_dict['XNAME'] = name + " (" + units + ")"
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_variable - data write OK')
    
    def get_variable_list(self, na_dict=None, vartype='main'):
        """ 
        Returns list of all variables in NASA Ames file.
        
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the variable list. By default, 
            na_dict = None and the variable list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_variable_list - vartype ' + str(vartype))
        var_list = []
        var_type = {'main': 'VNAME', 'independant': 'XNAME'}
        try:
            if not na_dict:
                na_dict = self.na_dict
            if isinstance(na_dict[var_type[vartype]], list):
                for var in na_dict[var_type[vartype]]:
                    var_list.append(_attemptVarAndUnitsMatch(var)[0])
            else:
                var_list.append(_attemptVarAndUnitsMatch(na_dict[var_type[vartype]])[0])
        except Exception:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - get_variable_list - An exception occured when '
                              'EGADS tried to get variable list.')
        return var_list
    
    def get_dimension_list(self, na_dict=None):
        """
        Returns a dictionary of all dimensions linked to their variables in NASA Ames dictionary.
        
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the dimension list. By default, 
            na_dict = None and the dimension list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_dimension_list')
        dim_dict = {}
        if not na_dict:
            na_dict = self.na_dict
        dim_dict[_attemptVarAndUnitsMatch(na_dict['XNAME'])[0]] = len(na_dict['X'])
        return dim_dict
    
    def get_attribute_list(self, varname=None, vartype="main", na_dict=None):
        """
        Returns a list of attributes found in current NASA Ames file either globally or
        attached to a given variable, depending on the type
        
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes. If independant
            variable attribute list is read, sequential number is useless as FFI 1001 has only
            one independant variable.
        :param string| vartype:
            Optional - type of variable to get list of attributes from. If no variable 
            type is provided with the variable name, the function returns an attribute
            of the main variable .
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the attribute list. By default, 
            na_dict = None and the attribute list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        """

        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_attribute_list - varname ' + str(varname)
                      + ', vartype ' + str(vartype))
        if not na_dict:
            na_dict = self.na_dict
        if varname is not None:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
                varnum = var_list.index(varname)
            attr_list = []
            if vartype == "main":
                variable, units = _attemptVarAndUnitsMatch(na_dict['VNAME'][varnum])
                miss = na_dict['VMISS'][varnum]
                scale = na_dict['VSCAL'][varnum]
                if variable is not None:
                    attr_list.append("standard_name")
                if units is not None:
                    attr_list.append("units")
                if miss is not None:
                    attr_list.append("_FillValue")
                if scale is not None:
                    attr_list.append("scale_factor")
            elif vartype == "independant":
                variable, units = _attemptVarAndUnitsMatch(na_dict['XNAME'])
                if variable is not None:
                    attr_list.append("standard_name")
                if units is not None:
                    attr_list.append("units")
            return attr_list
        else:
            return na_dict.keys()
    
    def get_attribute_value(self, attrname, varname=None, vartype="main", na_dict=None):
        """
        Returns the value of an attribute found in current NASA Ames file either globally 
        or attached to a given variable (only name, units, _FillValue and scale_factor), depending on the type
        
        :param string attrname:
            String name of attribute to write in currently open file.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes. If independant
            variable attribute is read, sequential number is useless as FFI 1001 has only one
            independant variable.
        :param string vartype:
            Optional - type of variable to get list of attributes from. If no
            variable type is provided with the variable name, the function returns an 
            attribute of the main variable.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the attribute value. By default, 
            na_dict = None and the attribute value is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_attribute_value - attrname ' + str(attrname) + 
                      ', varname ' + str(varname) + ', vartype ' + str(vartype))
        if not na_dict:
            na_dict = self.na_dict
        if varname is None:
            return na_dict[attrname]
        else:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
                varnum = var_list.index(varname)
            vardict = dict()
            if vartype == "main":
                vardict = {'standard_name': _attemptVarAndUnitsMatch(na_dict['VNAME'][varnum])[0],
                           'units': _attemptVarAndUnitsMatch(na_dict['VNAME'][varnum])[1],
                           '_FillValue': na_dict['VMISS'][varnum],
                           'scale_factor': na_dict['VSCAL'][varnum]}
            elif vartype == "independant":
                vardict = {'standard_name': _attemptVarAndUnitsMatch(na_dict['XNAME'])[0],
                           'units': _attemptVarAndUnitsMatch(na_dict['XNAME'])[1]}
            return vardict[attrname]
            
    def write_attribute_value(self, attrname, attrvalue, na_dict=None, varname=None, vartype="main"):
        """
        Write the value of an attribute in current NASA Ames file either globally or
        attached to a given variable (only name, units, _FillValue and scale_factor), 
        depending on the type
        
        :param string attrname:
            String name of attribute to write in currently open file.
        :param string|int|float|list attrvalue:
            Value of attribute to write in currently open file.
        :param dict na_dict:
            Optional - dictionary in which the attribute will be added. By default, na_dict = None 
            and the attribute value is added to the currently opened dictionary. Only mandatory 
            if creating a new file or creating a new dictionary.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
        :param string vartype:
            Optional - type of variable to get list of attributes from. If no variable type     
            is provided with the variable name, the function returns an attribute
            of the main variable .
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_attribute_value - attrname ' + str(attrname) + 
                      ', varname ' + str(varname) + ', vartype ' + str(vartype))
        var_type = {'main': 'VNAME', 'independant': 'XNAME'}
        if not na_dict:
            na_dict = self.na_dict
        if varname is None:
            na_dict[attrname] = attrvalue
        else:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
                varnum = var_list.index(varname)
            attr_dict = {"standard_name": "NAME", "units": "UNITS", "_FillValue": "VMISS", "scale_factor": "VSCAL"}
            if attr_dict[attrname] == "NAME" or attr_dict[attrname] == "UNITS":
                variable, units = _attemptVarAndUnitsMatch(na_dict[var_type[vartype]][varnum])
                if attr_dict[attrname] == "UNITS":
                    na_dict[var_type[vartype]][varnum] = variable + " (" + attrvalue + ")" 
                if attr_dict[attrname] == "NAME":
                    na_dict[var_type[vartype]][varnum] = attrvalue + " (" + units + ")" 
            else:
                na_dict[attr_dict[attrname]][varnum] = attrvalue
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_attribute_value - attribute write OK')
    
    def save_na_file(self, filename=None, na_dict=None, float_format=None, delimiter='    ', no_header=False):
        """
        Save a NASA/Ames dictionary to a file. IMPORTANT: only FFI 1001 is supported.

        :param string filename:
            Optional - String name of the file to be written.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be saved. If no dictionary is entered,
            the dictionary currently opened during the open file process will be saved.
        :param string float_format:
            Optional - The format of float numbers to be saved. If no string is entered, values are
            not round up. Ex: '%.4f' to round up to 4 decimals.
        :param string delimiter:
            Optional - A character or multiple characters to separate data. By default '    ' (four
            spaces) is used
        :param boolean no_header:
            Optional - If no_header is True then suppress writing the header and only write the 
            data section. Default - False.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - save_na_file - float_format ' + str(float_format)
                      + ' ; delimiter ' + str(delimiter) + ' ; no_header ' + str(no_header))
        if not filename:
            filename = self.filename
        if not na_dict:
            na_dict = self.na_dict
        header_string = io.StringIO()
        if self.get_attribute_value('NLHEAD', na_dict=na_dict):
            nlhead = str(self.get_attribute_value('NLHEAD', na_dict=na_dict))
        else:
            nlhead = '1'
        ffi = str(self.get_attribute_value('FFI', na_dict=na_dict))
        mname = self.get_attribute_value('MNAME', na_dict=na_dict)
        sname = self.get_attribute_value('SNAME', na_dict=na_dict)
        org = self.get_attribute_value('ORG', na_dict=na_dict)
        oname = self.get_attribute_value('ONAME', na_dict=na_dict)
        date = self.get_attribute_value('DATE', na_dict=na_dict)
        rdate = [datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day]
        ivol = str(self.get_attribute_value('IVOL', na_dict=na_dict))
        nvol = str(self.get_attribute_value('NVOL', na_dict=na_dict))
        scom = self.get_attribute_value('SCOM', na_dict=na_dict)
        ncom = self.get_attribute_value('NCOM', na_dict=na_dict)
        dx = str(self.get_attribute_value('DX', na_dict=na_dict))
        xname = self.get_attribute_value('XNAME', na_dict=na_dict)
        nv = str(self.get_attribute_value('NV', na_dict=na_dict))
        x = self.get_attribute_value('X', na_dict=na_dict)
        v = self.get_attribute_value('V', na_dict=na_dict)
        f = open(filename, 'w')
        if not no_header:
            first_line = nlhead + delimiter + ffi + '\n'
            header_string.write(first_line)
            header_string.write(oname + '\n')
            header_string.write(org + '\n')
            header_string.write(sname + '\n')
            header_string.write(mname + '\n')
            header_string.write(ivol + delimiter + nvol + '\n')
            header_string.write(str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + delimiter + str(rdate[0]) +
                                ' ' + str(rdate[1]) + ' ' + str(rdate[2]) + '\n')
            header_string.write(dx + '\n')
            header_string.write(xname + '\n')
            header_string.write(nv + '\n')
            vscal_line = ''
            for i in na_dict['VSCAL']:
                vscal_line += str(i) + delimiter
            vscal_line = vscal_line[:-len(delimiter)]
            header_string.write(vscal_line + '\n')
            vmiss_line = ''
            for i in na_dict['VMISS']:
                vmiss_line += str(i) + delimiter
            vmiss_line = vmiss_line[:-len(delimiter)]
            header_string.write(vmiss_line + '\n')
            for i in na_dict['VNAME']:
                header_string.write(i + '\n')
            if isinstance(scom, list):
                nscoml = str(len(scom))
                scom = '\n'.join(scom) + '\n'
            else:
                if scom[-1:] == '\n':
                    offset = 0
                    newline = ''
                else:
                    offset = 1
                    newline = '\n'
                nscoml = str(scom.count('\n') + offset)
                scom = scom + newline
            header_string.write(nscoml + '\n')
            header_string.write(scom)
            if isinstance(ncom, list):
                nncoml = str(len(ncom))
                ncom = '\n'.join(ncom) + '\n'
            else:
                if ncom[-1:] == '\n':
                    offset = 0
                    newline = ''
                else:
                    offset = 1
                    newline = '\n'
                nncoml = str(ncom.count('\n') + offset)
                ncom = ncom + newline
            header_string.write(nncoml + '\n')
            header_string.write(ncom)
            header_string = header_string.getvalue()
            nlhead = str(header_string.count('\n'))
            first_line_ud = nlhead + delimiter + ffi + '\n'
            header_string = header_string.replace(first_line, first_line_ud)
            f.write(header_string)

        for m in range(len(x)):
            if float_format is not None:
                var_string = float_format % x[m] + delimiter
            else:
                var_string = str(x[m]) + delimiter
            for n in range(int(nv)):
                if 'int' in str(type(v[n][m])):
                    value = str(v[n][m])
                else:
                    if float_format is not None:
                        value = float_format % v[n][m]
                    else:
                        value = str(v[n][m])
                var_string = var_string + value + delimiter
            f.write(var_string[:-len(delimiter)] + '\n')
        f.flush()
        f.close()
    
    def convert_to_netcdf(self, nc_file=None, na_dict=None):
        """
        Convert a NASA/Ames dictionary to a NetCDF file.

        :param string nc_file:
            Optional - String name of the netcdf file to be written. If no filename is passed, 
            the function will used the name of the actually opened NASA/Ames file.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be converted. If no dictionary is entered,
            the dictionary currently opened during the open file process will be converted.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_netcdf - nc_file ' + str(nc_file))
        if not na_dict:
            na_dict = self.na_dict
        if not nc_file:
            filename, _ = os.path.splitext(self.filename)
            nc_file = filename + '.nc'
        nlhead = int(self.get_attribute_value('NLHEAD', na_dict=na_dict))
        ffi = int(self.get_attribute_value('FFI', na_dict=na_dict))
        title = self.get_attribute_value('MNAME', na_dict=na_dict)
        source = self.get_attribute_value('SNAME', na_dict=na_dict)
        institution = self.get_attribute_value('ORG', na_dict=na_dict)
        authors = self.get_attribute_value('ONAME', na_dict=na_dict)
        history = (str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-'
                   + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':'
                   + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
                   + ' - Converted to NetCDF format using EGADS and NASA Ames class.')
        first_date = (str(self.get_attribute_value('DATE', na_dict=na_dict)[0]) + '-' + 
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[1]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[2]))
        file_number = int(self.get_attribute_value('IVOL', na_dict=na_dict))
        total_files = int(self.get_attribute_value('NVOL', na_dict=na_dict))
        scom = ''
        ncom = ''
        if isinstance(self.get_attribute_value('SCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('SCOM', na_dict=na_dict):
                scom += i + '\n'
            scom = scom[:-1]
        else:
            scom = self.get_attribute_value('SCOM', na_dict=na_dict)
            if scom[-1:] == '\n':
                scom = scom[:-1]
        if isinstance(self.get_attribute_value('NCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('NCOM', na_dict=na_dict):
                ncom += i + '\n'
            ncom = ncom[:-1]
        else:
            ncom = self.get_attribute_value('NCOM', na_dict=na_dict)
            if ncom[-1:] == '\n':
                ncom = ncom[:-1]
        variable_list = self.get_variable_list(vartype='main', na_dict=na_dict)
        ind_variable_list = self.get_variable_list(vartype='independant', na_dict=na_dict)
        ind_dimension_list = self.get_dimension_list(na_dict=na_dict)
        g = egads.input.EgadsNetCdf(nc_file, 'w')
        g.add_attribute('Conventions', 'CF-1.0')
        g.add_attribute('no_of_nasa_ames_header_lines', nlhead)
        g.add_attribute('file_format_index', ffi)
        g.add_attribute('title', title)
        g.add_attribute('source', source)
        g.add_attribute('special_comments', scom)
        g.add_attribute('normal_comments', ncom)
        g.add_attribute('institution', institution)
        g.add_attribute('authors', authors)
        g.add_attribute('history', history)
        g.add_attribute('first_valid_date_of_data', first_date)
        g.add_attribute('file_number_in_set', file_number)
        g.add_attribute('total_files_in_set', total_files)
        dim_list = []
        for key, _ in ind_dimension_list.items():
            dim_list.append(str(key))
        dim_tuple = tuple(dim_list)
        for var in ind_variable_list:
            g.add_dim(var, ind_dimension_list[var])
            var_data = self.read_variable(var, na_dict=na_dict)
            attr_dict = {}
            for attr in self.get_attribute_list(var, 'independant', na_dict=na_dict):
                attr_dict[attr] = self.get_attribute_value(attr, var, 'independant', na_dict=na_dict)
            egads_data = egads.EgadsData(var_data, variable_metadata=attr_dict)
            g.write_variable(egads_data, var, dim_tuple)
        for var in variable_list:
            var_data = self.read_variable(var, na_dict=na_dict)
            attr_dict = {}
            for attr in self.get_attribute_list(var, na_dict=na_dict):
                attr_dict[attr] = self.get_attribute_value(attr, var, na_dict=na_dict)
            egads_data = egads.EgadsData(var_data, variable_metadata=attr_dict)
            g.write_variable(egads_data, var, dim_tuple)
        g.close()
        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_netcdf - nc_file ' + str(nc_file)
                      + ' -> file conversion OK')

    def convert_to_hdf(self, hdf_file=None, na_dict=None):
        """
        Convert a NASA/Ames dictionary to a Hdf file.

        :param string hdf_file:
            Optional - String name of the hdf file to be written. If no filename is passed,
            the function will used the name of the actually opened NASA/Ames file.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be converted. If no dictionary is entered,
            the dictionary currently opened during the open file process will be converted.
        """

        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_netcdf - hdf_file ' + str(hdf_file))
        if not na_dict:
            na_dict = self.na_dict
        if not hdf_file:
            filename, _ = os.path.splitext(self.filename)
            hdf_file = filename + '.h5'
        nlhead = int(self.get_attribute_value('NLHEAD', na_dict=na_dict))
        ffi = int(self.get_attribute_value('FFI', na_dict=na_dict))
        title = self.get_attribute_value('MNAME', na_dict=na_dict)
        source = self.get_attribute_value('SNAME', na_dict=na_dict)
        institution = self.get_attribute_value('ORG', na_dict=na_dict)
        authors = self.get_attribute_value('ONAME', na_dict=na_dict)
        history = (str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-'
                   + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':'
                   + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
                   + ' - Converted to NetCDF format using EGADS and NASA Ames class.')
        first_date = (str(self.get_attribute_value('DATE', na_dict=na_dict)[0]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[1]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[2]))
        file_number = int(self.get_attribute_value('IVOL', na_dict=na_dict))
        total_files = int(self.get_attribute_value('NVOL', na_dict=na_dict))
        scom = ''
        ncom = ''
        if isinstance(self.get_attribute_value('SCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('SCOM', na_dict=na_dict):
                scom += i + '\n'
            scom = scom[:-1]
        else:
            scom = self.get_attribute_value('SCOM', na_dict=na_dict)
            if scom[-1:] == '\n':
                scom = scom[:-1]
        if isinstance(self.get_attribute_value('NCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('NCOM', na_dict=na_dict):
                ncom += i + '\n'
            ncom = ncom[:-1]
        else:
            ncom = self.get_attribute_value('NCOM', na_dict=na_dict)
            if ncom[-1:] == '\n':
                ncom = ncom[:-1]
        variable_list = self.get_variable_list(vartype='main', na_dict=na_dict)
        ind_variable_list = self.get_variable_list(vartype='independant', na_dict=na_dict)
        ind_dimension_list = self.get_dimension_list(na_dict=na_dict)
        g = egads.input.EgadsHdf(hdf_file, 'w')
        g.add_attribute('Conventions', 'CF-1.0')
        g.add_attribute('no_of_nasa_ames_header_lines', nlhead)
        g.add_attribute('file_format_index', ffi)
        g.add_attribute('title', title)
        g.add_attribute('source', source)
        g.add_attribute('special_comments', scom)
        g.add_attribute('normal_comments', ncom)
        g.add_attribute('institution', institution)
        g.add_attribute('authors', authors)
        g.add_attribute('history', history)
        g.add_attribute('first_valid_date_of_data', first_date)
        g.add_attribute('file_number_in_set', file_number)
        g.add_attribute('total_files_in_set', total_files)
        dim_list = []
        for key, _ in ind_dimension_list.items():
            dim_list.append(str(key))
        dim_tuple = tuple(dim_list)
        for var in ind_variable_list:
            var_data = self.read_variable(var, na_dict=na_dict)
            attr_dict = {}
            for attr in self.get_attribute_list(var, 'independant', na_dict=na_dict):
                attr_dict[attr] = self.get_attribute_value(attr, var, 'independant', na_dict=na_dict)
            egads_data = egads.EgadsData(var_data, variable_metadata=attr_dict)
            g.add_dim(var, egads_data)
        for var in variable_list:
            var_data = self.read_variable(var, na_dict=na_dict)
            attr_dict = {}
            for attr in self.get_attribute_list(var, na_dict=na_dict):
                attr_dict[attr] = self.get_attribute_value(attr, var, na_dict=na_dict)
            egads_data = egads.EgadsData(var_data, variable_metadata=attr_dict)
            g.write_variable(egads_data, var, dim_tuple)
        g.close()
        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_hdf - hdf_file ' + str(hdf_file)
                      + ' -> file conversion OK')

    def _open_file(self, filename, perms):
        """
        Private method for opening NASA Ames file.

        :parm string filename:
            Name of NASA Ames file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - _open_file')
        self.close()
        try:
            self.f = open(filename, mode=perms)
            self.na_dict = self._get_header()
            self.na_dict['X'], self.na_dict['V'] = self._get_variables(filename)
            self.filename = filename
            self.perms = perms
        except RuntimeError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)

    def _get_header(self):
        logging.debug('egads - nasa_ames_io.py - NasaAmes - _get_header')
        tmp = {}
        self.__delimiter = '    '
        first_line = self.f.readline().rstrip('\n')
        if '    ' not in first_line:
            nlhead, ffi = re.findall(r'-?\d+\.?\d*', first_line)
            self.__delimiter = first_line[len(nlhead):first_line.find(ffi)]
        tmp['NLHEAD'], tmp['FFI'] = first_line.split(self.__delimiter)
        tmp['ONAME'] = self.f.readline().rstrip('\n')
        tmp['ORG'] = self.f.readline().rstrip('\n')
        tmp['SNAME'] = self.f.readline().rstrip('\n')
        tmp['MNAME'] = self.f.readline().rstrip('\n')
        tmp['IVOL'], tmp['NVOL'] = self.f.readline().rstrip('\n').split(self.__delimiter)
        # if self.__delimiter is None:
        #     yy1, mm1, dd1, yy2, mm2, dd2 = self.f.readline().split(self.__delimiter)
        # else:
        date, rdate = self.f.readline().split(self.__delimiter)
        yy1, mm1, dd1 = date.split()
        yy2, mm2, dd2 = rdate.split()
        tmp['DATE'] = [int(yy1), int(mm1), int(dd1)]
        tmp['RDATE'] = [int(yy2), int(mm2), int(dd2)]
        tmp['DX'] = self.f.readline().rstrip('\n')
        tmp['XNAME'] = self.f.readline().rstrip('\n')
        tmp['NV'] = int(self.f.readline().rstrip('\n'))
        vscal = self.f.readline().split(self.__delimiter)
        sf_list = []
        for sf in vscal:
            if isint(sf):
                sf = int(float(sf))
            else:
                sf = float(sf)
            sf_list.append(sf)
        tmp['VSCAL'] = sf_list
        vmiss = self.f.readline().split(self.__delimiter)
        fv_list = []
        for fv in vmiss:
            if isint(fv):
                fv = int(float(fv))
            else:
                fv = float(fv)
            fv_list.append(fv)
        tmp['VMISS'] = fv_list
        name_list = []
        for _ in range(tmp['NV']):
            name_list.append(self.f.readline().rstrip('\n'))
        tmp['VNAME'] = name_list
        tmp['NSCOML'] = int(self.f.readline().rstrip('\n'))
        scom = ''
        for _ in range(tmp['NSCOML']):
            scom += self.f.readline()
        tmp['SCOM'] = scom
        tmp['NNCOML'] = int(self.f.readline().rstrip('\n'))
        ncom = ''
        for _ in range(tmp['NNCOML']):
            ncom += self.f.readline()
        tmp['NCOM'] = ncom
        return tmp

    def _get_variables(self, filename):
        logging.debug('egads - nasa_ames_io.py - NasaAmes - _get_variables')
        data = np.genfromtxt(filename, dtype=None, delimiter=self.__delimiter, skip_header=int(self.na_dict['NLHEAD']))
        x, v = [], []
        for i in range(len(self.na_dict['VNAME'])):
            v.append([])
            for item in data:
                v[i].append(item[i + 1] * self.na_dict['VSCAL'][i])
                if i == 0:
                    x.append(item[i])
        return x, v

    logging.info('egads - nasa_ames_io.py - NasaAmes has been loaded')


class EgadsNasaAmes(NasaAmes):
    """
    EGADS class for reading and writing to NasaAmes files following EUFAR
    conventions. Inherits from the general EGADS NasaAmes module.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes EgadsNasaAmes instance.

        :param string filename:
            Optional - Name of NasaAmes file to open.
        :param char perms:
            Optional -  Permissions used to open file.
            Options are ``w`` for write (overwrites data), ``a`` and ``r+`` for append, and ``r``
            for read. ``r`` is the default value.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - __init__')
        self.file_metadata = None
        self.__delimiter = None
        FileCore.__init__(self, filename, perms)

    def read_variable(self, varname, na_dict=None, read_as_float=False, replace_fill_value=False):
        """
        Read in variable from currently open NASA Ames file to :class: EgadsData
        object. Any additional variable metadata is additionally read in.

        :param string|int varname:
            String name or sequential number of variable to read in from currently
            open file. If independant variable is read, sequential number is useless as
            FFI 1001 has only one independant variable.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which the variable will be read. By default,
            na_dict = None and the variable is read to the currently opened dictionary. Only
            mandatory if creating a new file or creating a new dictionary.
        :param boolean read_as_float:
            Optional - if True, EGADS reads the data and convert them to float numbers. If False,
            the data type is the type of data in file. `False`` is the default value.
        :param boolean replace_fill_value:
            Optional - if True, EGADS reads the data and replaces missing_value to NaN.
            ``False`` is the default value.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - read_variable - varname ' + str(varname))
        file_metadata = None
        if not na_dict:
            na_dict = self.na_dict
            file_metadata = self.file_metadata
        try:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(na_dict=na_dict)
                varnum = var_list.index(varname)
            variable, units = _attemptVarAndUnitsMatch(na_dict['VNAME'][varnum])
            miss = na_dict['VMISS'][varnum]
            scale = na_dict['VSCAL'][varnum]
            values = np.array(na_dict['V'][varnum])
            if read_as_float:
                values = values.astype('float')
            try:
                if replace_fill_value:
                    values[values == miss] = np.nan
            except ValueError:
                raise Exception('cannot convert float NaN to integer')
            var_metadata = {'standard_name': variable, 'units': units, 'scale_factor': scale, '_FillValue': miss}
        except ValueError:
            variable, units = _attemptVarAndUnitsMatch(na_dict['XNAME'])
            var_metadata = {'standard_name': variable, 'units': units}
            values = np.array(na_dict['X'])
            if read_as_float:
                values = [float(item) for item in values]
        if file_metadata is not None:
            variable_metadata = egads.core.metadata.VariableMetadata(var_metadata, self.file_metadata)
        else:
            variable_metadata = egads.core.metadata.VariableMetadata(var_metadata)
        data = egads.EgadsData(values, variable_metadata=variable_metadata)
        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - read_variable - varname ' + str(varname)
                      + ' -> data read OK')
        return data

    def write_variable(self, data, varname=None, vartype="main", na_dict=None):
        """
        Write or update a variable in the NASA/Ames dictionary.

        :param EgadsData data:
            Data to be written in the NASA/Ames dictionary. data has to be an EgadsData instance.
        :param string|int varname:
            The name or the sequential number of the variable to be written in the
            dictionary.
        :param string vartype:
            The type of data to read, by default ``main``. Options are ``independant`` for
            independant variables, ``main`` for main variables. ``main`` is the default value.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which the variable will be added. By default,
            na_dict = None and the variable is added to the currently opened dictionary. Only
            mandatory if creating a new file or creating a new dictionary.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - varname ' + str(varname)
                      + '; vartype ' + str(vartype))
        if not na_dict:
            na_dict = self.na_dict
        if vartype == "main":
            try:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(na_dict=na_dict)
                    varnum = var_list.index(varname)
                na_dict['V'][varnum] = data.value.tolist()
            except ValueError:
                value = data.value.tolist()
                if varname is not None:
                    name = varname
                else:
                    try:
                        name = data.metadata["standard_name"]
                    except KeyError:
                        try:
                            name = data.metadata["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The '
                                              'EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                try:
                    units = data.metadata["units"]
                except KeyError:
                    logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The EgadsData object'
                                      ' has no units metadata')
                    raise KeyError('The EgadsData object has no units metadata')
                try:
                    scale = data.metadata["scale_factor"]
                except KeyError:
                    scale = int(1)
                    logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The EgadsData object'
                                  ' has no scale_factor metadata')
                try:
                    miss = data.metadata["_FillValue"]
                except KeyError:
                    try:
                        miss = data.metadata["missing_value"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The EgadsData '
                                          'object has no _FillValue or missing_value metadata')
                        raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
                if miss is not None:
                    value = np.where(np.isnan(value), miss, value)
                na_dict['NV'] += 1
                na_dict['V'].append(value)
                na_dict['VNAME'].append(name + " (" + units + ")")
                na_dict['VMISS'].append(miss)
                na_dict['VSCAL'].append(scale)
        elif vartype == "independant":
            if na_dict['X']:
                na_dict['X'] = data.value.tolist()
            else:
                value = data.value.tolist()
                if varname is not None:
                    name = varname
                else:
                    try:
                        name = data.metadata["standard_name"]
                    except KeyError:
                        try:
                            name = data.metadata["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The '
                                              'EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                try:
                    units = data.metadata["units"]
                except KeyError:
                    logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - The EgadsData object'
                                      'has no units metadata')
                    raise KeyError('The EgadsData object has no units metadata')
                na_dict['NX'] = 1
                na_dict['X'] = value
                na_dict['XNAME'] = name + " (" + units + ")"
        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - write_variable - data write OK')

    def convert_to_netcdf(self, nc_file=None, na_dict=None):
        """
        Convert a NASA/Ames dictionary to a NetCDF file.

        :param string nc_file:
            Optional - String name of the netcdf file to be written. If no filename is passed,
            the function will used the name of the actually opened NASA/Ames file.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be converted. If no dictionary is entered,
            the dictionary currently opened during the open file process will be converted.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - convert_to_netcdf - nc_file ' + str(nc_file))
        if not na_dict:
            na_dict = self.na_dict
        if not nc_file:
            filename, _ = os.path.splitext(self.filename)
            nc_file = filename + '.nc'
        nlhead = int(self.get_attribute_value('NLHEAD', na_dict=na_dict))
        ffi = int(self.get_attribute_value('FFI', na_dict=na_dict))
        title = self.get_attribute_value('MNAME', na_dict=na_dict)
        source = self.get_attribute_value('SNAME', na_dict=na_dict)
        institution = self.get_attribute_value('ORG', na_dict=na_dict)
        authors = self.get_attribute_value('ONAME', na_dict=na_dict)
        history = (str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-'
                   + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':'
                   + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
                   + ' - Converted to NetCDF format using EGADS and NASA Ames class.')
        first_date = (str(self.get_attribute_value('DATE', na_dict=na_dict)[0]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[1]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[2]))
        file_number = int(self.get_attribute_value('IVOL', na_dict=na_dict))
        total_files = int(self.get_attribute_value('NVOL', na_dict=na_dict))
        scom = ''
        ncom = ''
        if isinstance(self.get_attribute_value('SCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('SCOM', na_dict=na_dict):
                scom += i + '\n'
            scom = scom[:-1]
        else:
            scom = self.get_attribute_value('SCOM', na_dict=na_dict)
            if scom[-1:] == '\n':
                scom = scom[:-1]
        if isinstance(self.get_attribute_value('NCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('NCOM', na_dict=na_dict):
                ncom += i + '\n'
            ncom = ncom[:-1]
        else:
            ncom = self.get_attribute_value('NCOM', na_dict=na_dict)
            if ncom[-1:] == '\n':
                ncom = ncom[:-1]
        variable_list = self.get_variable_list(vartype='main', na_dict=na_dict)
        ind_variable_list = self.get_variable_list(vartype='independant', na_dict=na_dict)
        ind_dimension_list = self.get_dimension_list(na_dict=na_dict)
        g = egads.input.EgadsNetCdf(nc_file, 'w')
        g.add_attribute('Conventions', 'CF-1.0')
        g.add_attribute('no_of_nasa_ames_header_lines', nlhead)
        g.add_attribute('file_format_index', ffi)
        g.add_attribute('title', title)
        g.add_attribute('source', source)
        g.add_attribute('special_comments', scom)
        g.add_attribute('normal_comments', ncom)
        g.add_attribute('institution', institution)
        g.add_attribute('authors', authors)
        g.add_attribute('history', history)
        g.add_attribute('first_valid_date_of_data', first_date)
        g.add_attribute('file_number_in_set', file_number)
        g.add_attribute('total_files_in_set', total_files)
        dim_list = []
        for key, _ in ind_dimension_list.items():
            dim_list.append(str(key))
        dim_tuple = tuple(dim_list)
        for var in ind_variable_list:
            g.add_dim(var, ind_dimension_list[var])
            g.write_variable(self.read_variable(var, na_dict=na_dict), var, dim_tuple)
        for var in variable_list:
            g.write_variable(self.read_variable(var, na_dict=na_dict), var, dim_tuple)
        g.close()
        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - convert_to_netcdf - nc_file ' + str(nc_file)
                      + ' -> file conversion OK')

    def convert_to_hdf(self, hdf_file=None, na_dict=None):
        """
        Convert a NASA/Ames dictionary to a Hdf file.

        :param string hdf_file:
            Optional - String name of the hdf file to be written. If no filename is passed,
            the function will used the name of the actually opened NASA/Ames file.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be converted. If no dictionary is entered,
            the dictionary currently opened during the open file process will be converted.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - convert_to_hdf - hdf_file ' + str(hdf_file))
        if not na_dict:
            na_dict = self.na_dict
        if not hdf_file:
            filename, _ = os.path.splitext(self.filename)
            hdf_file = filename + '.h5'
        nlhead = int(self.get_attribute_value('NLHEAD', na_dict=na_dict))
        ffi = int(self.get_attribute_value('FFI', na_dict=na_dict))
        title = self.get_attribute_value('MNAME', na_dict=na_dict)
        source = self.get_attribute_value('SNAME', na_dict=na_dict)
        institution = self.get_attribute_value('ORG', na_dict=na_dict)
        authors = self.get_attribute_value('ONAME', na_dict=na_dict)
        history = (str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-'
                   + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':'
                   + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second)
                   + ' - Converted to NetCDF format using EGADS and NASA Ames class.')
        first_date = (str(self.get_attribute_value('DATE', na_dict=na_dict)[0]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[1]) + '-' +
                      str(self.get_attribute_value('DATE', na_dict=na_dict)[2]))
        file_number = int(self.get_attribute_value('IVOL', na_dict=na_dict))
        total_files = int(self.get_attribute_value('NVOL', na_dict=na_dict))
        scom = ''
        ncom = ''
        if isinstance(self.get_attribute_value('SCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('SCOM', na_dict=na_dict):
                scom += i + '\n'
            scom = scom[:-1]
        else:
            scom = self.get_attribute_value('SCOM', na_dict=na_dict)
            if scom[-1:] == '\n':
                scom = scom[:-1]
        if isinstance(self.get_attribute_value('NCOM', na_dict=na_dict), list):
            for i in self.get_attribute_value('NCOM', na_dict=na_dict):
                ncom += i + '\n'
            ncom = ncom[:-1]
        else:
            ncom = self.get_attribute_value('NCOM', na_dict=na_dict)
            if ncom[-1:] == '\n':
                ncom = ncom[:-1]
        variable_list = self.get_variable_list(vartype='main', na_dict=na_dict)
        ind_variable_list = self.get_variable_list(vartype='independant', na_dict=na_dict)
        ind_dimension_list = self.get_dimension_list(na_dict=na_dict)
        g = egads.input.EgadsHdf(hdf_file, 'w')
        g.add_attribute('Conventions', 'CF-1.0')
        g.add_attribute('no_of_nasa_ames_header_lines', nlhead)
        g.add_attribute('file_format_index', ffi)
        g.add_attribute('title', title)
        g.add_attribute('source', source)
        g.add_attribute('special_comments', scom)
        g.add_attribute('normal_comments', ncom)
        g.add_attribute('institution', institution)
        g.add_attribute('authors', authors)
        g.add_attribute('history', history)
        g.add_attribute('first_valid_date_of_data', first_date)
        g.add_attribute('file_number_in_set', file_number)
        g.add_attribute('total_files_in_set', total_files)
        dim_list = []
        for key, _ in ind_dimension_list.items():
            dim_list.append(str(key))
        dim_tuple = tuple(dim_list)
        for var in ind_variable_list:
            g.add_dim(var, self.read_variable(var, na_dict=na_dict))
        for var in variable_list:
            g.write_variable(self.read_variable(var, na_dict=na_dict), var, dim_tuple)
        g.close()
        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - convert_to_hdf - hdf_file ' + str(hdf_file)
                      + ' -> file conversion OK')

    def _open_file(self, filename, perms):
        """
        Private method for opening NASA Ames file using Nappy API.

        :parm string filename:
            Name of NASA Ames file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """

        logging.debug('egads - nasa_ames_io.py - EgadsNasaAmes - _open_file')
        self.close()
        try:
            self.f = open(filename, mode=perms)
            self.na_dict = self._get_header()
            self.na_dict['X'], self.na_dict['V'] = self._get_variables(filename)
            self.filename = filename
            self.perms = perms

            attr_dict = dict()
            attr_dict['Comments'] = self.na_dict['NCOM']
            attr_dict['SpecialComments'] = self.na_dict['SCOM']
            attr_dict['Organisation'] = self.na_dict['ORG']
            attr_dict['CreationDate'] = self.na_dict['DATE']
            attr_dict['RevisionDate'] = self.na_dict['RDATE']
            attr_dict['Originator'] = self.na_dict['ONAME']
            attr_dict['Mission'] = self.na_dict['MNAME']
            attr_dict['Source'] = self.na_dict['SNAME']
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename, conventions=["NASAAmes"])
        except RuntimeError:
            logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - open_file - RuntimeError, File ' +
                              str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % filename)
        except IOError:
            logging.exception('egads - nasa_ames_io.py - EgadsNasaAmes - open_file - IOError, File ' +
                              str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % filename)

    logging.info('egads - nasa_ames_io.py - EgadsNasaAmes has been loaded')


def _attemptVarAndUnitsMatch(item):
    """
    If it can match variable name and units from the name, it returns
    (var_name, units). Otherwise returns (item, None).
    """

    logging.debug('egads - nasa_ames_io.py - _attemptVarAndUnitsMatch - item ' + str(item))
    match = re.compile("^\s*(.*)\((.+?)\)(.*)\s*$").match(item)
    if match:
        (v1, units, v2) = match.groups()
        var_name = v1 + " " + v2
    else:
        (var_name, units) = (item, None)
    var_name = var_name.strip()
    if ' ()' in var_name:
        var_name = var_name[:var_name.find(' ()')]
    return var_name, units


def isint(value):
    try:
        a = float(value)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


def na_format_information():
    logging.debug('egads - nasa_ames_io.py - na_format_information')
    string = ("The goal of the 'na_format_information' function is to give few information\n"
              + "about the file structure. Please see the following link for details:\n"
              + "    http://badc.nerc.ac.uk/help/formats/NASA-Ames/\n"
              + "\n"
              + "A NASA/Ames file is composed of different elements:\n"
              + "    NLHEAD  FFI\n"
              + "    ONAME\n"
              + "    ORG\n"
              + "    SNAME\n"
              + "    MNAME\n"
              + "    IVOL  NVOL\n"
              + "    DATE  RDATE\n"
              + "    DX\n"
              + "    NIV (not written in NASA/Ames file)\n"
              + "    XNAME\n"
              + "    NV\n"
              + "    VSCAL(1) ... VSCAL(NV)\n"
              + "    VMISS(1) ... VMISS(NV)\n"
              + "    VNAME(1)\n"
              + "    ...\n"
              + "    VNAME(NV)\n"
              + "    NSCOML\n"
              + "    SCOM\n"
              + "    NNCOML\n"
              + "    NCOM\n"
              + "    --- Here start the data ---\n"
              + "\n"
              + "with NLHEAD: number of lines in the header (above the first line of data\n"
              + "     FFI: number of the File Format Index used in the file\n"
              + "     ONAME: list of authors in the format Lastname, Firstname separated by\n"
              + "        an arbitrary character\n"
              + "     ORG: Organisation name (your university, institute or lab). May include\n"
              + "        address and phone number\n"
              + "     SNAME: Source of data (i.e. instrument, set of instruments, observation\n"
              + "        station, platform, model name,...)\n"
              + "     MNAME: Name of mission, campaign, programme, project,...\n"
              + "     IVOL: Total number of files in the current dataset.\n"
              + "     NVOL: Number of this file in your dataset (1 <= IVOL <=  NVOL)\n"
              + "     DATE: Date at which the data recorded in this file begin (YYYY MM DD)\n"
              + "     RDATE: Date at which the data were last revised (YYYY MM DD)\n"
              + "     DX: Independent variable interval identifier\n"
              + "     NIV: Number of independent variables\n"
              + "     XNAME: Name and unit of the independent variable. E.g.: time (s)\n"
              + "     NV: Number of dependent variables\n"
              + "     VSCAL: Scaling factors of the NV dependent variables, in the same order\n"
              + "        as the dependent variables\n"
              + "     VMISS: Missing value identifiers for the dependent variables\n"
              + "     VNAME: Names and units of the NV dependent variables. E.g.: V(n) = temperature (K)\n"
              + "     NSCOML: Number of Special Comment lines including blank lines (= 0\n"
              + "        if no Special Comment is given).\n"
              + "     SCOM: Special Comments. Can expand over any number of lines (equal to NSCOML).\n"
              + "        If the data are collected at a given site, these should include the \n"
              + "        following lines: site name, country, longitude, latitude, height above\n"
              + "        sea level\n"
              + "     NNCOML: Number of Normal Comment lines including blank lines (= 0 if no\n"
              + "        Normal Comment is given)\n"
              + "     NCOM: Normal comments. Can expand on any number of lines (equal to NNCOML)\n"
              + "        The last line(s) are often used for column headers or to indicate how\n"
              + "        the data are displayed (but this is not mandatory). The Normal Comments\n"
              + "        may include some Conditions of Use. They should also include a reference\n"
              + "        to Gaines and Hipskind, 1998 (see the Instructions worksheet)."
              )
    print(string)

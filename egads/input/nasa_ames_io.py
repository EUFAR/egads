__author__ = "ohenry"
__date__ = "2016-11-29 15:38"
__version__ = "1.7"
__all__ = ["NasaAmes"]

import logging
import datetime
import egads
import copy
import re
import os
from egads.input import FileCore
try:
    import nappy
    logging.info('egads - nasa_ames_io.py - nappy has been imported')
    if 'egads' not in nappy.__path__[0]:
        logging.warning('egads - nasa_ames_io.py - EGADS has imported an already installed version of Nappy. If issues occure,'
                        + ' please check the version number of Nappy.')
        print ('EGADS has imported an already installed version of Nappy. If issues occure,'
               + ' please check the version number of Nappy.')
except ImportError:
    logging.exception('egads - nasa_ames_io.py - EGADS couldn''t find Nappy. Please check for a valid installation of Nappy'
                 + ' or the presence of Nappy in third-party software directory.')
    raise ImportError('EGADS couldn''t find Nappy. Please check for a valid installation of Nappy'
                 + ' or the presence of Nappy in third-party software directory.')


class NasaAmes(FileCore):
    """
    EGADS module for interfacing with NASA Ames files. This module adapts the NAPpy 
    library to the file access methods used in EGADS. To keep compatibility with
    Windows, all functions calling CDMS or CDMS2 have been revoked. The user still
    can use egads.thirdparty.nappy functions to have access to CDMS possibilities
    under Linux and Unix.
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
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_filename - filename ' + str(filename) + ', perms' + str(perms))
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    def read_na_dict(self):
        """
        Read the dictionary from currently open NASA Ames file. Method accessible by
        the user to read the dictionary in a custom object.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_na_dict')
        return copy.deepcopy(self.f.getNADict())

    def create_na_dict(self):
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
        dx = [0.0]
        na_dict = {
            "DATE":None,"DX":dx,"FFI":ffi,"IVOL":ivol,"MNAME":None,"NAUXC":None,
            "NAUXV":None,"NCOM":None,"NIV":None,"NLHEAD":nlhead,"NNCOML":None,"NSCOML":None,"NV":0,
            "NVOL":nvol,"NX":0,"NXDEF":None,"ONAME":None,"ORG":None,"RDATE":rdate,"SCOM":None,
            "SNAME":None,"V":[],"VMISS":[],"VNAME":[],"VSCAL":[],"X":[],"XNAME":[]}
        return na_dict

    def read_variable(self, varname):
        """
        Read in variable from currently open NASA Ames file to :class: EgadsData
        object. Any additional variable metadata is additionally read in.

        :param string|int varname:
            String name or sequential number of variable to read in from currently
            open file.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_variable - varname ' + str(varname))
        var_type = "main"
        try:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list()
                varnum = var_list.index(varname)
            variable, units, miss, scale = self.f.getVariable(varnum)
        except ValueError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - read_variable - no main variable called ' + str(varname))
            var_type = "independant"
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(vartype="independant")
                varnum = var_list.index(varname)
            
            variable, units = self.f.getIndependentVariable(varnum)
            miss = None
            scale = None
        variable_metadata = egads.core.metadata.VariableMetadata({'standard_name':variable,
                                                                  'units':units,
                                                                  '_FillValue':miss,
                                                                  'scale_factor':scale},
                                                                  self.file_metadata)
        na_data = self.f.getVariableValues(varnum, var_type)
        data = egads.EgadsData(na_data, variable_metadata)
        logging.debug('egads - nasa_ames_io.py - NasaAmes - read_variable - varname ' + str(varname) + ' -> data read OK')
        return data

    def write_variable(self, data, varname=None, vartype="main", attrdict=None, na_dict=None):
        """
        Write or update a variable in the NASA/Ames dictionary.

        :param list|egadsData data:
            Data to be written in the NASA/Ames dictionary. data can be a list of value or an 
            EgadsData instance.
        :param string|int var_name:
            The name or the sequential number of the variable to be written in the 
            dictionary.
        :param string vartype:
            The type of data to read, by default ``main``. Options are ``independant`` for 
            independant variables, ``main`` for main variables. ``main`` is the default value.
        :param dict attrdict:
            Optional - Dictionary of variable attribute linked to the variable to be written in 
            the dictionary. Mandatory only if data is not an EgadsData instance and is not 
            already present in the dictionary.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which the variable will be added. By default, 
            na_dict = None and the variable is added to the currently opened dictionary. Only 
            mandatory if creating a new file or creating a new dictionary.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_variable - data_type ' + str(type(data)) + 
                      ', vartype ' + str(vartype) + ', na_dict ' + str(na_dict) + ', varname ' + 
                      str(varname) + ', attrdict ' + str(attrdict))
        if na_dict is None:
            if vartype == "main":
                try:
                    if isinstance(varname, int):
                        varnum = varname
                    else:
                        var_list = self.get_variable_list()
                        varnum = var_list.index(varname)
                    if isinstance(data, egads.EgadsData):
                        self.f.V[varnum] = data.value.tolist()
                    else:
                        self.f.V[varnum] = data
                except ValueError:
                    if isinstance(data, egads.EgadsData):
                        value = data.value.tolist()
                        try:
                            name = data.metadata["standard_name"]
                        except KeyError:
                            try:
                                name = data.metadata["long_name"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                                raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                        try:
                            units = data.metadata["units"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                            raise KeyError('The EgadsData object has no units metadata')
                        try:
                            scale = data.metadata["scale_factor"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no scale_factor metadata')
                            raise KeyError('The EgadsData object has no scale_factor metadata')
                        try:
                            miss = data.metadata["_FillValue"]
                        except KeyError:
                            try:
                                miss = data.metadata["missing_value"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no _FillValue or missing_value metadata')
                                raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
                    else:
                        value = data
                        try:
                            name = attrdict["standard_name"]
                        except KeyError:
                            try:
                                name = attrdict["long_name"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                                raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                        try:
                            units = attrdict["units"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                            raise KeyError('The EgadsData object has no units metadata')
                        try:
                            scale = attrdict["scale_factor"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no scale_factor metadata')
                            raise KeyError('The EgadsData object has no scale_factor metadata')
                        try:
                            miss = attrdict["_FillValue"]
                        except KeyError:
                            try:
                                miss = attrdict["missing_value"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no _FillValue or missing_value metadata')
                                raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
                    self.f.NV += 1
                    self.f.V.append(value)
                    self.f.VNAME.append(name + " (" + units + ")")
                    self.f.VMISS.append(miss)
                    self.f.VSCAL.append(scale)
            elif vartype == "independant":
                try:
                    if isinstance(varname, int):
                        varnum = varname
                    else:
                        var_list = self.get_variable_list(vartype=vartype)
                        varnum = var_list.index(varname)
                    if isinstance(data, egads.EgadsData):
                        self.f.X[varnum] = data.value.tolist()
                    else:
                        self.f.X[varnum] = data
                except ValueError:
                    if isinstance(data, egads.EgadsData):
                        value = data.value.tolist()
                        try:
                            name = data.metadata["standard_name"]
                        except KeyError:
                            try:
                                name = data.metadata["long_name"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                                raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                        try:
                            units = data.metadata["units"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                            raise KeyError('The EgadsData object has no units metadata')
                    else:
                        value = data
                        try:
                            name = attrdict["standard_name"]
                        except KeyError:
                            try:
                                name = attrdict["long_name"]
                            except KeyError:
                                logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                                raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                        try:
                            units = attrdict["units"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                            raise KeyError('The EgadsData object has no units metadata')
                    self.f.NX += 1
                    self.f.X.append(value)
                    self.f.XNAME.append(name + " (" + units + ")")
        else:
            if vartype == "main":
                if isinstance(data, egads.EgadsData):
                    value = data.value.tolist()
                    try:
                        name = data.metadata["standard_name"]
                    except KeyError:
                        try:
                            name = data.metadata["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                    try:
                        units = data.metadata["units"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                        raise KeyError('The EgadsData object has no units metadata')
                    try:
                        scale = data.metadata["scale_factor"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no scale_factor metadata')
                        raise KeyError('The EgadsData object has no scale_factor metadata')
                    try:
                        miss = data.metadata["_FillValue"]
                    except KeyError:
                        try:
                            miss = data.metadata["missing_value"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no _FillValue or missing_value metadata')
                            raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
                else:
                    value = data
                    try:
                        name = attrdict["standard_name"]
                    except KeyError:
                        try:
                            name = attrdict["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                    try:
                        units = attrdict["units"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                        raise KeyError('The EgadsData object has no units metadata')
                    try:
                        scale = attrdict["scale_factor"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no scale_factor metadata')
                        raise KeyError('The EgadsData object has no scale_factor metadata')
                    try:
                        miss = attrdict["_FillValue"]
                    except KeyError:
                        try:
                            miss = attrdict["missing_value"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no _FillValue or missing_value metadata')
                            raise KeyError('The EgadsData object has no _FillValue or missing_value metadata')
            
                na_dict['VNAME'].append(name + ' (' + units + ')' )
                na_dict['VMISS'].append(miss)
                na_dict['VSCAL'].append(scale)
                na_dict['NV'] += 1
                na_dict['V'].append(value)
            elif vartype == "independant":
                if isinstance(data, egads.EgadsData):
                    value = data.value.tolist()
                    try:
                        name = data.metadata["standard_name"]
                    except KeyError:
                        try:
                            name = data.metadata["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                    try:
                        units = data.metadata["units"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                        raise KeyError('The EgadsData object has no units metadata')
                else:
                    value = data
                    try:
                        name = attrdict["standard_name"]
                    except KeyError:
                        try:
                            name = attrdict["long_name"]
                        except KeyError:
                            logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no name, standard_name or long_name metadata')
                            raise KeyError('The EgadsData object has no name, standard_name or long_name metadata')
                    try:
                        units = attrdict["units"]
                    except KeyError:
                        logging.exception('egads - nasa_ames_io.py - NasaAmes - write_variable - The EgadsData object has no units metadata')
                        raise KeyError('The EgadsData object has no units metadata')
                    
                na_dict['XNAME'].append(name + ' (' + units + ')' )
                na_dict['NX'] += 1
                na_dict['X'] = value 
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_variable - data write OK')

    def get_variable_list(self, na_dict=None, vartype="main"):
        """ 
        Returns list of all variables in NASA Ames file.
        
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the variable list. By default, 
            na_dict = None and the variable list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_variable_list - vartype ' + str(vartype) +
                      ', na_dict ' + str(na_dict))
        if not na_dict:
            try:
                if vartype == "main":
                    var_list = self.f.getVariables()
                elif vartype == "independant":
                    var_list = self.f.getIndependentVariables()
                elif vartype == "auxiliary":
                    var_list = self.f.getAuxVariables()
                varname = []
                for var in var_list:
                    varname.append(var[0])
            except AttributeError:
                logging.exception('egads - nasa_ames_io.py - NasaAmes - get_variable_list - AttributeError, no ' +
                              'file opened or no na_dict passed.')
                raise AttributeError("ERROR: no file opened or no na_dict passed")
        else:
            varname = []
            if vartype == 'main':
                for i in na_dict['VNAME']:
                    (var, _) = self._attemptVarAndUnitsMatch(i)
                    varname.append(var)
            elif vartype == 'independant':
                for i in na_dict['XNAME']:
                    (var, _) = self._attemptVarAndUnitsMatch(i)
                    varname.append(var)
        return varname
    
    def get_dimension_list(self, vartype="main", na_dict=None):
        """
        Returns a dictionary of all dimensions linked to their variables in NASA Ames dictionary.
        
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the dimension list. By default, 
            na_dict = None and the dimension list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_dimension_list - vartype ' + str(vartype) +
                      ', na_dict ' + str(na_dict))
        dim_dict = {}
        if not na_dict:
            var_list = self.get_variable_list(vartype=vartype)
            for var in var_list:
                varnum = var_list.index(var)
                dim_dict[var] = len(self.f.getVariableValues(varnum, vartype))
        else:
            var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
            for var in var_list:
                varnum = var_list.index(var)
                if vartype == 'main':
                    dim_dict[var] = len(na_dict['V'][varnum])
                if vartype == 'independant':
                    dim_dict[var] = len(na_dict['X'][varnum])
        return dim_dict
    
    def get_attribute_list(self, varname=None, vartype="main", na_dict=None):
        """
        Returns a list of attributes found in current NASA Ames file either globally or
        attached to a given variable, depending on the type
        
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
        :param string| vartype:
            Optional - type of variable to get list of attributes from. If no variable 
            type is provided with the variable name, the function returns an attribute
            of the main variable .
        :param dict na_dict:
            Optional - The NASA/Ames dictionary in which to get the attribute list. By default, 
            na_dict = None and the attribute list is retrieved from the currently opened NASA/Ames 
            file . Only mandatory if creating a new file or creating a new dictionary.
        """

        logging.debug('egads - nasa_ames_io.py - NasaAmes - get_attribute_list - varname ' + str(varname) + 
                      ', vartype ' + str(vartype) + ', na_dict ' + str(na_dict))
        if not na_dict:
            if varname is not None:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(vartype=vartype)
                    varnum = var_list.index(varname)
                attr_list = []
                if vartype == "main":
                    (variable, units, miss, scale) = self.f.getVariable(varnum)
                    if variable is not None:
                        attr_list.append("standard_name")
                    if units is not None:
                        attr_list.append("units")
                    if miss is not None:
                        attr_list.append("_FillValue")
                    if scale is not None:
                        attr_list.append("scale_factor")
                elif vartype == "independant":
                    (variable, units) = self.f.getIndependentVariable(varnum)
                    if variable is not None:
                        attr_list.append("standard_name")
                    if units is not None:
                        attr_list.append("units")
                return attr_list
            else:
                return self.na_dict.keys()
        else:
            if varname is not None:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
                    varnum = var_list.index(varname)
                attr_list = []
                if vartype == "main":
                    try:
                        (variable, units) = self._attemptVarAndUnitsMatch(na_dict["VNAME"][varnum])
                        attr_list.append("standard_name")
                        if units is not None:
                            attr_list.append("units")
                    except (KeyError, ValueError):
                        pass
                    try:
                        _ = na_dict['VMISS'][varnum]
                        attr_list.append("_FillValue")
                    except (KeyError, ValueError):
                        pass
                    try:
                        _ = na_dict['VSCAL'][varnum]
                        attr_list.append("scale_factor")
                    except (KeyError, ValueError):
                        pass
                elif vartype == "independant":
                    try:
                        (variable, units) = self._attemptVarAndUnitsMatch(na_dict["XNAME"][varnum])
                        attr_list.append("standard_name")
                        if units is not None:
                            attr_list.append("units")
                    except (KeyError, ValueError):
                        pass
                return attr_list
            else:
                return self.na_dict.keys()
        
    def get_attribute_value(self, attrname, varname=None, vartype="main", na_dict=None):
        """
        Returns the value of an attribute found in current NASA Ames file either globally 
        or attached to a given variable (only name, units, _FillValue and scale_factor), depending on the type
        
        :param string attrname:
            String name of attribute to write in currently open file.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
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
            if varname is None:
                return self.na_dict[attrname]
            else:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(vartype=vartype)
                    varnum = var_list.index(varname)
                if vartype == "main":
                    vardict = {'standard_name':self.f.getVariable(varnum)[0],
                           'units':self.f.getVariable(varnum)[1],
                           '_FillValue':self.f.getVariable(varnum)[2],
                           'scale_factor':self.f.getVariable(varnum)[3]}
                elif vartype == "independant":
                    vardict = {'standard_name':self.f.getIndependentVariable(varnum)[0],
                           'units':self.f.getIndependentVariable(varnum)[1]}
                return vardict[attrname]
        else:
            if varname is None:
                return na_dict[attrname]
            else:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(na_dict=na_dict, vartype=vartype)
                    varnum = var_list.index(varname)
                if vartype == "main":
                    (variable, units) = self._attemptVarAndUnitsMatch(na_dict["VNAME"][varnum])
                    vardict = {'standard_name':variable,
                               'units':units,
                               '_FillValue':na_dict['VMISS'][varnum],
                               'scale_factor':na_dict['VSCAL'][varnum]}
                elif vartype == "independant":
                    (variable, units) = self._attemptVarAndUnitsMatch(na_dict["XNAME"][varnum])
                    vardict = {'standard_name':variable,
                               'units':units}
                return vardict[attrname]
    
    def write_attribute_value(self,attrname, attrvalue, na_dict=None, varname=None, vartype="main"):
        """
        Write the value of an attribute in current NASA Ames file either globally or
        attached to a given variable (only name, units, _FillValue and scale_factor), 
        depending on the type
        
        :param string| attrname:
            String name of attribute to write in currently open file.
        :param string|int|float attrvalue:
            Value of attribute to write in currently open file.
        :param dict na_dict:
            Optional - dictionary in which the attribute will be added. By default, na_dict = None 
            and the attribute value is added to the currently opened dictionary. Only mandatory 
            if creating a new file or creating a new dictionary.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
        :param string| vartype:
            Optional - type of variable to get list of attributes from. If no variable type     
            is provided with the variable name, the function returns an attribute
            of the main variable .
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_attribute_value - attrname ' + str(attrname) + 
                      ', attrvalue ' + str(attrvalue) + ', varname ' + str(varname) + ', vartype ' +
                       str(vartype) + '; na_dict ' + str(na_dict))
        if na_dict is None:
            if varname is None:
                self.na_dict[attrname] = attrvalue
            else:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list(vartype=vartype)
                    varnum = var_list.index(varname)
                attr_dict = {"standard_name":"NAME", "units":"UNITS", "_FillValue":"VMISS", "scale_factor":"VSCAL"}
                if attr_dict[attrname] == "NAME" or attr_dict[attrname] == "UNITS":
                    if vartype == "main":
                        (variable, units) = self.f._attemptVarAndUnitsMatch(self.na_dict["VNAME"][varnum])
                        if attr_dict[attrname] == "UNITS":
                            self.na_dict["VNAME"][varnum] = variable + " (" + attrvalue + ")"  
                        if attr_dict[attrname] == "NAME":
                            self.na_dict["VNAME"][varnum] = attrvalue + " (" + units + ")"
                    elif vartype == "independant":
                        (variable, units) = self.f._attemptVarAndUnitsMatch(self.na_dict["XNAME"][varnum])
                        if attr_dict[attrname] == "UNITS":
                            self.na_dict["XNAME"][varnum] = variable + " (" + attrvalue + ")"  
                        if attr_dict[attrname] == "NAME":
                            self.na_dict["XNAME"][varnum] = attrvalue + " (" + units + ")"
                else:
                    self.na_dict[attr_dict[attrname]][varnum] = attrvalue
        else:
            if varname is None:
                na_dict[attrname] = attrvalue
            else:
                if isinstance(varname, int):
                    varnum = varname
                else:
                    try:
                        var_list = self.get_variable_list(vartype=vartype, na_dict=na_dict)
                        varnum = var_list.index(varname)
                        attr_dict = {"standard_name":"NAME", "units":"UNITS", "_FillValue":"VMISS", "scale_factor":"VSCAL"}
                        if attr_dict[attrname] == "NAME" or attr_dict[attrname] == "UNITS":
                            if vartype == 'main':
                                (variable, units) = self._attemptVarAndUnitsMatch(na_dict["VNAME"][varnum])
                                if attr_dict[attrname] == "UNITS":
                                    na_dict["VNAME"][varnum] = variable + " (" + attrvalue + ")"  
                                if attr_dict[attrname] == "NAME":
                                    na_dict["VNAME"][varnum] = attrvalue + " (" + units + ")"
                            elif vartype == 'independant':
                                (variable, units) = self._attemptVarAndUnitsMatch(na_dict["XNAME"][varnum])
                                if attr_dict[attrname] == "UNITS":
                                    na_dict["XNAME"][varnum] = variable + " (" + attrvalue + ")"  
                                if attr_dict[attrname] == "NAME":
                                    na_dict["XNAME"][varnum] = attrvalue + " (" + units + ")"
                        else:
                            na_dict[attr_dict[attrname]][varnum] = attrvalue
                        
                    except ValueError:
                        raise ValueError("The variable " + str(varname) + "doesn't exist in " + 
                                         "VNAME or XNAME metadata. Please check your inputs or " +
                                         "create a new variable before.")
            
        logging.debug('egads - nasa_ames_io.py - NasaAmes - write_attribute_value - attribute write OK')

    def save_na_file(self, filename=None, na_dict=None, float_format='%.g', delimiter=None, 
                     annotation=False, no_header=False):
        """
        Save a NASA/Ames dictionary to a file.

        :param string filename:
            String name of the file to be written.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be saved. If no dictionary is entered,
            the dictionary currently opened during the open file process will be saved.
        :param string float_format:
            Optional - The format of numbers to be saved. If no string is entered, values are
            round up to two decimal places.
        :param string delimiter:
            Optional - A character or multiple characters to separate data. By default '    ' (four
            spaces) is used
        :param boolean annotation:
            Optional - If annotation is True then add annotation column to left of file. Default - 
            False.
        :param boolean no_header:
            Optional - If no_header is True then suppress writing the header and only write the 
            data section. Default - False.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - save_na_file - filename ' + str(filename) + 
                      ', float_format ' + str(float_format))
        if not filename:
            filename = self.filename
        if not na_dict:
            na_dict = self.na_dict
        args = {}
        if delimiter:
            args['delimiter'] = delimiter
        if annotation is True:
            args['annotation'] = annotation
        if no_header is True:
            args['no_header'] = no_header
        saved_file = nappy.openNAFile(filename, mode="w", na_dict=na_dict)
        saved_file.write(float_format=float_format, **args)
        saved_file.close()

    def convert_to_netcdf(self, nc_file=None):
        """
        Convert a NASA/Ames dictionary to a NetCDF file.

        :param string nc_file:
            Optional - String name of the netcdf file to be written. If no filename is passed, 
            the function will used the name of the actually opened NASA/Ames file.
        """
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_netcdf - nc_file ' + str(nc_file))
        if not nc_file:
            filename, _ = os.path.splitext(self.filename)
            nc_file = filename + '.nc'
        
        # populate title, source, institution, history, ffi, file_number_in_set, total_files_in_set,
        # first_valid_date_of_data, no_of_nasa_ames_header_lines
        nlhead = int(self.get_attribute_value('NLHEAD'))
        ffi = int(self.get_attribute_value('FFI'))
        title = self.get_attribute_value('MNAME')
        source = self.get_attribute_value('SNAME')
        institution = self.get_attribute_value('ORG')
        authors = self.get_attribute_value('ONAME')
        history = (str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-'
                + str(datetime.datetime.now().day) + ' ' + str(datetime.datetime.now().hour) + ':'
                + str(datetime.datetime.now().minute) + ':' + str(datetime.datetime.now().second) + 
                ' - Converted to NetCDF format using EGADS and Nappy.')
        first_date = (str(self.get_attribute_value('DATE')[0]) + '-' + 
                      str(self.get_attribute_value('DATE')[1]) + '-' +
                      str(self.get_attribute_value('DATE')[2]))
        file_number = int(self.get_attribute_value('IVOL'))
        total_files = int(self.get_attribute_value('NVOL'))
        scom = ''
        ncom = ''
        for i in self.get_attribute_value('SCOM'):
            scom += i + '\n'
        scom = scom[:-1]
        for i in self.get_attribute_value('NCOM'):
            ncom += i + '\n'
        ncom = ncom[:-1]
        variable_list = self.get_variable_list(vartype = 'main')
        ind_variable_list = self.get_variable_list(vartype = 'independant')
        ind_dimension_list = self.get_dimension_list(vartype='independant')
        g = egads.input.EgadsNetCdf(nc_file, 'w')  # @UndefinedVariable
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
        for key, _ in ind_dimension_list.iteritems():
            dim_list.append(str(key))
        dim_tuple = tuple(dim_list)
        for var in ind_variable_list:
            g.add_dim(var, ind_dimension_list[var])
            g.write_variable(self.read_variable(var), var, dim_tuple)
        for var in variable_list:
            g.write_variable(self.read_variable(var), var, dim_tuple)
        g.close()
        logging.debug('egads - nasa_ames_io.py - NasaAmes - convert_to_netcdf - nc_file ' + str(nc_file)
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
        
        logging.debug('egads - nasa_ames_io.py - NasaAmes - open_file - filename ' + str(filename) + 
                      ', perms ' + str(perms))
        self.close()
        try:
            self.f = nappy.openNAFile(filename, mode=perms)
            self.f.readData()
            self.filename = filename
            self.perms = perms
            self.na_dict = self.f.getNADict()
            attr_dict = {}
            attr_dict['Comments'] = self.f.getNormalComments()
            attr_dict['SpecialComments'] = self.f.getSpecialComments()
            attr_dict['Organisation'] = self.f.getOrganisation()
            dates = self.f.getFileDates()
            attr_dict['CreationDate'] = dates[0]
            attr_dict['RevisionDate'] = dates[1]
            attr_dict['Originator'] = self.f.getOriginator()
            attr_dict['Mission'] = self.f.getMission()
            attr_dict['Source'] = self.f.getSource()
            self.file_metadata = egads.core.metadata.FileMetadata(attr_dict, self.filename,
                                                                  conventions="NASAAmes")
        except RuntimeError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.exception('egads - nasa_ames_io.py - NasaAmes - open_file - IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))

    def na_format_information(self):
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
        print string
    
    def _attemptVarAndUnitsMatch(self, item):
        """
        If it can match variable name and units from the name it does and returns
        (var_name, units). Otherwise returns (item, None).
        """
        
        match = re.compile("^\s*(.*)\((.+?)\)(.*)\s*$").match(item)
        if match:
            (v1, units, v2) = match.groups()
            var_name = v1 + " " + v2
        else:
            (var_name, units) = (item, None)   
        return (var_name.strip(), units)
    
    
    logging.info('egads - nasa_ames_io.py - NasaAmes has been loaded')
        
        
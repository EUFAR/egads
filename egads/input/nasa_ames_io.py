__author__ = "ohenry"
__date__ = "$Date:: 2016-11-29 15:38#$"
__version__ = "$Revision:: 104       $"
__all__ = ["NasaAmes"]

import logging
import egads
import copy
from egads.input import FileCore
try:
    import nappy
    if 'egads' not in nappy.__path__[0]:
        logging.warning('EGADS has imported an already installed version of Quantities. If issues occure,'
                        + ' please check the version number of Quantities.')
except ImportError:
    logging.warning('EGADS couldn''t find quantities. Please check for a valid installation of Quantities'
                 + ' or the presence of Quantities in third-party software directory.')


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
        
        logging.debug('egads.input.NasaAmes.get_filename invoked: filename ' + str(filename) + ', perms' + str(perms))
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)

    def read_na_dict(self):
        """
        Read the dictionary from currently open NASA Ames file. Method accessible by
        the user to read the dictionary in a custom object.
        """
        
        logging.debug('egads.input.NasaAmes.read_na_dict invoked')
        return copy.deepcopy(self.f.getNADict())

    def read_variable(self, varname):
        """
        Read in variable from currently open NASA Ames file to :class: EgadsData
        object. Any additional variable metadata is additionally read in.

        :param string|int varname:
            String name or sequential number of variable to read in from currently
            open file.
        """
        
        logging.debug('egads.input.NasaAmes.read_variable invoked: varname ' + str(varname))
        var_type = "main"
        try:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list()
                varnum = var_list.index(varname)
            variable, units, miss, scale = self.f.getVariable(varnum)
            logging.debug('.................................................... main')
        except ValueError:
            logging.debug('.................................................... independant')
            var_type = "independant"
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(vartype="independant")
                varnum = var_list.index(varname)
            
            variable, units = self.f.getIndependentVariable(varnum)
            miss = None
            scale = None
        variable_metadata = egads.core.metadata.VariableMetadata({'name':variable,
                                                                  'units':units,
                                                                  '_FillValue':miss,
                                                                  'scale_factor':scale},
                                                                  self.file_metadata)
        na_data = self.f.getVariableValues(varnum, var_type)
        data = egads.EgadsData(na_data, variable_metadata)
        logging.debug('egads.input.NasaAmes.read_variable invoked: varname ' + str(varname) + ' -> data read OK')
        return data

    def write_variable(self, data, vartype="main", varname=None, attrdict=None):
        """
        Write or update a variable in the NASA/Ames dictionary.

        :param list|egadsData data:
            Data to be written in the NASA/Ames dictionary. data can be a list of value or an 
            EgadsData instance.
        :param string vartype:
            The type of data to read, by default ``main``. Options are ``independant`` for 
            independant variables, ``main`` for main variables. ``main`` is the default value.
        :param string|int var_name:
            Optional - The name or the sequential number of the variable to be written in the 
            dictionary. Only mandatory if data is not an EgadsData Instance.
        :param dict attrdict:
            Optional - Dictionary of variable attribute linked to the variable to be written in 
            the dictionary. Mandatory only if data is not an EgadsData instance and is not 
            already present in the dictionary. 
        """
        
        logging.debug('egads.input.NasaAmes.write_variable invoked: data_type ' + str(type(data)) + 
                      ', vartype ' + str(vartype) + ', varname ' + str(varname) + ', attrdict ' + 
                      str(attrdict))
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
                    name = data.metadata["name"]
                    units = data.metadata["units"]
                    scale = data.metadata["scale_factor"]
                    miss = data.metadata["_FillValue"]
                else:
                    value = data
                    name = attrdict["name"]
                    units = attrdict["units"]
                    scale = attrdict["scale_factor"]
                    miss = attrdict["_FillValue"]
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
                    name = data.metadata["name"]
                    units = data.metadata["units"]
                else:
                    value = data
                    name = attrdict["name"]
                    units = attrdict["units"]
                self.f.NX += 1
                self.f.X.append(value)
                self.f.XNAME.append(name + " (" + units + ")")
        logging.debug('egads.input.NasaAmes.write_variable invoked -> data write OK')

    def get_variable_list(self, vartype="main"):
        """ 
        Returns list of all variables in NASA Ames file.
        
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        """
        
        logging.debug('egads.input.NasaAmes.get_variable_list invoked: vartype ' + str(vartype))
        if vartype == "main":
            var_list = self.f.getVariables()
        elif vartype == "independant":
            var_list = self.f.getIndependentVariables()
        elif vartype == "auxiliary":
            var_list = self.f.getAuxVariables()
        varname = []
        for var in var_list:
            varname.append(var[0])
        logging.debug('................................................varname ' + str(varname))
        return varname
    
    def get_dimension_list(self, vartype="main"):
        """
        Returns list of all dimensions in NASA Ames file.
        
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        """
        
        logging.debug('egads.input.NasaAmes.get_dimension_list invoked: vartype ' + str(vartype))
        dim_list = []
        if vartype == "main":
            var_list = self.f.getVariables()
        elif vartype == "independant":
            var_list = self.f.getIndependentVariables()
        for var in var_list:
            varnum = var_list.index(var)
            dim_list.append(len(self.f.getVariableValues(varnum, vartype)))
        logging.debug('................................................dim_list ' + str(dim_list))
        return dim_list
    
    def get_attribute_list(self, varname=None, vartype="main"):
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
        """

        logging.debug('egads.input.NasaAmes.get_attribute_list invoked: varname ' + str(varname) + ', vartype ' + str(vartype))
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
                    attr_list.append("name")
                if units is not None:
                    attr_list.append("units")
                if miss is not None:
                    attr_list.append("_FillValue")
                if scale is not None:
                    attr_list.append("scale_factor")
            elif vartype == "independant":
                attr_list = ["name","units"]
                (variable, units) = self.f.getIndependentVariable(varnum)
                if variable is not None:
                    attr_list.append("name")
                if units is not None:
                    attr_list.append("units")
            elif vartype == "auxiliary":
                (variable, units, miss, scale) = self.f.getAuxVariable(varnum)
                if variable is not None:
                    attr_list.append("name")
                if units is not None:
                    attr_list.append("units")
                if miss is not None:
                    attr_list.append("_FillValue")
                if scale is not None:
                    attr_list.append("scale_factor")
            logging.debug('................................................attr_list ' + str(attr_list))
            return attr_list
        else:
            logging.debug('................................................self.na_dict.keys() ' + 
                          str(self.na_dict.keys()))
            return self.na_dict.keys()
        
    def get_attribute_value(self, attrname, varname=None, vartype="main"):
        """
        Returns the value of an attribute found in current NASA Ames file either globally 
        or attached to a given variable, depending on the type
        
        :param string| attrname:
            String name of attribute to write in currently open file.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
        :param string| vartype:
            Optional - type of variable to get list of attributes from. If no
            variable type is provided with the variable name, the function returns an 
            attribute of the main variable .
        """
        
        logging.debug('egads.input.NasaAmes.get_attribute_value invoked: attrname ' + str(attrname) + 
                      ', varname ' + str(varname) + ', vartype ' + str(vartype))
        if varname is None:
            logging.debug('................................................self.na_dict[attrname] ' + 
                          str(self.na_dict[attrname]))
            return self.na_dict[attrname]
        else:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(vartype=vartype)
                varnum = var_list.index(varname)
            if vartype == "main":
                vardict = {'name':self.f.getVariable(varnum)[0],
                       'units':self.f.getVariable(varnum)[1],
                       '_FillValue':self.f.getVariable(varnum)[2],
                       'scale_factor':self.f.getVariable(varnum)[3]}
            elif vartype == "independant":
                vardict = {'name':self.f.getIndependentVariable(varnum)[0],
                       'units':self.f.getIndependentVariable(varnum)[1]}
            elif vartype == "auxiliary":
                vardict = {'name':self.f.getAuxVariable(varnum)[0],
                       'units':self.f.getAuxVariable(varnum)[1],
                       '_FillValue':self.f.getAuxVariable(varnum)[2],
                       'scale_factor':self.f.getAuxVariable(varnum)[3]}
            logging.debug('................................................vardict[attrname] ' + 
                          str(vardict[attrname]))
            return vardict[attrname]
    
    def write_attribute_value(self, attrname, attrvalue, varname = None, vartype = "main"):
        """
        Write the value of an attribute in current NASA Ames file either globally or
        attached to a given variable, depending on the type
        
        :param string| attrname:
            String name of attribute to write in currently open file.
        :param string|int|float attrvalue:
            Value of attribute to write in currently open file.
        :param string|int varname:
            Optional - Name or number of variable to get list of attributes from. If no
            variable name is provided, the function returns global attributes.
        :param string| vartype:
            Optional - type of variable to get list of attributes from. If no variable type     
            is provided with the variable name, the function returns an attribute
            of the main variable .
        """
        
        logging.debug('egads.input.NasaAmes.write_attribute_value invoked: attrname ' + str(attrname) + 
                      ', attrvalue ' + str(attrvalue) + ', varname ' + str(varname) + ', vartype ' + str(vartype))
        if varname is None:
            self.na_dict[attrname] = attrvalue
        else:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list(vartype=vartype)
                varnum = var_list.index(varname)
            attr_dict = {"name":"NAME", "units":"UNITS", "_FillValue":"VMISS", "scale_factor":"VSCAL"}
            if attr_dict[attrname] == "NAME" or attr_dict[attrname] == "UNITS":
                if vartype == "main":
                    (variable, units) = self.f._attemptVarAndUnitsMatch(self.na_dict["VNAME"][varnum])
                elif vartype == "independant":
                    (variable, units) = self.f._attemptVarAndUnitsMatch(self.na_dict["XNAME"][varnum])
                elif vartype == "auxiliary":
                    (variable, units) = self.f._attemptVarAndUnitsMatch(self.na_dict["ANAME"][varnum])
                if attr_dict[attrname] == "UNITS":
                    self.na_dict["VNAME"][varnum] = variable + " (" + attrvalue + ")"  
                if attr_dict[attrname] == "NAME":
                    self.na_dict["VNAME"][varnum] = attrvalue + " (" + units + ")"
            else:
                self.na_dict[attr_dict[attrname]][varnum] = attrvalue
        logging.debug('egads.input.NasaAmes.write_attribute_value invoked -> attribute write OK')

    def save_na_file(self, filename=None, na_dict=None, float_format='%.2f'):
        """
        Save a NASA/Ames dictionary to a file.

        :param string filename:
            String name of the file to be writed.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be saved. If no dictionary is entered,
            the dictionary currently opened during the open file process will be saved.
        :param string float_format:
            Optional - The format of numbers to be saved. If no string is entered, values are
            round up to two decimal places.
        """
        
        logging.debug('egads.input.NasaAmes.save_na_file invoked: filename ' + str(filename) + 
                      ', float_format ' + str(float_format))
        if not na_dict:
            na_dict = self.f.na_dict
        saved_file = nappy.openNAFile(filename, mode="w", na_dict=na_dict)
        saved_file.write(float_format=float_format)
        saved_file.close()

    def _open_file(self, filename, perms):
        """
        Private method for opening NASA Ames file using Nappy API.

        :parm string filename:
            Name of NASA Ames file to open.
        :param char perms:
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads.input.NasaAmes.open_file invoked: filename ' + str(filename) + 
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
            logging.error('egads.input.NasaAmes.open_file invoked: RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.error('egads.input.NasaAmes.open_file invoked: IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.error('egads.input.NasaAmes.open_file invoked: Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

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
        
    logging.info('egads.input.NasaAmes has been loaded')
        
        
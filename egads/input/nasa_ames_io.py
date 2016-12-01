__author__ = "ohenry"
__date__ = "$Date:: 2016-11-29 15:38#$"
__version__ = "$Revision:: 101       $"
__all__ = ["NasaAmes"]


import egads
from egads.thirdparty import nappy
from egads.input import FileCore


class NasaAmes(FileCore):
    """
    EGADS module for interfacing with NASA Ames files. This module adapts the NAPpy 
    library to the file access methods used in EGADS
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
        
        self.file_metadata = None
        FileCore.__init__(self, filename, perms)


    def read_na_dict(self):
        """
        Read the dictionary from currently open NASA Ames file. Method accessible by
        the user to read the dictionary in a custom object.
        """
        
        return self.f.getNADict()


    def read_variable(self, varname):
        """
        Read in variable from currently open NASA Ames file to :class: EgadsData
        object. Any additional variable metadata is additionally read in.

        :param string|int varname:
            String name or sequential number of variable to read in from currently
            open file.
        """
        
        var_type = "main"
        try:
            if isinstance(varname, int):
                varnum = varname
            else:
                var_list = self.get_variable_list()
                varnum = var_list.index(varname)
            variable, units, miss, scale = self.f.getVariable(varnum)
        except ValueError:
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
        
        if isinstance(data, egads.EgadsData):
            value = data.value
            name = data.metadata["name"]
            units = data.metadata["units"]
            if vartype == "main":
                scale = data.metadata["scale_factor"]
                miss = data.metadata["_FillValue"]
        else:
            value = data
            name = attrdict["name"]
            units = attrdict["units"]
            if vartype == "main":
                scale = attrdict["scale_factor"]
                miss = attrdict["_FillValue"]
            
        
        if vartype == "main":
            try:
                
                
                if isinstance(varname, int):
                    varnum = varname
                else:
                    var_list = self.get_variable_list()
                    varnum = var_list.index(varname)
                self.f.V[varnum] = value
            except ValueError:
                
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
                self.f.X[varnum] = data
            except ValueError:
                
                self.f.NX += 1
                self.f.X.append(data)
                self.f.XNAME.append(name + " (" + units + ")")


    def get_variable_list(self, vartype="main"):
        """ 
        Returns list of all variables in NASA Ames file.
        
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        """

        if vartype == "main":
            var_list = self.f.getVariables()
        elif vartype == "independant":
            var_list = self.f.getIndependentVariables()
        elif vartype == "auxiliary":
            var_list = self.f.getAuxVariables()
        varname = []
        for var in var_list:
            varname.append(var[0])
        return varname
    
    
    def get_dimension_list(self, vartype="main"):
        """
        Returns list of all dimensions in NASA Ames file.
        
        :param string vartype:
            Optional - the type of data to read
            Options are ``independant`` for independant variables, ``main`` for main variables
            and ``auxiliary`` for auxiliary variables.
        """
        
        dim_list = []
        if vartype == "main":
            var_list = self.f.getVariables()
        elif vartype == "independant":
            var_list = self.f.getIndependentVariables()
        for var in var_list:
            varnum = var_list.index(var)
            dim_list.append(len(self.f.getVariableValues(varnum, vartype)))
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
            return attr_list
        else:
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
        
        if varname is None:
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
    

    def save_na_file(self, filename, na_dict=None):
        """
        Save a NASA/Ames dictionary to a file.

        :param string filename:
            String name of the file to be writed.
        :param dict na_dict:
            Optional - The NASA/Ames dictionary to be saved. If no dictionary is entered,
            the dictionary currently opened during the open file process will be saved.
        """
        
        if not na_dict:
            na_dict = self.f.getNADict()
        saved_file = nappy.openNAFile(filename, mode="w", na_dict=na_dict)
        saved_file.write()
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
            print "ERROR: File %s doesn't exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise


    
        
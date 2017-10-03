"""
var_utils.py
============

A set of utilitiies for handling CDMS variable objects.

"""

# Import python modules
import re

# Import third-party software
from cdms_utils.cdms_compat import *

# Import local modules
import cdms_utils.array_utils as array_utils
import cdms_utils.axis_utils as axis_utils

cdms.setAutoBounds("off")


def cleverSqueeze(var, axes_not_to_squeeze=[]):
    """
    Squeezes out any singleton axes except for those whose ids are in
    axes_not_to_squeeze.
    """
    if axes_not_to_squeeze == []:
        return var(squeeze=1)

    # Now do clever squeezing
    shape = var.shape
    axes = var.getAxisList()

    new_shape = []
    new_axes = []

    slice_list = []

    for axis in axes:
        if axis.id in axes_not_to_squeeze or len(axis) > 1:
            new_shape.append(len(axis))
            new_axes.append(axis)

    new_arr = var.resize(new_shape)
    new_var = cdms.createVariable(new_arr, id=var.id, axes=new_axes,
                         attributes=var.attributes, fill_value=var.getMissing())
    return new_var
         

def areDomainsIdentical(var1, var2):
    """
    Compares two cdms variables to see if they are defined on identical
    axes.
    """
    #check they have the same number of axis
    if len(var1.getAxisList()) != len(var2.getAxisList()):
        return False

    for i in range(len(var1.getAxisList())):
        ax1 = var1.getAxis(i)
        ax2 = var2.getAxis(i)
        #print ax1, ax2
        if axis_utils.areAxesIdentical(ax1, ax2) == False:
            return False

    return True


def addSingletonAxesToVar(var, cdms_axes, reorder=None, verbose=False):
    "Returns a new_var identical to var with any number of singleton axes added at least-changing end."

    for ax in cdms_axes:
        if len(ax) != 1:
            raise Exception("Cannot add non singleton axis to variable, axis " + str(ax.id) + \
                            " has length of " + str(len(ax)) + ".")

    new_axis_list = cdms_axes + var.getAxisList()
    n = len(cdms_axes)
    resize_string = "("
    for i in range(n):
        resize_string = resize_string + "1, "

    resize_string = resize_string + str(var.shape)[1:]
    #print n, ("MA.resize(var, %s)" % resize_string)
    new_array = eval("MA.resize(var._data, %s)" % resize_string)
    #print var.shape, new_array.shape
    new_var = cdms.createVariable(new_array, id=var.id, axes=new_axis_list, attributes=var.attributes)
    if reorder:
        if verbose:  print "Reordering axes:", new_var.getAxisIds()
        new_var = new_var.reorder(reorder)
        if verbose:  print "New axis order:", new_var.getAxisIds()
    return new_var


def makeSingleValueVar(value, id, attributes={}):
    """
    Makes a simple single value variable - typically to be
    referenced in the parent-variable 'coordinates' attribute.
    """
    if type(value) == list or type(value) == N.ndarray:
        raise Exception("Can't create single value variable with value of type " + \
                        str(type(value)) + ".")

    var = cdms.createVariable(value, id=id, axes=[], attributes=attributes)
    return var


def separateSingletonAxesToAuxVars(var, singletons="all"):
    """
    Inputs:
     - var - a cdms variable
     - singletons - either "all" or an ordered list of axis ids of singleton
                    axes to separate out.

    Returns (var_modified, aux_vars) where:
     - var_modified - var with singleton axes removed as required.
            - with "coordinates" attribute added as a space-delimited string of
              singleton axes separated out.
     - aux_vars - a list of auxiliary variables separated out into their own
                  singleton variables.
    """

    print "WORKING ON:", var.id, var.getAxisIds()
    # Get list of singleton axes if not provided as argument
    if singletons == "all":
        singletons = []
        for axis in var.getAxisList():
            if len(axis) == 1:
                singletons.append(axis.id)

    if len(singletons) == 0:
        return (var, [])

    # Now loop through singleton axes to get indices and check they are valid
    axids = var.getAxisIds()
    singleton_indices = []
    for axid in singletons:
        if axid not in axids:
            raise Exception("Axis id of singleton axis not found in variable: '" + axid + "'.")
        singleton_indices.append(axids.index(axid))

    # Now we have the indices we step through them to make single value varaibles
    aux_vars = []
    for i in singleton_indices:
        axis = var.getAxis(i)
        atts = {}
        for (key, value) in  axis.attributes.items():
            if key in ("datatype", "isvar"): continue
            atts[key] = value
        aux_vars.append( makeSingleValueVar(axis[0], id=axis.id, attributes=atts) )

    # Write coordinates string
    if hasattr(var, "coordinates"):
        print "\nWARNING: var has 'coordinates' attribute already so appending to it!"
        ca = var.coordinates
        coordinates_attr = ca + " " + (" ".join(singletons))
    else:
        coordinates_attr = " ".join(singletons)
    var.coordinates = coordinates_attr

    # Remove singleton axes from var if they have been separated out
    var = axis_utils.removeSingletonAxes(var, singletons)
    return (var, aux_vars)


def getBestName(var):
    """
    Returns the most appropriate variable name for a NASA Ames header.
    """
    name = None
    att_order = ("id", "shortname", "name", "title", "standard_name", "long_name")

    # Deal with object that has attributes
    for att in att_order:
        if hasattr(var, att):   name = getattr(var, att)

    # Deal with object that has dictionary lookup - not sure why we do both
    if hasattr(var, "has_key"):
        for att in att_order:
            if var.has_key(att):   name = var[att]

    if hasattr(var, "units") and not re.match("^\s+$", var.units):
        units = var.units.strip()
        name = "%s (%s)" % (name, units)

        if name.count("(%s)" % units) > 1:
            name = name.replace("(%s)" % units, "")  # remove all (units) and start again
            name = "%s(%s)" % (name, units)          # using the space inserted last time

    if name[-2:] == "()": name = name[:-2]
    return name


def getMissingValue(var):
    """
    Returns the missing value or defaults to 1.E20.
    """
    miss = None
    if hasattr(var, "missing_value"):  miss = var.missing_value
    if hasattr(var, "_fill_value"):    miss = var._fill_value
    if hasattr(var, "_FillValue"):     miss = var._FillValue

    if miss == None:
        try:
            miss = var.getMissing()
        except:
            miss = -1.e20

    return miss


def printVar(var):
    """
    Prints: id, shape and axis ids of var.
    """
    for i in ("id", "shape", "axes"):
        try:
            print ("%s: %s" % (i.title(), getattr(var, i))),
        except:
            if i == "axes":
                try:
                    print "Axes:", var.getAxisIds()
                except:
                    pass
                    
                    
def areVariablesEqual(varA, varB):
    """
    Tests if two variables are equal
    
    Tests the data, domains, grids and attributes of the two variables
    """
    equal = True
           
    if equal:        
        equal = areDomainsIdentical(varA, varB)

    if equal:
        equal = isVariableDataEqual(varA, varB)
    
    if equal:        
        equal = areGridsEqual(varA, varB)
        
    if equal:        
        equal = areAttributesEqual(varA, varB)
        
    return equal                    

def isVariableDataEqual(varA, varB):
    """
    Tests if the data contained in two variables is the same
    """
    
    return array_utils.areArraysEqual(varA[:], varB[:])
       
def areGridsEqual(varA, varB):
    """
    Tests if the grids of two variables are the same
    """
    
    varAGrid = varA.getGrid()
    varBGrid = varB.getGrid()
    
    #if one grid exists and the other doesn't
    if (varAGrid == None and varBGrid != None ) or \
       (varAGrid != None and varBGrid == None):
        return False
    #if both have no grids
    elif varAGrid == None and varBGrid == None:
        return True
        
    equal = True
    if equal:
        equal = varAGrid.__class__ == varBGrid.__class__
    
    if equal:
        equal = array_utils.areArraysEqual(varA.getLongitude()[:],
                                           varB.getLongitude()[:])
                                           
    if equal:
        equal = array_utils.areArraysEqual(varA.getLatitude()[:],
                                           varB.getLatitude()[:])
                                               
    return equal
    
def areAttributesEqual(varA, varB):
    """
    Tests if the attribuetes of two variables are the same.
    
    The variable.attributes dictionary contains more entries that the variable.attribues.keys() reveals. The .keys() only shows the public (not starting with '_') attributes.
    """
    if varA.attributes.keys() != varB.attributes.keys():
        return False
        
    for k in varA.attributes.keys():
        if varA.attributes[k] != varB.attributes[k]:
            return False
            
    return True
    

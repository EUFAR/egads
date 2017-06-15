"""
axis_utils.py
=============

A set of utilitiies for handling CDMS axis objects.

"""
# Import python modules

# Import third-party software
try:
   import cdms2 as cdms
except ImportError:
   import cdms

def getAxisById(var, id, alt_ids=[]):
    """
    Takes a cdms variable and an axis id and returns the axis with that id or False 
    if none are found.
    
    Can also provide a list of alternative ids to check if first does not match.
    
    @param       var: the variable to check the axis of
    @type        var: cdms variable
    @param        id: the id of the axis to be returned
    @type         id: string
    @keyword alt_ids: a list of alternative axis id's to search for
    @type    alt_ids: list or strings
    @return         : the matching cdms.axis or False if none found
    @rtype          : cdms.axis
    """
    ax_ids = var.getAxisIds()
    for this_id in [id] + alt_ids:
        if this_id in ax_ids:
            return var.getAxis(ax_ids.index(this_id))
    return False


def areAxesIdentical(ax1, ax2, is_subset=False, check_id=True):
    """
    Takes 2 CDMS axis objects returning True if they are essentially
    the same and False if not.
    
    If is_subset == True then return True if ax1 is same as ax2 except that it is
    only defined on a subset of regularly spaced values within ax2.
    
    If is_subset is used then return value is False or (len(ax2)/len(ax1)).
    
    If check_id == False then don't compare the ids of the axes.
    
    @param         ax1: the first axis to copmair
    @type          ax1: cdms.axis
    @param         ax2: the second axis to compair
    @type          ax2: cdms.axis
    @keyword is_subset: indicates if True should be returned if ax2 is a subset of ax1
    @type    is_subset: bool
    @keyword  check_id: indicates if the id's of the axes should be checked in the comparison
    @type     check_id: bool
    @return           : value indicating if the axis are identicle
    @rtype            : bool
    """
    for axtype in ("time", "level", "latitude", "longitude"):
        if cdms.axisMatches(ax1, axtype) == 1 and not (cdms.axisMatches(ax2, axtype) == 1):
            return False

    # Check ids
    if check_id:
        if ax1.id != ax2.id: return False

    # Check units
    if hasattr(ax1, 'units') or hasattr(ax2, 'units'):
        if ax1.units != ax2.units: return False

    # Do different comparisons depending on 'is_subset' argument
    if is_subset == False:
        # Check lengths and values
        if (len(ax1) != len(ax2)) or \
           (ax1.getData()[:].tolist() != ax2.getData()[:].tolist()): return False

    elif is_subset == True:
        # Check whether values are a subset
        len1 = len(ax1)
        len2 = len(ax2)

        # Check length of 1 divides into length of 2
        if len2 % len1 != 0:
            return False
        # Now test if it is subset
        n = len2 / len1

        for i in range(len(ax1)):
            ax2_value = ax2[n * i]
            test_value = ax1[i]
            if ax2_value != test_value:
                return False

        # If we got here then return len2/len1
        return n

    # OK, I think they are the same axis!
    return True


def createAxis(values, id, units=None, designated=None, standard_name=None,
                   long_name=None, axis=None, positive=None, attributes={}):
    """
    Creates a cdms axis using the supplied parameters.
    
    @param          values: array of values to populate the cdms.axis
    @type           values: numpy.ndarray
    @param              id: the id for the axis
    @type               id: string
    @keyword         units: the units for the new axis
    @type            units: string
    @keyword    designated: the type to designate the new axis as
    @type       designated: string, one of "time", "level", "latitude" or "longitude"
    @keyword standard_name: the standard_name of the new axis
    @type    standard_name: string
    @keyword    long_name : the long name for the new axis
    @type       long_name : string
    @keyword          axis: the axis attribute of the new axis, if 'X', 'Y', 'Z' or 'T' 
        will affect the designation of the axis.
    @type             axis: string
    @keyword      positive: sets the valeu of the axis positive property
    @type         positive: string
    @keyword    attributes: any additional attributes to set on the axis, { name:value,}
    @type       attributes: dictionary
    @return               : a new axis object
    @rtype                : cdms.axis
    """
    ax = cdms.createAxis([float(x) for x in values])
    ax.id = ax.name = id
    if units: ax.units = units
    if designated:
        if designated.lower() not in ("time", "level", "latitude", "longitude"):
            raise Exception('Keyword "designated" must be in ("time", "level", "latitude", "longitude").')
        des = designated.lower().title()
        exec("ax.designate%s()" % des)

    if standard_name: ax.standard_name = standard_name
    if long_name: ax.long_name = long_name
    if axis: ax.axis = axis
    if positive: ax.positive = positive

    # Now set any other attributes given - overriding any others provided
    for key, value in attributes.items():
        setattr(ax, key, value)

    return ax


def removeSingletonAxis(var, axis):
    """
    Finds axis with id == axis and then squeezes it out of variable description.
    Or axis can be an actual axis!
    
    @param  var: the cdms variable to remove the axis of
    @type   var: cmds.variable
    @param axis: the singleton axis to be removed, either an id or an axis object
    @type  axis: string or cmds.axis
    @return    : a copy of the cdms.variable without the singleton axis
    @rtype     : cdms.variable 
    """                              
    slice_string = "["

    for ax in var.getAxisList():
        if cdms.axis.axisMatches(ax, axis):
            if len(ax.getValue()) != 1:
                raise Exception ("Axis is not a singleton axis: " + str(axis))

            s = "0"
        else:
            s = ":"
        slice_string = slice_string + s + ","

    if not slice_string.find("0") > -1:
        raise Exception("Did not find axis matching: " + str(axis))

    slice_string = slice_string[:-1] + "]"
    new_var = eval("var%s" % slice_string)
    return new_var

def removeSingletonAxes(var, axes):
    """
    For all axes where axis with id == axis this squeezes it out of variable description.
    axes is a list of axis ids or actual CDMS axes.
    
    @param  var: the cdms variable to remove the axis of
    @type   var: cmds.variable
    @param axis: the singleton axes to be removed, either a list of ids or axis objects
    @type  axis: list of strings or cmds axes
    @return    : a copy of the cdms.variable without the singleton axes
    @rtype     : cdms.variable
    """
    slice_string = "["
    foundCount = 0

    for ax in var.getAxisList():
        matched = False
        for singleton in axes:
            if cdms.axis.axisMatches(ax, singleton):
                matched = True

        if matched == True:
            if len(ax.getValue()) != 1:
                raise Exception ("Axis is not a singleton axis: " + str(axis))
            foundCount += 1
            s = "0"
        else:
            s = ":"

        slice_string = slice_string + s + ","

    if foundCount == 0:
        raise Exception("Did not find any matching axes to remove.")
    elif foundCount != len(axes):
        raise Exception("Only found %i of %i axes to remove." % (foundCount, len(axes)))

    slice_string = slice_string[:-1] + "]"
    new_var = eval("var%s" % slice_string)
    return new_var

def constructLevelMetadata(var, level_value, level_units):
    """
    Returns (var, singleton_var) where 'var' might be same as the input var
    and 'singleton_var' is None if not needed. However, if the variable was
    defined on a single level only it is common that this function will return
    new_var with the coordinates attribute updated and the singleton_var will
    be a simple single value variable that is referenced by said attribute.
    
    @param var:
    @type var:
    @parma level_value:
    @type level_value:
    @param level_units:
    @type level_utins:
    @return :
    @rtype :
    
    """
    # Do some logic to check if needed
    required = True

    if required:
        singleton_var = makeSingleValueLevelVar(level_value, units=level_units)

        if hasattr(var, "coordinates"):
            raise Exception("Danger: var has 'coordinates' attribute already!")
        var.coordinates = singleton_var.id
        if var.getLevel():
            print "removing ", var.getLevel()
            var = removeSingletonAxis(var, var.getLevel())
            print var.getLevel()
    else:
        singleton_var = None
    return (var, singleton_var)


def makeSingleValueLevelVar(value, units="m", id="height", standard_name="height",
               long_name="height", axis="Z", positive="up", attributes={}):
    """
    Makes a simple single value variable for a singleton level axis to be
    referenced in the parent-variable 'coordinates' attribute.
    """

    var = cdms.createVariable(value, id=id, axes=[], attributes=attributes)
    if units: var.units = units
    if standard_name: var.standard_name = standard_name
    if long_name: var.long_name = long_name
    if axis: var.axis = axis
    if positive: var.positive = positive

    return var


def tidyAxisNames(var):
    """
    Returns variable same but with tidier axis names and cell_methods changed to match.
    """
    cm = False
    ln = False

    if hasattr(var, "cell_methods"):
        cm = var.cell_methods
    if hasattr(var, "long_name"):
        ln = var.long_name

    for ax in var.getAxisList():

        orig = ax.id

        if ax.isLongitude():
            ax.id = "longitude"
            ax.long_name = "Longitude"

        elif ax.isLatitude():
            ax.id = "latitude"
            ax.long_name = "Latitude"
        elif ax.isLevel():
            ax.id = "level"
            ax.long_name = "Vertical Level"
        elif ax.isTime():
            ax.id = "time"
            ax.long_name = "Time"

        # Now fix cell methods and long name if changed id
        if cm and cm.find(orig + ":") > -1:
#            print "Changing cell methods and long names where required: '" + orig  \
#                  +  ":' to '" +  ax.id + ":' ."
            cm = cm.replace(orig + ":", ax.id + ":")
        if ln and ln.find(orig + ":") > -1:
            ln = ln.replace(orig + ":", ax.id + ":")

    if cm: var.cell_methods = cm
    if ln: var.long_name = ln

    return

def isAxisRegularlySpacedSubsetOf(ax1, ax2):
    """
    Returns True if ax1 is same as ax2 except that it is only defined on a
    subset of regularly spaced values within ax2. Otherwise returns False.
    """
    return areAxesIdentical(ax1, ax2, is_subset=True, check_id=False)


def isUniformlySpaced(ax):
    "Returns True is axis values are uniformaly spaced else returns False."
    if len(ax) == 1: return False
    incr = ax[1] - ax[0]

    for i in range(1, len(ax)):
        i1 = ax[i - 1]
        i2 = ax[i]
        if (i2 - i1) != incr:
            return False

    return True

def nudgeSingleValuesToAxisValues(value, axisValues, minBound=None, maxBound=None):
    """
    Takes a value and checks if it is in the axisValues array. If not, it nudges the
    value to the nearest neighbour in axis. It returns the new value twice along
    with a message describing the change.

    minBound and maxBound added as options.
    If a value is outside of minBound or maxBound it is nudged so that it is within.

    @param value:    value to check
    @param axisValues:    array of values
    @param minBound:    minimum return value
    @param minBound:    maxmimum return value
    @return:    nearest neighbour of value
    """
    bounds=False
    reverseBounds=False
    #TODO - rewrite this so it is legible!
    #determine if bounds have been provided and if they are of the form (-30,30)  or (330, 30)
    if minBound!=None and maxBound!=None:
        bounds =True
        if minBound > maxBound:
            reverseBounds = True

    newValue=None

    if value in axisValues:
        newValue=value
    else:
        sortedAxis=[]
        if bounds == True:
           if reverseBounds!=True:
                for i in axisValues:
                    if i >= minBound:
                        if i <= maxBound:
                            sortedAxis.append(i)

           else:
               for i in axisValues:
                   if i >= minBound:
                       sortedAxis.append(i)
                   elif i <= maxBound:
                        sortedAxis.append(i)
        else:
            for i in axisValues:
                sortedAxis.append(i)
        sortedAxis.sort()

        if value<sortedAxis[0]:
            if maxBound:
                if sortedAxis[0] < maxBound:
                    newValue=sortedAxis[0]
                else:
                    newValue=sortedAxis[-1]
            else:
                newValue=sortedAxis[0]

        elif value>sortedAxis[-1]:
            newValue=sortedAxis[-1]
        else:
            for i in range(len(sortedAxis)):
                if i<(len(sortedAxis )-1):
                    (current, nextone)=(sortedAxis[i], sortedAxis[i+1])
                    if current>nextone:
                        tempc=nextone
                        nextone=current
                        current=tempc
                    if value>current and value<nextone:
                        lowergap=value-current
                        uppergap=nextone-value
                        if uppergap==lowergap:
                            newValue=nextone
                        elif uppergap>lowergap:
                            newValue=current
                        elif uppergap<lowergap:
                            newValue=nextone
                        break
        if newValue==None:
            axisType='unknown'
            rtMessage="%s axis selected value '%s' nudged to nearest value in real axis '%s' ;" % (axisType, value, newValue)


    return (newValue)

if __name__ == "__main__":
    print nudgeSingleValuesToAxisValues2(27,[10,40,30,20])
    print nudgeSingleValuesToAxisValues(27,[10,40,30,20],"blah")

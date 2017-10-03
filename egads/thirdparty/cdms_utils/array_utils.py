"""
array_utils.py
==============

Some useful utilities for working with arrays and lists.
"""
# Import python modules

# Import third-party software
try:
   import numpy as N
except:
   import Numeric as N

def getSensibleLimits(values, low=999999999, high=-9999999999, buffer=False):
    """
    Returns sensible range by recursively looking in object.
    
    @param   values: array/list of values to find the range of
    @type    values: numpy.ndarray or a python list
    @param      low: minimum lower bound of the returned range
    @type       low: int, float
    @param     high: maximum upper bound of the returned range
    @type      high: int, flaot
    @keyword buffer: indicates if the buffer should be used                    
    @type    buffer: bool
    @return        : (lower range limit, upper range limit)                                          
    @rtype         : tuple
    """

    #because vlaues could be a numpy array need to check for numpy numeric types
    #as well as int and float.
    numericalTypesList = [int,float]
    numericalTypesList.extend(_getNumpyIntTypesList())
    numericalTypesList.extend(_getNumpyFloatTypesList())

    try: 
        if type(values[0]) not in numericalTypesList:
            for array in values:
                (low, high) = getSensibleLimits(array, low, high)
        else:
            for x in values:
                if x < low:                                                                       
                    low = x
                if x > high:                                                
                    high = x
    except:
        # Assume failure due to no contents in values
        # Just leave high and low as they are.
        pass

    if buffer == True:
            full_range = int(high - low)
            tidy_buffer = 2
                                                                                                  
            while tidy_buffer < (full_range / 10):
                tidy_buffer = tidy_buffer * 2
            low = low - tidy_buffer
            high = high + tidy_buffer
    return (low, high)



def getValuesInRange(start, end, array, isLongitude = False):
    """
    Takes a start and end value and returns the values in the array that are between them.
    If not in range and are the same value then returns [start].

    Special case for dealing with longitude with flag.
    """

    #this flag is used to format returned longitude values
    longitudeNegative = False

    # check all are floats
    array = [float(x) for x in list(array)]

    # Make into floats
    (start, end) = (float(start), float(end))


    if isLongitude == False:
        #check the latitude values are valid
        if not _isValidLatitude(start):
            raise ValueError('Starting latitude range vlaue [' + str(start) + \
                             '] is not valid, should be between -90 and 90.')

        if not _isValidLatitude(end):
            raise ValueError('Ending latitude range vlaue [' + str(end) + \
                             '] is not valid, should be between -90 and 90.')

        if not _isValidLatitudeList(array):
            raise ValueError('Starting latitude range vlaue ' + str(array) + \
                             ' is not valid, should be between -90 and 90.')

    else: # the values are longitude
        #wrap the longitude values so that they are within 0 - 360

        #check to see if any of the values are negative (-180 - 0)
        for lon in array:
            if lon < 0.0:
                longitudeNegative = True

        if start < 0.0: longitudeNegative = True
        if end < 0.0: longitudeNegative = True

        #wrap all values so they are within 0 - 360
        start = _wrapLongitude0To360(start)
        end = _wrapLongitude0To360(end)
        newArray = []
        for v in array:
            newArray.append(_wrapLongitude0To360(v))
        array = newArray

    # rtarray is list sent back
    rtarray=[]

    # if start and end sent as (higher, lower) then reverse
    # only do this for a latitude range
    if not isLongitude and start > end :  (start, end) = (end, start)

    #this is not the most efficent way of doing this
    for i in array:

        isInRange = False

        # Deal with longitude coping with 360 modulo
        # Adjust to get them both in range
        if isLongitude == True:
            isInRange = _inLongitudeRange0To360(i, start,end)

        else: #latitude so only need to do a simple range check
            isInRange = (i >= start and i <= end)

        if isInRange:
            rtarray.append(i)


    if rtarray==[] and start==end:
        rtarray=[start]

    if longitudeNegative:
        newArray = []
        for v in rtarray:
            newArray.append(_wrapLongitude180To180(v))
        rtarray = newArray

    return rtarray


def sortUnique(list1):
    """
    Returns sorted list that removes any duplicates.
    """
    rtlist=[]
    list1.sort()
    for i in list1:
        if i not in rtlist: rtlist.append(i)
    return rtlist


def overlap(list1, list2):
    """
    overlap function - returns a list of overlapping items in list1 and list2.
    Otherwise returns None.
    """
    rtlist=[]
    for i in list1:
        if i in list2: rtlist.append(i)

    if len(rtlist)>0:
        return rtlist
    else:
        return None

        
def areArraysEqual(arrA, arrB, delta=1e-4):
    """
    Tests if two numpy arrays are equal.
    
    Tests the arrays shape, type and data to determine if the arrays are equal.
    
    @param arrA: an array to compare
    @type arrA: numpy.array
    @param arrB: an array to compare
    @type arrB: numpy.array
    @kwarg delta: the threshold value for doing floating point comparisons
    @type arrA: float
    """
    equal = True
    
    if equal:
        equal = _areArrayShapesEqual(arrA, arrB)
    
    if equal:
        equal = _areArrayTypesEqual(arrA, arrB)
    
    if equal:
        equal = _isArrayDataEqual(arrA, arrB, delta)
        
    return equal
    
def _areArrayShapesEqual(arrA, arrB):
    return N.shape(arrA) == N.shape(arrB)    

def _areArrayTypesEqual(arrA, arrB):
    return arrA.dtype == arrB.dtype
    
def _isArrayDataEqual(arrA, arrB, delta=1e-4):

    if not _areArrayTypesEqual(arrA, arrB):
        raise Exception("Array types %s and %s are not equal, cannot compare the array data." % (arrA.dtype, arrB.dtype))
    
    if _isFloatData(arrA):
        return _compareFloatArrays(arrA, arrB, delta)
    else:
        return _compareArraysExactly(arrA, arrB)
        
def _isFloatData(arr):
    return arr.dtype in [float, N.float, N.float128, N.float32, N.float64]
        
def _compareFloatArrays(arrA, arrB, delta=1e-5):

    arrA_flat = arrA.flatten()
    arrB_flat = arrB.flatten()
    
    if len(arrA_flat) != len(arrB_flat):
        raise Exception("Arrays are of different length, can't compare their data")
    
    for i in range(len(arrA_flat)):
        a = arrA_flat[i]
        b = arrB_flat[i]
        
        if (a - delta) < b < (a + delta):
            pass
        else:
            return False
    
    return True
    
def _compareArraysExactly(arrA, arrB):
    arrA_flat = arrA.flatten()
    arrB_flat = arrB.flatten()
    
    if len(arrA_flat) != len(arrB_flat):
        return False
    
    for i in range(len(arrA_flat)):
        a = arrA_flat[i]
        b = arrB_flat[i]
        
        if a != b:
            return False
    
    return True

        
        
#internal functions, not used form outside this module

def _getNumpyIntTypesList():
    return [N.int8, N.int16, N.int32, N.int64]

def _getNumpyFloatTypesList():
    return [N.float32, N.float64, N.float128]

def _wrapLongitude0To360(lon):
    """
    Takes a longitude value and returns a value wrapped to between 0 and 360.

    @param lon: a longitude value
    @type  lon: int, float
    @return   : the longitude value wrapped (if neccessary) to be within the range 0-360
    @rtype    : float
    """

    while lon > 360.0:
        lon = lon - 360.0                                                                            
    while lon < 0.0:
        lon = lon + 360.0

    return lon

def _wrapLongitude180To180(lon):
    """
    Takes a longitude value and returns a value wrapped to between -180 and 180.

    @param lon: a longitude value
    @type  lon: int, float
    @return: the longitude value wrapped (if neccessary) to be within the range 0-360
    @rtype: float
    """

    while lon > 180.0:
        lon = lon - 360.0
    while lon < -180.0:
        lon = lon + 360.0

    return lon

def _isValidLatitudeList(latList):
    """
    checks that all latitudes in a given list are valid (i.e. in the range -90 to 90)      

    @param latList: the latitudes to be checked
    @type  latList: list
    @return: if all of the lattitudes are valid
    @rtype: boolen
    """

    for lat in latList:                                                                           
        if not _isValidLatitude(lat):
            return False

    return True


def _isValidLatitude(lat):
    """
    checks that the latitude given is valid (i.e. in the range -90 to 90)

    @param lat: the value of latitude to be checked
    @type  lat: int or float
    @return: if lat is a valid latitude
    @rtype: boolen                                                                                  
    """
    return lat >= -90.0 and lat <= 90.0

def _inLongitudeRange0To360(val, start, end):
    """
    Checks if a longitude value is within a particular range.

    The longitude values specified must all lie between 0 - 360 or the comparison
    won't work.

    @param   val: the value of longitude (0-360) to be checked
    @type    val: float
    @param start: the value of longitude (0-360) of the start of the range
    @type  start: float
    @param   end: the value of longitude (0-360) of the end of the range
    @type    end: float
    @return: if the value is within the range
    @rtype: boolen
    """
    if start < end:
        return val > start and val < end
    else: # end is before start, need to check outside the range
        #e.g. range between 270 and 30

          # the 0 - 30 bit or the 270 - 360 bit
        return (val < end) or (val > start)

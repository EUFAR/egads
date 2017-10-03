#/urs/bin/env python
"""
test_array_utils.py
"""

# Import python modules
import sys

# Import third-party software
import nose
import nose.tools as nt

try:
    import numpy as N
except:
    import Numeric as N

import cdms_utils.array_utils as array_utils

class TestGetSensibleLimits:
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testArrayWithNoBounds(self):
        a = N.array([1,2,3,4])
        result = array_utils.getSensibleLimits(a)
        assert(result[0] == 1 and result[1] == 4)

    def testCompositeListWithNoBounds(self):
        a = [[1,2,3,4], [5,0,6,7,8,9]]
        result = array_utils.getSensibleLimits(a)
        assert(result[0] == 0 and result[1] == 9)

    def testWithLowerBound(self):
        a = N.array([12.2,3.22,230,43.48])
        result = array_utils.getSensibleLimits(a, low=0.3)
        assert(result[0] == 0.3 and result[1] == 230)

    def testWithUpperBound(self):
        a = [23.42,1.1,.2,4,124.2,44]
        result = array_utils.getSensibleLimits(a, high = 125)
        assert(result[0] == .2 and result[1] == 125)

    def testWithBothBounds(self):
        a = [23.42,1.1,.200,4,124.2,10000000]
        result = array_utils.getSensibleLimits(a, high = 1e8, low=0.3)
        assert(result[0] == .2 and result[1] == 1e8)

    def testUsingBuffer(self):
        a = [2,3,4,5,1,6,34,34.2,134,5,9,2]
        result = array_utils.getSensibleLimits(a, buffer=True)
        assert(result[0] == -15 and result[1] == 150)

    def testUsingBufferWithUpperBound(self):
        a = N.array([2,3,4,5,1,6,34,34.2,134,5,9,2])
        result = array_utils.getSensibleLimits(a, high=200, buffer=True)
        assert(result[0] == -31 and result[1] == 232)


class TestGetValuesInRange:
    """
    Tests the array_utils module getValuesInRange function
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testExceptionWhenValueNotFloat(self):
        #check an execption is thrown when a value wont convert to a float
        nose.tools.assert_raises(ValueError, array_utils.getValuesInRange,
                                12,23,[23.3,42.1,1.1,23, "fifty two"], isLongitude = False)

    def testExceptionWhenEndNotValidLatitude(self):
        #cant have latitude > 90 or < -90
        nose.tools.assert_raises(ValueError, array_utils.getValuesInRange,
                                12,-123,[23.3,42.1,1.1,23, 30], isLongitude = False)

    def testExceptionWhenListHasInvalidLatitude(self):
        #cant have latitude > 90 or < -90
        nose.tools.assert_raises(ValueError, array_utils.getValuesInRange,
                                12,23,[23.3,42.1,1.1,23, 230], isLongitude = False)

    def testLatitudeRangeOfInts(self):
        result = array_utils.getValuesInRange(50, -50,
                                             [2, 4, 8, "16", 32, -2, -4, -6, -32],
                                             isLongitude = False)
        answer = [2,4,8,16,32,-2,-4,-6,-32]
        assert(_areNumericListsEqual(result,answer))
        assert(type(result[2]) == float) # check the result is a float

    def testLatitudeRangeOfFloats(self):
        result = array_utils.getValuesInRange(-7.7,16.3,[24,45,8.78,16.3,32,0,90,-56])
        answer = [8.78,16.3,0.0]
        assert(_areNumericListsEqual(result,answer))

    def testLatitudeRangeOfIntAndFloat(self):
        result = array_utils.getValuesInRange(72.5,45,[54,55,68.78,46.3,72,50])
        answer = [54,55,68.78,46.3,72,50]
        assert(_areNumericListsEqual(result,answer))

    def testLatitudeRangeWithEmptyResult(self):
        result = array_utils.getValuesInRange(70.0,85.0,[24.5,4,8.78,16.3,32,0,-88,57])
        answer = []
        assert(_areNumericListsEqual(result,answer))

    def testWhenStartEqualsEnd(self):
        #odd behaviour when start == end
        result = array_utils.getValuesInRange(-29.5,-29.5,[84,4,8.78,16.3,32,0,-88,-86])
        answer = [-29.5]
        assert(_areNumericListsEqual(result,answer))

    def testLongitudeWithNegativeValues(self):
        result = array_utils.getValuesInRange(-30.3,36.0,
                                             [-30.4,-30.2,4,78.78,16.3,35,0],
                                              isLongitude=True)
        answer = [-30.2,4,16.3,35,0]
        assert(_areNumericListsEqual(result,answer))

    def testLongitudeWithNegativeValuesAndEmptyResult(self):
        result = array_utils.getValuesInRange(-20,-10,
                                             [-30.4,4,8.78,16.3,55,0],
                                             isLongitude=True)
        answer = []
        assert(_areNumericListsEqual(result,answer))

    def testLongitudeWith360PlusValuesWrap(self):
        result = array_utils.getValuesInRange(370,36,
                                             [30.4,4,8.78,16.3,345,0],
                                             isLongitude=True)
        answer = [16.3,30.4]
        assert(_areNumericListsEqual(result,answer))

    def testLongitudeWith360PlusValuesNoWrap(self):
        result = array_utils.getValuesInRange(350.0,390.0,
                                             [4,8.78,16.3,355,0],
                                             isLongitude=True)
        answer = [355,0,4,8.78,16.3]
        assert(_areNumericListsEqual(result,answer))


def test_sortUnique():
    """
    Test the sort unique function.
    """
    result =array_utils.sortUnique([4,3,7,56,3,1.4,'es',4])
    answer = [3,4,7,56,1.4,'es']
    assert(_areListsEqual(result,answer))

    result =array_utils.sortUnique([4,4.0,'4'])
    answer = [4,'4']
    assert(_areListsEqual(result,answer))

    result =array_utils.sortUnique(['a','b','a','c','f','f',1.21,1.22,1.21,1.23])
    answer = ['a','b','c','f',1.21,1.22, 1.23]
    assert(_areListsEqual(result,answer))

    result =array_utils.sortUnique([2,4,6,2,8,5,6,4,0,4,-6])
    answer = [-6,0,2,4,6,8,5]
    assert(_areListsEqual(result,answer))

def test_overlap():
    result = array_utils.overlap([2,3,4,5,6],[5,6,7,8])
    answer = [5,6]
    assert(_areListsEqual(result,answer))

    result = array_utils.overlap([2.21,2.453,2.74,2.57,2.786],[2.453,5.7,2.786])
    answer = [2.453,2.786]
    assert(_areListsEqual(result,answer))

    result = array_utils.overlap(['a','b','c','d'],[1,2,3,4,5])
    assert(result == None)


class TestAreArraysEqual:
    """
    Tests the array_utils module getValuesInRange function
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_001_arrayShapesAreDifferent(self):
        a = N.array(range(10))
        b = N.array(range(10))
        b = b.reshape((2,5))
        nt.assert_false( array_utils.areArraysEqual(a,b))
        
    def test_002_arrayTypesAreDifferent(self):
        a = N.array(range(10), N.float32)
        b = N.array(range(10), N.float64)
        nt.assert_false( array_utils.areArraysEqual(a,b))        
        
    def test_003_arrayDataIsDifferent(self):
        a = N.array([[True, False, True],[False,False,True]])
        b = N.array([[False, False, True],[False,False,True]])
        nt.assert_false( array_utils.areArraysEqual(a,b))
        
        a = N.array(range(10))
        a = a.reshape((2,5))
        b = N.array(range(10))
        b = b.reshape((2,5))
        b[1,4] = 99
        nt.assert_false( array_utils.areArraysEqual(a,b))
        
        a = N.array(N.arange(0.5,10.5,0.25))
        a = a.reshape( (10,4) )
        b = N.array(N.arange(0.5,10.5,0.25))
        b = b.reshape( (10,4) )
        
        b[5,0] = 5.6
        nt.assert_false( array_utils.areArraysEqual(a,b))
        
    def test_004_arraysAreIdenticle(self):
        a = N.array(range(12))
        a = a.reshape((3,4))
        b = N.array(range(12))
        b = b.reshape((3,4))
        nt.assert_true( array_utils.areArraysEqual(a,b))
        
        a = N.array([[False,False,True,True],[False,True,False,True]])
        b = N.array([[False,False,True,True],[False,True,False,True]])
        nt.assert_true( array_utils.areArraysEqual(a,b))       
        
    def test_005_floatArraysAreIdenticle(self):
        a = N.array(N.arange(0.5,10.5,0.25))
        a = a.reshape( (10,4) )
        b = N.array(N.arange(0.5,10.5,0.25))
        b = b.reshape( (10,4) )
        b[5,0] = 5.5 + 1e-6
        nt.assert_true( array_utils.areArraysEqual(a,b))
        b[9,3] = 11.24
        nt.assert_true( array_utils.areArraysEqual(a,b, delta=1.0))
    
###Testing internal functions###

def test__wrapLongitude0To360():
    assert(_floatCompare(array_utils._wrapLongitude0To360(-90.0), 270.0))
    assert(_floatCompare(array_utils._wrapLongitude0To360(-390.0), 330.0))
    assert(_floatCompare(array_utils._wrapLongitude0To360(91.2), 91.2))
    assert(_floatCompare(array_utils._wrapLongitude0To360(361.2),  1.2))
    assert(_floatCompare(array_utils._wrapLongitude0To360(761.2),  41.2))

def test__wrapLongitude180To180():
    assert(_floatCompare(array_utils._wrapLongitude180To180(-90.0), -90.0))
    assert(_floatCompare(array_utils._wrapLongitude180To180(-390.0), -30.0))
    assert(_floatCompare(array_utils._wrapLongitude180To180(91.2), 91.2))
    assert(_floatCompare(array_utils._wrapLongitude180To180(361.2),  1.2))
    assert(_floatCompare(array_utils._wrapLongitude180To180(350.0), -10.0))
    assert(_floatCompare(array_utils._wrapLongitude180To180(761.2),  41.2))

def test___isValidLatitude():
    assert(array_utils._isValidLatitude(-90.0) == True)
    assert(array_utils._isValidLatitude(90.0) == True)
    assert(array_utils._isValidLatitude(50) == True)
    assert(array_utils._isValidLatitude(-45.6) == True)
    assert(array_utils._isValidLatitude(-95.6) == False)
    assert(array_utils._isValidLatitude(-91) == False)
    assert(array_utils._isValidLatitude(90.1) == False)

def test___isValidLatitudeList():
    assert(array_utils._isValidLatitudeList([-90.0,54,54.3,-23.2, 0, 90]) == True)
    assert(array_utils._isValidLatitudeList([90.0,54,54.3,-23.2, 0, -90.1]) == False)

def test__inLongitudeRange0To360():
    assert(array_utils._inLongitudeRange0To360(190.0, 80.2, 200.53) == True)
    assert(array_utils._inLongitudeRange0To360(10.0, 190.0, 50.0) == True)
    assert(array_utils._inLongitudeRange0To360(86.0, 180.0, 256.0) == False)
    assert(array_utils._inLongitudeRange0To360(190.0, 200.0, 180.0) == False)

### Utility functions ###

#These are only used within this module#

def _floatCompare(f1,f2,thres=0.00001):
    """
    compairs two float numbers for equality using a threshold value
    """
    if f1 == f2: return True
    size = (abs(f1) + abs(f2))/2
    return abs((f1-f2)/size) < thres

def _areListsEqual(result,answer):
    """
    compairs the items in two lists
    """
    if len(result) != len (answer):
        return False

    for x in answer:
        if not x in result:
            return False

    return True

def _areNumericListsEqual(result,answer):
    """
    tests if two lists are equal (converts all values to float before comparison)
    """
    if (len(result) != len(answer)):
        return False

    for x in answer:
        x = float(x)
        found = False
        for y in result:
            y = float(y)
            if _floatCompare(x,y):
                found = True
                break

        if not found:
            return False

    return True


# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_array_utils')

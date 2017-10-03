# Import python modules
import nose
import types
import sys
import os

# Import third-party software
try:
    import cdms2 as cdms
    import numpy as N
    import numpy.core.ma as MA
except:
    import cdms
    import Numeric as N
    import MA

import cdms_utils.axis_utils as axis_utils

def test_getAxisById():
    a = N.array([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
    temp = cdms.createVariable(a,id='temp')
    axisX = cdms.createAxis(N.array([10,20,30,40]))
    axisX.id = 'x'
    axisY = cdms.createAxis(N.array([45,55,65,75]))
    axisY.id = 'y'
    temp.setAxisList([axisX, axisY])

    result = axis_utils.getAxisById(temp, 'latitude')
    assert(result == False)
    result = axis_utils.getAxisById(temp, 'latitude',alt_ids=['z','x'])
    assert(result.id == 'x')
    result = axis_utils.getAxisById(temp, 'x', alt_ids=['latitude'])
    assert(result == axisX)
    result = axis_utils.getAxisById(temp, 'x', alt_ids=['y', 'z'])
    assert(result == axisX)

def test_areAxesIdentical():
    axisX = cdms.createAxis(N.array([10,20,30,40]))
    axisX.id = 'x'
    axisX.units = 'm'
    axisY = cdms.createAxis(N.array([45,55,65,75]))
    axisY.id = 'y'
    axisY.units = 'm'

    result = axis_utils.areAxesIdentical(axisX,axisX)
    assert(result == True)

    result = axis_utils.areAxesIdentical(axisX,axisY)
    assert(result == False)

    axisX3 = cdms.createAxis(N.array([10,21,30,40]))
    axisX3.id = 'x'
    axisX3.units = 'm'
    result = axis_utils.areAxesIdentical(axisX,axisX3, check_id=True)
    assert(result == False)

    axisX2 = cdms.createAxis(N.array([10,20,30,40]))
    axisX2.id = 'x2'
    axisX2.units = 'm'
    result = axis_utils.areAxesIdentical(axisX,axisX2, check_id=True)
    assert(result == False)

    result = axis_utils.areAxesIdentical(axisX,axisX2, check_id=False)
    assert(result == True)

    axisX2.units = 'km'
    result = axis_utils.areAxesIdentical(axisX,axisX2, check_id=False)
    assert(result == False)

    axisX2 = cdms.createAxis(N.array([10,20]))
    axisX2.id = 'x'
    axisX2.units = 'm'
    result = axis_utils.areAxesIdentical(axisX,axisX2,is_subset=True)
    assert(result == len(axisX2)/ len(axisX))

    axisX2.id = 'x2'
    result = axis_utils.areAxesIdentical(axisX,axisX2,is_subset=True, check_id=False)
    assert(result == len(axisX2)/ len(axisX))

def test_createAxis():

    resultAxis = axis_utils.createAxis([10.0,20.0,30.0,40.0], 'x')
    assert(resultAxis.getValue().tolist()== [10.0,20.0,30.0,40.0])
    assert(resultAxis.id == 'x')
    assert(resultAxis.name == 'x')

    atts = {'a':'one', 'b':'two', 'c':'three'}

    resultAxis = axis_utils.createAxis([10.0,20.0,30.0,40.0], 'x', units='km',
                                       standard_name='x-lat', long_name='axis x',
                                       designated='longitude', positive = True,
                                       attributes=atts)

    assert(resultAxis.units == 'km')
    assert(resultAxis.standard_name == 'x-lat')
    assert(resultAxis.long_name == 'axis x')
    assert(resultAxis.axis == 'X')
    assert(resultAxis.isLongitude() == True)
    assert(resultAxis.positive == True)
    for key in atts.keys():
        assert(getattr(resultAxis, key) == atts[key])

    #need to test setting the axis separatly to testing the designated as designnating an axis
    #sets the .axis attribute
    resultAxis = axis_utils.createAxis([10.0,20.0,30.0,40.0], 'x', axis='X')

    assert(resultAxis.axis == 'X')
    assert(resultAxis.isLongitude() == True)

class TestRemoveSingletonAxis():
    """
    Tests the axis_utils module removeSingletonAxis function
    """

    def setUp(self):
        a = N.array([[[17, 18, 19, 20],[21,22,23,24],[25, 26, 27, 28],[29, 30, 31, 32]]])
        self.temp = cdms.createVariable(a,id='temp')
        self.axisX = cdms.createAxis(N.array([10,20,30,40]))
        self.axisX.id = 'x'
        self.axisY = cdms.createAxis(N.array([45,55,65,75]))
        self.axisY.id = 'y'
        self.axisZ = cdms.createAxis(N.array([1]))
        self.axisZ.id = 'z'
        self.temp.setAxisList([self.axisZ, self.axisX, self.axisY])


    def tearDown(self):
        self.temp = None

    def testRaiseExceptionWhenRemoveAxisWhichDoesntExist(self):
        #should get an exception if you try to remove an axis that isn't there
        nose.tools.assert_raises(Exception, axis_utils.removeSingletonAxis, self.temp, 'q')

    def testRaiseExceptionWhenRemoveNonSingletonAxis(self):
        #should get an exception if you try to remove an axis that isn't a singleton
        nose.tools.assert_raises(Exception, axis_utils.removeSingletonAxis, self.temp, 'x')

    def testRemoveAxisByName(self):
        resultVar = axis_utils.removeSingletonAxis(self.temp,'z')

        assert(len(resultVar.getAxisList()) == 2) # there are two axis left

        #check that one of the axis is axisX
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisX) or \
               _compareAxes(resultVar.getAxisList()[1],self.axisX) )
        #check that one of the axis is axisY
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisY) or \
               _compareAxes(resultVar.getAxisList()[1],self.axisY) )

    def testRemoveAxisByVariable(self):
        #pass the actual axis object instead of just the id
        resultVar = axis_utils.removeSingletonAxis(self.temp,self.axisZ)

        assert(len(resultVar.getAxisList()) == 2) # there are two axis left

        #check that one of the axis is axisX
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisX) or \
               _compareAxes(resultVar.getAxisList()[1],self.axisX) )
        #check that one of the axis is axisY
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisY) or \
               _compareAxes(resultVar.getAxisList()[1],self.axisY) )


class TestRemoveSingletonAxes:
    """
    Tests the axis_utils module removeSingletonAxes function
    """

    def setUp(self):
        a = N.array([[[29, 30, 31, 32]]])
        self.temp = cdms.createVariable(a,id='temp')
        self.axisX = cdms.createAxis(N.array([10,20,30,40]))
        self.axisX.id = 'x'
        self.axisY = cdms.createAxis(N.array([45]))
        self.axisY.id = 'y'
        self.axisZ = cdms.createAxis(N.array([1]))
        self.axisZ.id = 'z'
        self.temp.setAxisList([self.axisZ, self.axisY, self.axisX])

    def tearDown(self):
        self.temp = None

    def testExceptionWhenRemoveAxisWhichDoesntExist(self):
        #should get an exception if you try to remove an axis that isn't there
        nose.tools.assert_raises(Exception, axis_utils.removeSingletonAxes, self.temp, ['q','z'])

    def testExceptionWhenRemoveNonSigletonAxis(self):
        #should get an exception if you try to remove a non-signleton axes
        nose.tools.assert_raises(Exception, axis_utils.removeSingletonAxes, self.temp, ['x','y'])

    def testRemoveAxesByName(self):
        resultVar = axis_utils.removeSingletonAxes(self.temp,['y','z'])
        assert(len(resultVar.getAxisList()) == 1) # only the x axis left

        #check that the remaining axis is the X axis
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisX))

    def testRemoveAxesByName(self):
        resultVar = axis_utils.removeSingletonAxes(self.temp,['y','z'])
        assert(len(resultVar.getAxisList()) == 1) # only the x axis left

        #check that the remaining axis is the X axis
        assert(_compareAxes(resultVar.getAxisList()[0],self.axisX))

    def testRemoveAxesByVariable(self):
        resultVar = axis_utils.removeSingletonAxes(self.temp,[self.axisZ, self.axisY])
        assert(len(resultVar.getAxisList()) == 1) # only the x axis left

        #check that the remaining axis is the X axis
        assert(_compareAxes(resultVar.getAxisList()[0], self.axisX))


def test_makeSingleValueLevelVar():
    defaults = {'units':'m','id':'height','standard_name':'height', 'long_name':'height',
                'positive':'up','axis':'Z'}
    result = axis_utils.makeSingleValueLevelVar(1)
    #test the default values
    for key in defaults.keys():
        assert(getattr(result, key) == defaults[key])

    args = {'units':'km','id':'width','standard_name':'width', 'long_name':'width',
                'positive':'down','axis':'X'}
    attributes = {'a':1, 'b':2}
    result = axis_utils.makeSingleValueLevelVar(1,attributes=attributes, **args)
    #test the argument values
    for key in args.keys():
        assert(getattr(result, key) == args[key])
    #test the keys
    for key in attributes.keys():
        assert(getattr(result, key) == attributes[key])



class TestConstructLevelMetadata:
    """
    Tests the axis_utils module removeSingletonAxes function
    """

    def setUp(self):
        a = N.array([[[29, 30, 31, 32], [29, 30, 31, 32]]])
        self.temp = cdms.createVariable(a,id='temp')

    def tearDown(self):
        pass

    def testRaisesExceptionWhenCoordinatesAttributeAlreadyExists(self):
        self.temp.coordinates = "exists"
        nose.tools.assert_raises(Exception, axis_utils.constructLevelMetadata, self.temp,1,'km')

    def testGeneratedVariableAttribues(self):
        (result_var, result_singletonVar) = axis_utils.constructLevelMetadata(self.temp,112,'km')

        #the coorinates will now have id height
        assert(self.temp.coordinates == 'height')

        singleton_atts= {'units':'km','id':'height','standard_name':'height',
                        'long_name':'height', 'positive':'up','axis':'Z'}
        for key in singleton_atts.keys():
            assert(getattr(result_singletonVar, key) == singleton_atts[key])

        assert (result_singletonVar.getValue() == 112)

    def testRemovesSingletonLevelAxisIfPresent(self):
        print self.temp.getAxisList()
        axis1 = self.temp.getAxisList()[1]
        axis2 = self.temp.getAxisList()[2]
        self.temp.getAxisList()[0].axis = 'Z' #make a level axis
        print self.temp.getLevel()

        (result_var, result_singletonVar) = axis_utils.constructLevelMetadata(self.temp,1,'km')

        assert(len(result_var.getAxisList()) == 2)
        print result_var.getAxisList()
        #check that the other two axis are still present
        assert(_compareAxes(result_var.getAxisList()[0],axis1) )
        assert(_compareAxes(result_var.getAxisList()[1],axis2) )


def test_constructLevelMetadata():
    a = N.array([[29, 30, 31, 32], [29, 30, 31, 32]])

    temp = cdms.createVariable(a,id='temp')
    temp2 = cdms.createVariable(a,id='temp')
    temp3 = cdms.createVariable(a,id='temp')

    temp2.coordinates = "exists"
    nose.tools.assert_raises(Exception, axis_utils.constructLevelMetadata, temp2,1,'km')

    (result_var, result_singletonVar) = axis_utils.constructLevelMetadata(temp,112,'km')

    #the coorinates will always have id height
    assert(temp.coordinates == 'height')

    singleton_atts= {'units':'km','id':'height','standard_name':'height',
                    'long_name':'height', 'positive':'up','axis':'Z'}
    for key in singleton_atts.keys():
        assert(getattr(result_singletonVar, key) == singleton_atts[key])

    assert (result_singletonVar.getValue() == 112)

    #check that any level axis is removed
    temp3.getAxisList()[0].axis = 'Z'


def test_tidyAxisNames():
    a = N.array([[[[ 1,  2,  3,  4], [ 5,  6,  7,  8], [ 9, 10, 11, 12], [13, 14, 15, 16]],
                  [[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]]]])
    temp = cdms.createVariable(a,id='temp')
    axisX = cdms.createAxis(N.array([10, 20, 30, 40]))
    axisX.id = 'x'
    axisX.axis = 'X' # make the axis a longitude axis
    axisY = cdms.createAxis(N.array([45, 55, 65, 75]))
    axisY.id = 'lat_y'  # make the axis a latitude axis
    axisZ = cdms.createAxis(N.array([1, 2]))
    axisZ.id = 'z'
    axisZ.axis = 'Z' # make a Level axis
    axisT = cdms.createAxis(N.array([12]))
    axisT.axis = 'T' # make a time axis
    axisT.id = 't'
    temp.setAxisList([axisT, axisZ, axisY, axisX])

    axis_utils.tidyAxisNames(temp)
    assert(temp.getLongitude().id == 'longitude' and  \
           temp.getLongitude().long_name =='Longitude')

    assert(temp.getLatitude().id == 'latitude' and  \
           temp.getLatitude().long_name =='Latitude')

    assert(temp.getLevel().id == 'level' and  \
           temp.getLevel().long_name =='Vertical Level')

    assert(temp.getTime().id == 'time' and  \
           temp.getTime().long_name =='Time')

    assert(hasattr(temp, "cell_methods") == False)
    assert(hasattr(temp, "long_name") == False)


    temp2 = cdms.createVariable(a,id='temp')
    axisX = cdms.createAxis(N.array([10, 20, 30, 40]))
    axisX.id = 'x'
    axisX.axis = 'X' # make the axis a longitude axis
    axisY = cdms.createAxis(N.array([45, 55, 65, 75]))
    axisY.id = 'lat_y'  # make the axis a latitude axis
    axisZ = cdms.createAxis(N.array([1, 2]))
    axisZ.id = 'z'
    axisZ.axis = 'Z' # make a Level axis
    axisT = cdms.createAxis(N.array([12]))
    axisT.axis = 'T' # make a time axis
    axisT.id = 't'
    temp2.setAxisList([axisT, axisZ, axisY, axisX])

    temp2.cell_methods = 'x:lat_y:z:something else,t:'
    temp2.long_name = 'some data about x:lat_y:z: at level t:'

    axis_utils.tidyAxisNames(temp2)

    assert(temp2.cell_methods == 'longitude:latitude:level:something else,time:')
    assert(temp2.long_name == 'some data about longitude:latitude:level: at level time:')

def test_isAxisRegularlySpacedSubsetOf():
    axisX = cdms.createAxis(N.array([10, 20, 30, 40]))
    axisX.id = 'x'
    axisX.units = 'm'

    axisX2 = cdms.createAxis(N.array([10, 20]))
    axisX2.units = 'm'
    axisX2.id = 'x2'

    result = axis_utils.isAxisRegularlySpacedSubsetOf(axisX,axisX2)
    assert(result == len(axisX2)/ len(axisX))

def test_isUniformlySpaced():
    axisX = cdms.createAxis(N.array([10, 20, 30, 40]))
    assert(axis_utils.isUniformlySpaced(axisX) == True)

    axisX = cdms.createAxis(N.array([10]))
    assert(axis_utils.isUniformlySpaced(axisX) == False)

    axisX = cdms.createAxis(N.array([10, 11, 13]))
    assert(axis_utils.isUniformlySpaced(axisX) == False)

    axisX = cdms.createAxis(N.array([10, 20.0, 30, 40.0]))
    assert(axis_utils.isUniformlySpaced(axisX) == True)

class TestNudgeSingleValuesToAxisValues:

    def setUp(self):
        sortedArray    = N.array([-2.45, 0.45, 1.345, 8.443, 20.55, 40.33])
        self.unsortedArray  = N.array([10, 40, 30, 20])
        longitudeArray = N.array([280.5, 290.995, 310.2, 340.3,
                                       357.0, 3.4, 5.53 , 18.63, 25.4])

        self.sortedAxis       = cdms.createAxis(sortedArray)
        self.unsortedAxis     = cdms.createAxis(self.unsortedArray)
        self.longitudeAxis    = cdms.createAxis(longitudeArray)

    def tearDown(self):
        self.unsortedArray = None
        self.sortedAxis = None
        self.unsortedAxis = None
        self.longitudeAxis = None

    def test_01_AxisOrderingIsntChanged(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(10, self.unsortedAxis)
        assert(self.unsortedAxis.getValue().tolist() ==
               self.unsortedArray.tolist())

    def test_02_AcceptsArrayAndListInsteadOfAxis(self):
        assert(axis_utils.nudgeSingleValuesToAxisValues(1, self.unsortedAxis.getValue()) == 10)
        assert(axis_utils.nudgeSingleValuesToAxisValues(56.5,
                                                 self.sortedAxis.getValue().tolist()) == 40.33)

    def test_03_UnsortedAxisWithoutBounds(self):
        assert(axis_utils.nudgeSingleValuesToAxisValues(1, self.unsortedAxis) == 10)
        assert(axis_utils.nudgeSingleValuesToAxisValues(52, self.unsortedAxis) == 40)
        assert(axis_utils.nudgeSingleValuesToAxisValues(27, self.unsortedAxis) == 30)
        assert(axis_utils.nudgeSingleValuesToAxisValues(22, self.unsortedAxis) == 20)

    def test_04_SortedAxisWithoutBounds(self):
        assert(axis_utils.nudgeSingleValuesToAxisValues(-3.44, self.sortedAxis) == -2.45)
        assert(axis_utils.nudgeSingleValuesToAxisValues(56.5, self.sortedAxis) == 40.33)
        assert(axis_utils.nudgeSingleValuesToAxisValues(1.1, self.sortedAxis) == 1.345)
        assert(axis_utils.nudgeSingleValuesToAxisValues(30.0, self.sortedAxis) == 20.55)

    def test_05_LongitudeAxisWithoutBounds(self):
        assert(axis_utils.nudgeSingleValuesToAxisValues(260.54, self.longitudeAxis) == 280.5)
        assert(axis_utils.nudgeSingleValuesToAxisValues(100.0, self.longitudeAxis) == 25.4)
        assert(axis_utils.nudgeSingleValuesToAxisValues(330.6, self.longitudeAxis) == 340.3)
        assert(axis_utils.nudgeSingleValuesToAxisValues(295.0, self.longitudeAxis) == 290.995)

    def test_06_SortedAxisWithBoundsBelowLowestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(-5.5, self.sortedAxis,
                                               minBound = -5.0, maxBound= 25.5)
        assert(result == -2.45)

    def test_07_SortedAxisWithBoundsAboveHighestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(40.5, self.sortedAxis,
                                               minBound = -5.0, maxBound= 25.5)
        assert(result == 20.55)

    def test_08_SortedAxisWithBoundsJustBelowHighestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(25.4, self.sortedAxis,
                                               minBound = -5.0, maxBound= 25.5)
        assert(result == 20.55)

    def test_09_SortedAxisWithBoundsBetweenBounds(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(-0.24, self.sortedAxis,
                                               minBound = -5.0, maxBound= 25.5)
        assert(result == 0.45)

    def test_10_LongitudeAxisWithBoundsAboveHighestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(60.5, self.longitudeAxis,
                                               minBound = 250.0, maxBound= 40.5)
        assert(result == 25.4)

    def test_11_LongitudeAxisWithBoundsBelowLowestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(240.5, self.longitudeAxis,
                                               minBound = 250.0, maxBound= 40.5)
        assert(result == 280.5)

    def test_12_LongitudeAxisWithBoundsWithinBounds(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(290.7, self.longitudeAxis,
                                               minBound = 250.0, maxBound= 40.5)
        assert(result == 290.995)

    def test_13_LongitudeAxisWithBoundsJustAboveLowestBound(self):
        result = axis_utils.nudgeSingleValuesToAxisValues(251.0, self.longitudeAxis,
                                               minBound = 250.0, maxBound= 40.5)
        assert(result == 280.5)

# utility functions only used by the above tests

def _compareAxes(axisA, axisB):

    #check the data ascociated with the axis
    if axisA.getValue().tolist() != axisB.getValue().tolist():
        #print "axis values dont match",  axisA.getValue().tolist(), axisB.getValue().tolist()
        return False

    #check the attributes of the axis
    for key in dir(axisA):
        if key[0] == '_': #ignore private attributes
            continue
        attA = getattr(axisA,key)
        if type(attA) == types.MethodType: #ignore methods
            continue
        #print key, type(getattr(axisA,key)), getattr(axisA,key)
        if getattr(axisA, key) != getattr(axisB,key): #compair the public attributes
            #print "attribute:", key, "doesn't match ", \
            #       getattr(axisA, key), ",", getattr(axisB,key)
            return False

    return True


# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_axis_utils')

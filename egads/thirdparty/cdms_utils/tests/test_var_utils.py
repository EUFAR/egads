# Import python modules
import sys
import os

# Import third-party software
import nose
import nose.tools as nt

try:
   import cdms2 as cdms
   import numpy as N
except:
   import cdms
   import Numeric as N

import cdms_utils.var_utils as var_utils
import cdms_utils.axis_utils as axis_utils

class TestAreDomainsIdenticle:
    """
    tests teh var_utils.areDomainsIdenticle function
    """

    def setUp(self):
        a = N.array([[29, 30], [29, 30]])
        self.v1 = cdms.createVariable(a,id='v1')
        self.v2 = cdms.createVariable(a,id='v2')
        b = N.array([[[29, 30], [ 9, 30]], [[29, 30], [ 9, 30]] ])
        self.v3 = cdms.createVariable(b,id='v2')
        self.axisX = axis_utils.createAxis(N.array([10, 20]), 'x', units='m', axis='X')
        self.axisY = axis_utils.createAxis(N.array([10, 20]), 'y', units='m', axis='Y')
        self.axisZ = axis_utils.createAxis(N.array([10, 20]), 'z', units='m', axis='Z')
        self.axisX2 = axis_utils.createAxis(N.array([10, 25]), 'x', units='km', axis='X')


    def tearDown(self):
        pass

    def testReturnsTrueForMatchingDomains(self):
        self.v1.setAxisList([self.axisY, self.axisX])
        self.v2.setAxisList([self.axisY, self.axisX])
        #print var_utils.areDomainsIdentical(self.v1, self.v2)
        assert ( var_utils.areDomainsIdentical(self.v1, self.v2) == True)

    def testReturnsFalseForNonMatchingDomains(self):
        self.v1.setAxisList([self.axisY, self.axisX])
        self.v2.setAxisList([self.axisY, self.axisX2])
        assert ( var_utils.areDomainsIdentical(self.v1, self.v2) == False)

    def testReturnsFalseForVarsWithDifferntNumbersOfAxis(self):
        self.v1.setAxisList([self.axisY, self.axisX])
        self.v3.setAxisList([self.axisY, self.axisX, self.axisZ])
        assert ( var_utils.areDomainsIdentical(self.v1, self.v3) == False)


class TestAddSingletonAxesToVar:

    def setUp(self):
        a = N.array([20,21,22])
        self.var = cdms.createVariable(a, id='v1')
        self.axisX  = axis_utils.createAxis(N.array([1,2,3]), 'x', units='m', axis='X')
        self.axisY  = axis_utils.createAxis(N.array([1]),     'y', units='m', axis='Y')
        self.axisZ  = axis_utils.createAxis(N.array([1]),     'z', units='m', axis='Z')
        self.axisY2 = axis_utils.createAxis(N.array([1,2]),   'y', units='m', axis='Y')
        self.var.setAxisList([self.axisX])

    def tearDown(self):
        self.var = None
        self.axisX = None
        self.axisY = None
        self.axisZ = None
        self.axisY2 = None

    def testAddsTwoSingletonAxes(self):
        resultVar = var_utils.addSingletonAxesToVar(self.var, [self.axisY, self.axisZ])
        #check that the axis have been added to the start
        assert(resultVar.getOrder() == 'yzx')
        resultAxes = resultVar.getAxisList()
        assert(axis_utils.areAxesIdentical(resultAxes[0], self.axisY))
        assert(axis_utils.areAxesIdentical(resultAxes[1], self.axisZ))
        assert(axis_utils.areAxesIdentical(resultAxes[2], self.axisX))

    def testAddAxisReorder(self):
        resultVar = var_utils.addSingletonAxesToVar(self.var, [self.axisY, self.axisZ],
                                                    reorder='xyz')
        assert(resultVar.getOrder() == 'xyz')
        print resultVar.getAxisIds()
        assert(resultVar.getAxisIds() == ['x','y','z'])
        resultAxes = resultVar.getAxisList()
        assert(axis_utils.areAxesIdentical(resultAxes[0], self.axisX))
        assert(axis_utils.areAxesIdentical(resultAxes[1], self.axisY))
        assert(axis_utils.areAxesIdentical(resultAxes[2], self.axisZ))

    def testRaisesExceptionWhenAddingNonSingletonAxis(self):
        nose.tools.assert_raises(Exception,
                                 var_utils.addSingletonAxesToVar,
                                 self.var, [self.axisY2, self.axisZ])


class TestMakeSingleValueVar:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMakesSingleValueVar(self):
        singleValVar = var_utils.makeSingleValueVar(12.2, 's', attributes={'test':True})
        assert(singleValVar.getValue() == 12.2)
        assert(singleValVar.getAxisList() == [])
        assert(singleValVar.test == True)
        assert(singleValVar.id == 's')

    def testRaisesExceptionWhenValueGivenIsNotASingleValue(self):
        nose.tools.assert_raises(Exception,
                                 var_utils.makeSingleValueVar,
                                 N.array([12.3,14.4]), 's', attributes={'test':True})


class TestSeparateSingletonAxesToAuxVars:

    def setUp(self):
        a = N.array([ [ [ [29, 30], [ 9, 30] ] ] ])
        self.v = cdms.createVariable(a,id='v')
        self.axisX = axis_utils.createAxis(N.array([10, 20]), 'x', units='m', axis='X')
        self.axisY = axis_utils.createAxis(N.array([10, 20]), 'y', units='m', axis='Y')
        self.axisZ = axis_utils.createAxis(N.array([1])     , 'z', units='m', axis='Z')
        self.axisT = axis_utils.createAxis(N.array([100])     , 't', units='s', axis='T')
        self.v.setAxisList([self.axisT, self.axisZ, self.axisX, self.axisY])

    def tearDown(self):
        pass

    def testSeparatesSingletonAxes(self):
        (resultVar, resultAuxVar) = var_utils.separateSingletonAxesToAuxVars(self.v)
        #test the variable has been reduced
        assert((2,2) == N.shape(resultVar.getValue()))
        #test the x and y axis remain
        resultAxes = resultVar.getAxisList()
        assert(axis_utils.areAxesIdentical(resultAxes[0], self.axisX))
        assert(axis_utils.areAxesIdentical(resultAxes[1], self.axisY))

        #check the aux variables
        assert(resultAuxVar[0].id         == self.axisT.id)
        assert(resultAuxVar[0].getValue() == self.axisT[:])

        assert(resultAuxVar[1].id         == self.axisZ.id)
        assert(resultAuxVar[1].getValue() == self.axisZ[:])

        #check the coordinates variable
        assert(resultVar.coordinates == "t z")

    def testCoordinatesAttributeIsAppendedTo(self):
        self.v.coordinates = "initial value"
        (resultVar, resultAuxVar) = var_utils.separateSingletonAxesToAuxVars(self.v)
        assert(resultVar.coordinates == "initial value t z")

    def testOnlyRemovesNamedAxis(self):
        (resultVar, resultAuxVar) = var_utils.separateSingletonAxesToAuxVars(self.v,
                                                          singletons=[self.axisZ.id])
        #test the variable has been reduced
        assert((1,2,2) == N.shape(resultVar.getValue()))
        #test the x and y axis remain
        resultAxes = resultVar.getAxisList()
        assert(axis_utils.areAxesIdentical(resultAxes[0], self.axisT))
        assert(axis_utils.areAxesIdentical(resultAxes[1], self.axisX))
        assert(axis_utils.areAxesIdentical(resultAxes[2], self.axisY))

        #check the aux variables
        assert(resultAuxVar[0].id         == self.axisZ.id)
        assert(resultAuxVar[0].getValue() == self.axisZ[:])

        #check the coordinates variable
        assert(resultVar.coordinates == "z")

class TestGetBestName:

    def setUp(self):
        a = N.array([1,2,3])
        self.var = cdms.createVariable(a)
        delattr(self.var, "name") # delete the default name
        self.something = "else"
        self.coordinates = "x"
        self.d = {"axis":"xyz", "something":"else"}

    def tearDown(self):
        pass

    def testGetsNameFromCDMSVarByAttributesInOrder(self):

        attributesInReversePriorityOrder = ["id", "shortname", "name", "title",
                                            "standard_name", "long_name"]

        for att in attributesInReversePriorityOrder:
            newValue = att + " value"
            setattr(self.var, att, newValue)
            print newValue, var_utils.getBestName(self.var)
            assert(var_utils.getBestName(self.var) == newValue)

    def testGetsNameFromDictionary(self):
        self.d["shortname"] = "a good name"
        assert(var_utils.getBestName(self.d) == "a good name")
        self.d["title"] = "a better name"
        assert(var_utils.getBestName(self.d) == "a better name")

    def testAppendsUnitsToName(self):
        self.var.standard_name = "Average Wind Speed"
        self.var.units = "m/s"
        assert(var_utils.getBestName(self.var) == "Average Wind Speed (m/s)")

    def testRemovesUnitsIfAlreadyInName(self):
        self.var.name = "Average Wind Speed(m/s)"
        self.var.units = "m/s"
        print var_utils.getBestName(self.var)
        assert(var_utils.getBestName(self.var) == "Average Wind Speed (m/s)")

class TestGetMissingValue:

    def setUp(self):
        self.var = mock()

    def tearDown(self):
        pass

    def testCheckMissingValueAttribute(self):
        self.var.missing_value = 976
        assert(var_utils.getMissingValue(self.var) == 976)

    def testChecksFillValue(self):
        self.var.missing_value = 976
        self.var._fill_value = 23.455
        assert(var_utils.getMissingValue(self.var) == 23.455)
        self.var._FillValue = 450.002
        assert(var_utils.getMissingValue(self.var) == 450.002)

    def testChecksGetMissingFunction(self):
        self.var.getMissing = lambda : 34.345
        print self.var.getMissing()
        assert(var_utils.getMissingValue(self.var) == 34.345)

    def testDefaultValue(self):
        assert(var_utils.getMissingValue(self.var) == -1.e20)

class TestAreVariablesEqual(object):

    def setUp(self):
        self.x = cdms.createAxis([3.0,2.0,1.0], id='x')
        self.y = cdms.createAxis([5.0,10.0], id='y')
        self.z = cdms.createAxis(range(2), id='y')
        
        
        self.arr = N.array(range(6))
        self.arr = self.arr.reshape((3,2))

    def tearDown(self):
        pass

    def test_001_dataDifferent(self):
        v1 = cdms.createVariable(self.arr)
        arr2 = self.arr
        arr2[1,0] = 200
        v2 = cdms.createVariable(arr2)
        nt.assert_false( var_utils.areVariablesEqual(v1, v2))
        
    def test_002_domainsDifferent(self):
        v1 = cdms.createVariable(self.arr, axes=[self.x, self.y])
        v2 = cdms.createVariable(self.arr, axes=[self.x, self.z])
        nt.assert_false( var_utils.areVariablesEqual(v1, v2))
        
    def test_003_gridsDifferent(self):
        
        latArr = N.array([[56.,58.],[54.,56.],[52.,54.]])
        lonArr = N.array([[-14.,-10.],[-12.,-8.],[-10.,-6.]])

        lon = cdms.coord.TransientAxis2D(lonArr, axes=[self.x, self.y])
        lon.id = 'lon'
        lat = cdms.coord.TransientAxis2D(latArr, axes=[self.x, self.y])
        lat.id = 'lat'
        
        grid1 = cdms.hgrid.TransientCurveGrid(lat, lon)
        #adding the x and y axis to the transient grid changes them so you need to retrieve them from the grid to make sure they match
        x, y = grid1.getAxisList()
        grid2 = cdms.createRectGrid(y, x, 'yx')
        
        v1 = cdms.createVariable(self.arr, axes=[x, y], grid=grid1)
        v2 = cdms.createVariable(self.arr, axes=[x, y], grid=grid2)
        
        nt.assert_false( var_utils.areVariablesEqual(v1, v2))
        
        
    def test_004_attributesDifferent(self):
        v1 = cdms.createVariable(self.arr, attributes={'name':'v1'})
        v2 = cdms.createVariable(self.arr, attributes={'name':'v2'})
        
        nt.assert_false( var_utils.areVariablesEqual(v1, v2))
        
    def test_005_areTheSame(self):
        grid = cdms.createRectGrid(self.y, self.x, 'yx')
        
        v1 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid,
                                 attributes={'name':'v1'})
        v2 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid,
                                 attributes={'name':'v1'})
        
        nt.assert_true( var_utils.areVariablesEqual(v1, v2))
        
class TestIsVariablesDataEqual(object):
    
    def test_001_dataIsEqual(slef):
        arr = N.arange(10.0, 20.0, 0.25)
        arr = arr.reshape(8,5)
        
        v1 = cdms.createVariable(arr, id='v1')
        v2 = cdms.createVariable(arr, id='v2')
        nt.assert_true( var_utils.isVariableDataEqual(v1,v2))
        
    def test_002_dataIsNotEqual(self):
        arr = N.arange(10.0, 20.0, 0.25)
        arr = arr.reshape(8,5)
        v1 = cdms.createVariable(arr, id='v1')
        
        arr = N.arange(10.0, 20.0, 0.25)
        arr = arr.reshape(8,5)
        arr[5,2] = 18.25
        v2 = cdms.createVariable(arr, id='v2')

        nt.assert_false( var_utils.isVariableDataEqual(v1,v2))        
        
class TestAreGridsEqual(object):
    def setUp(self):
        self.x = cdms.createAxis([3.0,2.0,1.0], id='x')
        self.y = cdms.createAxis([5.0,10.0], id='y')
        
        self.arr = N.array(range(6))
        self.arr = self.arr.reshape((3,2))

    def tearDown(self):
        pass

    def test_001_gridTypesDifferent(self):
        
        latArr = N.array([[56.,58.],[54.,56.],[52.,54.]])
        lonArr = N.array([[-14.,-10.],[-12.,-8.],[-10.,-6.]])

        lon = cdms.coord.TransientAxis2D(lonArr, axes=[self.x, self.y])
        lon.id = 'lon'
        lat = cdms.coord.TransientAxis2D(latArr, axes=[self.x, self.y])
        lat.id = 'lat'
        
        grid1 = cdms.hgrid.TransientCurveGrid(lat, lon)
        #adding the x and y axis to the transient grid changes them so you need to retrieve them from the grid to make sure they match
        x, y = grid1.getAxisList()
        grid2 = cdms.createRectGrid(y, x, 'yx')
        
        v1 = cdms.createVariable(self.arr, axes=[x, y], grid=grid1)
        v2 = cdms.createVariable(self.arr, axes=[x, y], grid=grid2)
        
        nt.assert_false( var_utils.areGridsEqual(v1, v2))
        
    def test_002_gridLongitudeDifferent(self):
        
        latArr = N.array([[56.,58.],[54.,56.],[52.,54.]])
        lonArr  = N.array([[-14.,-10.],[-12.,-8.],[-10.,-6.]])
        lonArr2 = N.array([[-14., 50.],[-12.,-8.],[-10.,-6.]])

        lon  = cdms.coord.TransientAxis2D(lonArr, axes=[self.x, self.y])
        lon.id = 'lon'
        lon2 = cdms.coord.TransientAxis2D(lonArr2, axes=[self.x, self.y])
        lon2.id = 'lon'
        lat = cdms.coord.TransientAxis2D(latArr, axes=[self.x, self.y])
        lat.id = 'lat'
        
        grid1 = cdms.hgrid.TransientCurveGrid(lat, lon)
        #adding the x and y axis to the transient grid changes them so you need to retrieve them from the grid to make sure they match
        x, y = grid1.getAxisList()
        grid2 = cdms.hgrid.TransientCurveGrid(lat, lon2)
        x2, y2 = grid2.getAxisList()
        
        v1 = cdms.createVariable(self.arr, axes=[x, y], grid=grid1)
        v2 = cdms.createVariable(self.arr, axes=[x2, y2], grid=grid2)
        
        nt.assert_false( var_utils.areGridsEqual(v1, v2))
        
    def test_003_gridLatitudeDifferent(self):
        
        grid1 = cdms.createRectGrid(self.y, self.x, 'yx')
        y2 = cdms.createAxis([8.0,10.0], id='y')
        grid2 = cdms.createRectGrid(y2, self.x, 'yx')
                        
        v1 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid1)
        v2 = cdms.createVariable(self.arr, axes=[self.x, y2], grid=grid2)
        
        nt.assert_false( var_utils.areGridsEqual(v1, v2))
        
    def test_004_oneGridMissing(self):
        grid1 = cdms.createRectGrid(self.y, self.x, 'yx')
                
        v1 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid1)
        v2 = cdms.createVariable(self.arr)
        
        nt.assert_false( var_utils.areGridsEqual(v1, v2))
        nt.assert_false( var_utils.areGridsEqual(v2, v1))
        
    def test_005_gridsAreTheSame(self):
        grid1 = cdms.createRectGrid(self.y, self.x, 'yx')
                
        v1 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid1)
        v2 = cdms.createVariable(self.arr, axes=[self.x, self.y], grid=grid1)
        
        nt.assert_true( var_utils.areGridsEqual(v1, v2))
        nt.assert_true( var_utils.areGridsEqual(v2, v1))        
        
class TestAreAttributesEqual(object):
    def setUp(self):
        self.v1 = cdms.createVariable(range(10))
        self.v2 = cdms.createVariable(range(10))
        self.v1.name = 'name' # avoid the default names
        self.v2.name = 'name'
    def tearDown(self):
        pass
        
    def test_001_AdditionalNameAttribute(self):
        self.v1.name = "V1"
        nt.assert_false( var_utils.areAttributesEqual(self.v1, self.v2))
        
    def test_002_DifferentUnitAttribute(self):
        self.v1 = cdms.createVariable(range(10), attributes={'unit':'cm'})
        self.v2 = cdms.createVariable(range(10), attributes={'unit':'Volts'})
        nt.assert_false( var_utils.areAttributesEqual(self.v1, self.v2))
        
    def test_003_AreTheSame(self):
        self.v1.setMissing(999)
        self.v2.setMissing(999)
        self.v1.unit='cm'
        self.v2.unit='cm'
        nt.assert_true( var_utils.areAttributesEqual(self.v1, self.v2))
        
    def test_004_ignoresPrivateAttribue(self):
        self.v1._location = 'south'
        
        nt.assert_true( var_utils.areAttributesEqual(self.v1, self.v2))    
    
class mock:
    def __init__(self):
        pass


# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_var_utils')

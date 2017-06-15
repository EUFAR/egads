"""
test_grid_utils.py
=============


Some unit tests for the grid utils module

"""

# Import python modules
import os
import sys

# Import third-party software
import nose

try :
    import cdms2 as cdms
    import numpy as N
except:
    import cdms
    import Numeric as N

import cdms_utils.grid_utils as grid_utils
import cdms_utils.axis_utils as axis_utils

class TestCompareGrids:
    """
    Tests for the grid_utils.compareGrids function
    """

    def setUp(self):
        a = N.array([[29, 30, 31, 32], [29, 30, 31, 32]])
        self.grid1 = cdms.createVariable(a,id='grid1')
        axisX = axis_utils.createAxis(N.array([10, 20, 30, 40]), 'x', units='m', axis='X')
        axisY = axis_utils.createAxis(N.array([10, 20]), 'y', units='m', axis='Y')
        self.grid1.setAxisList([axisY, axisX])

        b = N.array([[19, 20, 21, 22], [23, 34, 31, 38]])
        self.grid2 = cdms.createVariable(a,id='grid2')
        axisX2 = axis_utils.createAxis(N.array([10, 20, 30, 40]), 'x', units='m', axis='X')
        axisY2 = axis_utils.createAxis(N.array([10, 20]), 'y', units='m', axis='Y')
        self.grid2.setAxisList([axisY2, axisX2])

        c = N.array([[35, 36, 31, 12], [19, 38, 33, 62]])
        self.grid3 = cdms.createVariable(a,id='grid3')
        axisX3 = axis_utils.createAxis(N.array([1, 2, 3, 4]), 'x', units='m', axis='X')
        axisY3 = axis_utils.createAxis(N.array([15, 16]), 'y', units='m', axis='Y')
        self.grid3.setAxisList([axisY3, axisX3])

    def tearDown(self):
        self.grid1 = None
        self.grid2 = None
        self.grid3 = None

    def testReturnOneForMatchingGrids(self):
        assert(grid_utils.compareGrids(self.grid1, self.grid2) == True)

    def testReturnZeroForNonMatchingGridValues(self):
        assert(grid_utils.compareGrids(self.grid1, self.grid3) == False)

    def testReturnZeroForNonMatchingGridUnits(self):
        self.grid2.getAxisList()[0].units = "km"
        assert(grid_utils.compareGrids(self.grid1, self.grid2) == False)


# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_grid_utils')

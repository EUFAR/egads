# Import python modules
import os
import sys
import types

# Import third-party software
import nose

try:
    import cdms2 as cdms
    import numpy as N
    import numpy.core.ma as MA
except:
    import cdms
    import Numeric as N
    import MA

import cdms_utils.bounds_checker as bounds_checker

arr= None
arrLowerBound1 = None
arrUpperBound10 = None
arrLowerBound1AndUpperBound10 = None
arrMaskBelow5 = None
arrMaskAbove12 = None
arrMaskBelow5Above12 = None
tempVar = None
missing = 1.0e20

def setup():
    global arr, arrLowerBound1, arrUpperBound10, arrLowerBound1AndUpperBound10, tempVar
    global arrMaskBelow5, arrMaskAbove12, arrMaskBelow5Above12, missing
    arr = N.array([
                  [ 1.2,  1.0,  8.3,  4.6,  0.3],
                  [53.2,  1.2,  1.2,  4.5, 12.4]])

    arrLowerBound1 = [
                  [ 1.2,  1.0,  8.3,  4.6,  1.0],
                  [53.2,  1.2,  1.2,  4.5, 12.4]]

    arrUpperBound10 = [
                  [ 1.2,  1.0,  8.3,  4.6,  0.3],
                  [10.0,  1.2,  1.2,  4.5, 10.0]]

    arrLowerBound1AndUpperBound10 = [
                  [ 1.2,  1.0,  8.3,  4.6,  1.0],
                  [10.0,  1.2,  1.2,  4.5, 10.0]]

    m =  missing
    arrMaskBelow5 =[
                  [m, m, 8.3, m, m],
                  [53.2,  m, m, m, 12.4]]

    arrMaskAbove12 = [
                  [ 1.2,  1.0,  8.3,  4.6,  0.3],
                  [m,  1.2,  1.2,  4.5, m]]

    arrMaskBelow5Above12 = [
                  [m, m, 8.3, m, m],
                  [m,  m, m, m, m]]

    tempVar = cdms.createVariable(arr,id='temp')
    tempVar.setMissing(missing)

def tearDown():
    pass

def with_setup(up, down):
    def with_setup_decorator(func):
        func.setup = up
        func.teardown = down
        return func
    return with_setup_decorator

@with_setup(setup, tearDown)
def test_restrictToBounds_SetMissingLower():
    global tempVar, arrMaskBelow5
    returnVar = bounds_checker.restrictToBounds(tempVar, 5.0, None , set_as='missing')
    assert(returnVar.getValue().tolist() == arrMaskBelow5)

@with_setup(setup, tearDown)
def test_restrictToBounds_SetMissingUpper():
    global tempVar, arrMaskAbove12
    returnVar = bounds_checker.restrictToBounds(tempVar, None, 12 , set_as='missing')
    assert(returnVar.getValue().tolist() == arrMaskAbove12)

@with_setup(setup, tearDown)
def test_restrictToBounds_SetMissingBoth():
    global tempVar, arrMaskBelow5Above12
    returnVar = bounds_checker.restrictToBounds(tempVar, 5.0, 12 , set_as='missing')
    assert(returnVar.getValue().tolist() == arrMaskBelow5Above12)


@with_setup(setup, tearDown)
def test_restrictToBounds_SetBoundLower():
    global tempVar, arrLowerBound1
    returnVar = bounds_checker.restrictToBounds(tempVar, 1.0, None , set_as='bound')
    assert(returnVar.getValue().tolist() == arrLowerBound1)

@with_setup(setup, tearDown)
def test_restrictToBounds_SetBoundUpper():
    global tempVar, arrUpperBound10
    returnVar = bounds_checker.restrictToBounds(tempVar, None, 10 , set_as='bound')
    assert(returnVar.getValue().tolist() == arrUpperBound10)

@with_setup(setup, tearDown)
def test_restrictToBounds_SetBoundBoth():
    global tempVar, arrLowerBound1AndUpperBound10
    returnVar = bounds_checker.restrictToBounds(tempVar, 1.0, 10.0 , set_as='bound')
    assert(returnVar.getValue().tolist() == arrLowerBound1AndUpperBound10)

@with_setup(setup, tearDown)
def test_maskOutOfBounds_SetUpper():
    global tempVar, arrMaskAbove12
    returnVar = bounds_checker.maskOutOfBounds(tempVar, None, 12.0)
    assert(returnVar.getValue().tolist() == arrMaskAbove12)

@with_setup(setup, tearDown)
def test_maskOutOfBounds_SetLower():
    global tempVar, arrMaskBelow5
    returnVar = bounds_checker.maskOutOfBounds(tempVar, 5.0, None)
    assert(returnVar.getValue().tolist() == arrMaskBelow5)

@with_setup(setup, tearDown)
def test_maskOutOfBounds_SetBoth():
    global tempVar, arrMaskBelow5Above12
    returnVar = bounds_checker.maskOutOfBounds(tempVar, 5.0, 12.0)
    assert(returnVar.getValue().tolist() == arrMaskBelow5Above12)

@with_setup(setup, tearDown)
def test_bringWithinBounds_SetUpper():
    global tempVar, arrUpperBound10
    returnVar = bounds_checker.bringWithinBounds(tempVar, None, 10)
    assert(returnVar.getValue().tolist() == arrUpperBound10)

@with_setup(setup, tearDown)
def test_bringWithinBounds_SetLower():
    global tempVar, arrLowerBound1
    returnVar = bounds_checker.bringWithinBounds(tempVar, 1.0, None)
    assert(returnVar.getValue().tolist() == arrLowerBound1)

@with_setup(setup, tearDown)
def test_bringWithinBounds_SetBoth():
    global tempVar, arrLowerBound1AndUpperBound10
    returnVar = bounds_checker.bringWithinBounds(tempVar, 1.0, 10.0)
    assert(returnVar.getValue().tolist() == arrLowerBound1AndUpperBound10)


def test_bringWithinBounds_Zero():
    global missing
    var = cdms.createVariable(N.array([-2.0, -1.0, 0.0, 1.0, 2.0]),id='temp')
    var.setMissing(missing)

    returnVar = bounds_checker.bringWithinBounds(var, 0.0, None)
    print returnVar
    assert(returnVar.getValue().tolist() == [0.0, 0.0, 0.0, 1.0, 2.0])

    returnVar = bounds_checker.bringWithinBounds(var, None, 0.0)
    assert(returnVar.getValue().tolist() == [-2.0, -1.0, 0.0, 0.0, 0.0])

# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_bounds_checker')

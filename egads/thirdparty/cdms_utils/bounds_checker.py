#!/usr/bin/env python

"""
bounds_checker.py
=================

Holds the restrictToBounds function that receives a cdms variable object and
a low and high bounds limit. It returns a variable identical to the input
variable except that it either masks outside bounds or resets those values
to the lower or upper bound.

"""

# Import python modules

# Import third-party software
from cdms_utils.cdms_compat import *
#cdms_compat imports cdms, N, MA, and MV


def restrictToBounds(cdms_var, lower_bound=None, upper_bound=None, set_as="missing"):
    """
    Receives a cdms variable object and a low and high bounds limit.
    It returns a variable identical to the input variable except that it
    either masks outside bounds or resets those values to the lower or upper bound.
    """
    if set_as == "missing":
        return maskOutOfBounds(cdms_var, lower_bound, upper_bound)
    elif set_as == "bound":
        return bringWithinBounds(cdms_var, lower_bound, upper_bound)
    else:
        print "No change to variable as no bounds given."
        return cdms_var


def maskOutOfBounds(cdms_var, lower_bound=None, upper_bound=None):
    """
    Receives a cdms variable object and a low and high bounds limit.
    It returns a masked variable identical to the input variable except that
    it is masked outside of the bounds.
    """
    if lower_bound and upper_bound:
        nv = MV.masked_outside(cdms_var, lower_bound, upper_bound)
    elif lower_bound:
        nv = MV.masked_less(cdms_var, lower_bound)
    elif upper_bound:
        nv = MV.masked_greater(cdms_var, upper_bound)
    else:
        print "No change to variable as no bounds given."
        nv = cdms_var

    return nv


def bringWithinBounds(cdms_var, lower_bound=None, upper_bound=None):
    """
    Receives a cdms variable object and a low and high bounds limit.
    It returns a variable identical to the input variable except that
    values out of bounds are reset to the lower or upper bound.
    """
    # Copy original mask if present

    real_mask = cdms_var.mask

    # Get normal array version
    array = N.array(cdms_var)

    # Get array with values less than lower bound equal to lower bound
    if lower_bound != None:
        array = MA.masked_less(array, lower_bound)
        array.set_fill_value(lower_bound)
        array = N.array(array.filled())
        print "LB:", array

    # Get array with values greater than upper bound equal to upper bound
    if upper_bound != None:
        array = MA.masked_greater(array, upper_bound)
        array.set_fill_value(upper_bound)
        array = N.array(array.filled())
        print "UB:", array

    # Now re-mask if necessary
    if real_mask:
        array = MA.masked_array(array, mask=real_mask, fill_value=cdms_var.missing_value)
        print "With mask back on:", array

    # Now re-make into variable
    new_var = cdms.createVariable(array, axes=cdms_var.getAxisList(),
                   id=cdms_var.id, attributes=cdms_var.attributes)

    return new_var


if __name__ == "__main__":

    print "Running test for bringWithinBounds function:"
    x = N.array([0,1,2,3,4,999])
    print "x is:", x
    print "we want to treat 999 as missing_value and then mask 0 to lower_bound of 1"
    import MV
    ma = MV.masked_array(x, mask=[0,0,0,0,0,1], fill_value=999)
    ax = cdms.createAxis([3,5,7,9,11,13])
    ax.id = ax.units = "super_axis"
    v = cdms.createVariable(ma, id="myvar", axes=[ax],
                            mask=ma.mask(), fill_value=ma.fill_value(), attributes={"cabbage":1})
    print "V:", v, type(v), v.shape, v.attributes
    lb = 1
    ub = 3
    nv = restrictToBounds(v, lower_bound=lb, upper_bound=ub, set_as="bound")
    print nv

__all__ = ['findIndex', 'findIndexLon']


def findIndexLon(value, boundsList, useLimits=False):
    """
    wrapper for the usual longitude case (modulo = 360)
    """
    return findIndex(value, boundsList, modulo=360., useLimits=useLimits)


def findIndex(value, boundsList,
              modulo = None,
              useLimits = False):
    """
    find the axis index whose bounds contain a particular coordinate value

    @param value: coordinate value to be found
    @type value: numeric
    @param boundsList: axis bounds list
    @type boundsList: list of 2-element lists, such as returned by getBounds() in CDMS
    @param modulo: None for non-periodic axis, else set to modulus e.g. 360 for longitude in degrees
    @type modulo: numeric or None
    @param useLimits: set to True to use the first or last index in the case
                      of data outside the range; in the case of a periodic
                      axis, it will choose whichever end is nearer to the
                      requested value
    @type useLimits: boolean

    @return: index in bounds array
    @rtype: int
    """

    order = _getOrder(boundsList[1][0], boundsList[0][0], modulo)

    # check that ordering between boxes agrees with ordering
    # of bounds within one box
    if _getOrder(boundsList[0][1], boundsList[0][0], modulo) != order:
        raise ValueError("bounds ordered incorrectly")

    n = len(boundsList)
    for index in range(n):
        if _inBounds(value, boundsList[index], order, modulo):
            return index

    # we are outside the range
    if not useLimits:
        raise IndexError("value lies outside bounds range")

    firstVal = boundsList[0][0]
    lastVal = boundsList[n - 1][1]
    
    off1 = _getOffset(firstVal, value, order, modulo)
    off2 = _getOffset(value, lastVal, order, modulo)
    if modulo:
        # periodic
        if off1 + off2 > modulo:
            raise ValueError("gap in bounds array?")
        if off1 < off2:
            return 0
        else:
            return n - 1
    else:
        # non-periodic
        if off1 > 0:
            return 0
        elif off2 > 0:
            return n - 1
        else:
            raise ValueError("gap in bounds array?") 


def _getOrder(val2, val1, modulo):
    """
    Get ordering: 1 = increasing, -1 = decreasing
    """
    diff = val2 - val1
    if modulo:
        # put into range e.g. -180 to 180
        diff = ((diff + modulo / 2) % modulo) - modulo / 2
    return cmp(diff, 0)


def _getOffset(val2, val1, order, modulo):
    """
    Evaluate the offset between two axis values, in the direction specified
    by the ordering, taking into account the modulo
    """
    diff = (val2 - val1) * order
    if modulo:
        # put in range e.g. 0 to 360
        diff = diff % modulo
    return diff


def _inBounds(value, bounds, order, modulo):
    """
    Test whether value lies within the bounds, taking into account the
    ordering and the modulo
    """
    diff = _getOffset(value, bounds[0], order, modulo)
    width = _getOffset(bounds[1], bounds[0], order, modulo)
    return 0 <= diff <= width

#----------------------------------------------------------------------

def _test(filename, varname=None):
    try:
        import cdms
    except ImportError:
        import cdms2 as cdms        
    f = cdms.open(filename)
    if varname:
        var = f[varname]
    else:
        var = f.getVariables()[0]
    axes = var.getAxisList()

    rlons = axes[3]
    rlats = axes[2]

    lonBounds = rlons.getBounds()
    latBounds = rlats.getBounds()

    print "file longitudes"
    print lonBounds
    print "finding longitudes"
    for lon in range(360):
        print lon, findIndexLon(lon, lonBounds, useLimits=True)

    print "file latitudes"
    print latBounds
    print "finding latitudes"
    for lat in range(-90, 91):
        print lat, findIndex(lat, latBounds, useLimits=True)


if __name__ == '__main__':
    _test('/tmp/afixaa.pem4oct.pp')

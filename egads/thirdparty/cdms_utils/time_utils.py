"""
time_utils.py
=============

Some useful time utilities for use with cdms and cdtime

"""

# Import python modules
import os
import re
import time

# Import third-party software
import cdtime

try:
    import cdms2 as cdms
except:
    import cdms


dateTimePattern=re.compile(r"^(\d{4}).(\d{1,2}).(\d{1,2})(\s+|T)(\d+):(\d+):(\d+\.?.*)$")


def getDateTimeComponents(dateTimeString):
    """
    Takes in a time string in standard DateTime format and returns the items in it.
    """
    match=dateTimePattern.match(dateTimeString)
    if not match:
        raise Exception("Cannot match date time string: %s" % dateTimeString)

    items=match.groups()
    (year, month, day, hour, minute)=[int(i) for i in items[:3]+items[4:6]]
    second=float(items[6])
    return (year, month, day, hour, minute, second)


def convertDateTimeStringToYYYYMMDDHH(timeString):
    """
    Takes in a long CF-compliant time string and returns a shorter
    YYYYMMDDHH string.
    """
    match=re.match(r"(\d{4}).(\d{1,2}).(\d{1,2})(\s+|T)(\d+):", timeString)
    if match:
        (y,m,d,blank,h)=match.groups()
        timeString="%.4d%.2d%.2d%.2d" % (int(y), int(m), int(d), int(h))

    return timeString


def getTodayMinus(n, format="string"):
    "Returns today minus n days as a string, dict or tuple."
    now = time.time()
    oneday = 24*60*60
    targettime = now - (int(n)*oneday)

    if format == "string":
        targetdate=time.strftime("%Y%m%d", time.localtime(targettime))
    else:
        (y, m, d) = time.localtime(targettime)[:3]
        if format == "dict":
            targetdate = {"year":"%.4d"%y, "month":"%.2d"%m, "day":"%.2d"%d}
        elif format == "list":
            targetdate = [y, m, d]
        elif format == "tuple":
            targetdate = (y, m, d)
        else :
            raise Exception("Unknown output format :" + format)
    return targetdate



def getTimeSubsetStartEndIndices(time_axis, start, end, required_hour=None):
    """
    Analyses time_axis and returns a (start_index, end_index) tuple that
    represent the correct indices in the array for start and end. If
    required_hour is given then it also checks start is set on the time
    of day (e.g. 0 for midnight and 12 for midday) expected. If not it adjusts
    the start_index so it is on the required_hour. It does NOT adjust the
    end_index.
    """

    units = time_axis.units
    start_time = cdtime.s2r(start, units, cdtime.Calendar360)
    end_time = cdtime.s2r(end, units, cdtime.Calendar360)

    # Check hour of start_time if required
    if required_hour != None:
        required_hour = int(required_hour)
        comp_time = start_time.tocomp()
        hour = comp_time.hour
        print start_time
        print start_time.tocomp()
        print hour
        if hour != required_hour:
            print "Adjusting to next day to get required hour right."
            new_start = comp_time.add(1, cdtime.Day)
            new_start.hour = required_hour
            print "New start time:", new_start
            start_time = new_start.torel(units, cdtime.Calendar360)

    start_value = start_time.value
    end_value = end_time.value

    # Check both indices are in the axis values
    if start_value not in time_axis[:]:
        raise Exception("Start index not in axis values: " + str(start_value))
    if end_value not in time_axis[:]:
        raise Exception("End index not in axis values: " + str(end_value))

    t_values = list(time_axis[:])

    start_index = t_values.index(start_value)
    end_index = t_values.index(end_value)

    return (start_index, end_index)

if __name__ == "__main__":

    t = cdms.createAxis([i/4. for i in range(100)])
    t.id = t.standard_name = t.long_name = "time"
    t.units = "days since 1970-01-01 00:00:00"
    t.axis = "T"
    t.designateTime()

    start = "1970-01-03 00:00:00"
    end = "1970-01-6 18:00:00"

    print "Testing with no required hour..."
    print getTimeSubsetStartEndIndices(t, start, end)

    print "Testing with required hour..."
    start = "1970-01-03 12:00:00"
    print getTimeSubsetStartEndIndices(t, start, end, required_hour=0)
    start = "1970-01-03 12:00:00"
    print getTimeSubsetStartEndIndices(t, start, end, required_hour=13)

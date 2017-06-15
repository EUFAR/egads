"""
test_time_utils.py
=============


Some unit tests for the grid utils module

"""

# Import python modules
import os
import sys
import time
import calendar
import datetime

# Import third-party software
import nose

try:
    import numpy as N
except:
    import Numeric as N

import cdms_utils.time_utils as time_utils
import cdms_utils.axis_utils as axis_utils

class TestGetDateTimeComponents:
    """
    Tests for the time_utils.getDateTimeComponents function
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testRaisesExceptionWhenGivenInvalidDateString(self):
        invalidDateString = "89.970,324235//3"
        nose.tools.assert_raises(Exception,
                                 time_utils.getDateTimeComponents,
                                 invalidDateString)

    def testReturnsComponetsCorrectly(self):
        dateString = "1764.12.2T14:24:1.345"
        (year, month, day, hour, minute, second) = time_utils.getDateTimeComponents(dateString)
        assert((year, month, day, hour, minute, second) == \
               (1764,    12,   2,   14,     24,  1.345))


class TestConvertDateTimeStringToYYYYMMDDHH:
    """
    Tests for the time_utils.convertDateTimeStringToYYYYMMDDHH function
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReducesLongDateTimeString(self):
        longTimeString = "1222-10-5 20:02:16"
        reducedString = time_utils.convertDateTimeStringToYYYYMMDDHH(longTimeString)
        assert(reducedString == "1222100520")

    def testReducesLongDateTimeStringWithAlternateFormat(self):
        longTimeString = "2001/4/14T6:02:16"
        reducedString = time_utils.convertDateTimeStringToYYYYMMDDHH(longTimeString)
        print reducedString
        assert(reducedString == "2001041406")

class TestGetTodayMinus:
    """
    Test for the time_utils.getTodayMinus function
    """

    def setUp(self):
        self.today = time.localtime()
        pass

    def tearDown(self):
        pass

    def testRaisesExceptionWithUnknownFormat(self):
        nose.tools.assert_raises(Exception,
                            time_utils.getTodayMinus,
                            2, "somethingthatisntaformat")

    def testDefaultResultIsString(self):
        result = time_utils.getTodayMinus(2)
        assert (type(result) == str)

    def testResultStringFormatForToday(self):
        result = time_utils.getTodayMinus(0, format='string')
        (year,month,day) = time.localtime()[:3]
        todayString = "%4i%02i%02i" % (year, month, day)
        assert(type(result) == str)
        assert(result == todayString)

    def testResultDictFormatForToday(self):
        result = time_utils.getTodayMinus(0, format='dict')
        (year,month,day) = time.localtime()[:3]
        todayDict = {"year":"%04i" % year, "month":"%02i" % month, "day":"%02i" % day}
        assert(type(result) == dict)
        assert(result == todayDict)

    def testResultListFormatForToday(self):
        result = time_utils.getTodayMinus(0, format='list')
        assert(type(result) == list)
        assert(result == list(time.localtime()[:3]))

    def testResultTupleFormatForToday(self):
        result = time_utils.getTodayMinus(0, format='tuple')
        assert(type(result) == tuple)
        assert(result == time.localtime()[:3])

    def testResultFor6DaysAgo(self):
        assert(self._checkResultForNDaysAgo(6) == True)

    def testResultFor23DaysAgo(self):
        assert(self._checkResultForNDaysAgo(23) == True)

    def testResultFor152DaysAgo(self):
        assert(self._checkResultForNDaysAgo(152) == True)

    def testResultFor2237DaysAgo(self):
        assert(self._checkResultForNDaysAgo(2237) == True)

    def _checkResultForNDaysAgo(self, N):

        (resultYear, resultMonth, resultDay) = time_utils.getTodayMinus(N, format='tuple')

        delta = datetime.timedelta(days=N)
        today = datetime.date.today()
        NdaysAgo = (today - delta)

        return (resultYear == NdaysAgo.year and resultMonth == NdaysAgo.month \
                and resultDay == NdaysAgo.day)


class TestGetTimeSubsetStartEndIndices:
    """
    Test for the time_utils.getTimeSubsetStartEndIndices function
    """

    def setup(self):
        self.daysAxis = axis_utils.createAxis(N.array([2, 3, 4, 5, 6, 7, 8, 9]),
                                          't', units='days since 1998-03-01', axis='T')

        self.quarterDaysAxis = axis_utils.createAxis(N.array([1, 1.25, 1.5, 1.75,
                                                              2, 2.25, 2.5, 2.75,
                                                              3, 3.25, 3.5, 3.75,
                                                              4, 4.25, 4.5, 4.75,
                                                              5]),
                                          't', units='days since 1998-03-01', axis='T')

    def tearDown(self):
        pass

    def testFindsIndiciesFromAxisInDays(self):
        result = time_utils.getTimeSubsetStartEndIndices(self.daysAxis,
                                                         "1998-03-05", "1998-03-08")
        assert(result == (2,5))

    def testRaisesExceptionWhenStartNotInRange(self):
        nose.tools.assert_raises(Exception,
                                time_utils.getTimeSubsetStartEndIndices,
                                self.daysAxis, "1998-03-01", "1998-03-08")

    def testRaisesExceptionWhenEndNotInRange(self):
        nose.tools.assert_raises(Exception,
                                self.daysAxis, "1998-03-05", "1998-03-18")

    def testFindIndiciesIncludingHour(self):
        result = time_utils.getTimeSubsetStartEndIndices(self.quarterDaysAxis,
                                                         "1998-03-03 06:00:00", "1998-03-05")

        print result
        assert(result == (5,12))

    def testFindIndiciesIncludingRequiredHour(self):
        result = time_utils.getTimeSubsetStartEndIndices(self.quarterDaysAxis,
                                                         "1998-03-03", "1998-03-05",
                                                         required_hour=6)
        #return a day after the first index to assure including the required hour
        assert(result == (9,12))



# Magic to run tests if executed as a script
if __name__ == '__main__':

    nose.main(defaultTest='test_time_utils')

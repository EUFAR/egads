#   Copyright (C) 2004 CCLRC & NERC( Natural Environment Research Council ).
#   This software may be distributed under the terms of the
#   Q Public License, version 1.0 or later. http://ndg.nerc.ac.uk/public_docs/QPublic_license.txt

"""
textParser.py
=============

A set of functions to parse text file data into lists, strings,
reals, integers etc.

"""

import re
import string

pattnNoQuotes = re.compile("^[\"'].*\1$")

def readItemFromLine(line, rttype=str):
    """

    """
    rtitem = pattnNoQuotes.sub("", line.strip())
    if rttype is not str:
        rtitem = rttype(rtitem)   
    return rtitem

def readItemsFromLine(line, nitems=None, rttype=str):
    """

    """
    rtitems = re.split(r"\s+", line.strip())
    if nitems and len(rtitems) != nitems:
        raise "Incorrect number of items (%s) found in line: \n'%s'" % (nitems, line)
    if rttype is not str:
        rtitems = [rttype(x) for x in rtitems]
    return rtitems

def readItemsFromLines(lines, nitems, rttype=str):
    """

    """
    rtitems = []
    for line in lines:
        rtitems = rtitems + [readItemFromLine(line, rttype)]
    if rttype is not str:
        rtitems = [rttype(x) for x in rtitems]
    return rtitems

def readItemsFromUnknownLines(object, nitems, rttype=str):
    """
    Reads from an unknown number of lines until n items have been collected.
    The 'object' argument can be a filehandle (i.e. obj=open('name.ext', 'r'))
    or a string wrapped in a StringIO object (i.e. obj=StringIO.StringIO('abc')).
    The 'object' argument can also be a list, in which case the partially used/read object is
    also returned.
    """

    rtitems = []
    lines = []        
    if type(object) == type([2,3]): 

        while len(rtitems) < nitems:   
	    nextitem = object[0]
	    object = object[1:]
            items = nextitem.strip().split()
            lines.append(items)
            (rtitems, extras) = (rtitems + items[:nitems], items[nitems:])

    else:
        while len(rtitems) < nitems:
            items = object.readline().strip().split()
            lines.append(items)
            (rtitems, extras) = (rtitems + items[:nitems], items[nitems:])

    if len(extras) > 0:
        raise Exception("Could not split " + `len(lines)` + " lines exactly into required number (" + `nitems` + ") of items: \n" + str(lines))

    if rttype is not str:
        rtitems = [rttype(x) for x in rtitems]

    if type(object) == type([1,2]):
        return (rtitems, object)
    else:
        return rtitems

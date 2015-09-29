__author__ = "mfreer"
__date__ = "$Date:: 2012-07-12 17:27#$"
__version__ = "$Revision:: 150       $"
__all__ = ["EgadsFile", "EgadsCsv", "parse_string_array"]

import csv
import sys

from egads.input import FileCore
import numpy

class EgadsFile(FileCore): #TODO: add error handling to EgadsFile.
    """
    Generic class for interfacing with text files.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes instance of EgadsFile object.


        :param string filename : string, optional
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r``
            is the default value.
        """

        FileCore.__init__(self, filename, perms, pos=0)



    def close(self):
        """
        Close opened file.
        """

        FileCore.close(self)
        self.pos = 0

    def _open_file(self, filename, perms):
        """
        Private method for opening file.


        :param string filename:
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is the default
            value.
        """

        self.close()

        try:
            self.f = open(filename, perms)
            self.filename = filename
            self.perms = perms
            self.pos = self.f.tell()
        except IOError:
#            print "ERROR: File %s doesn't exist" % (filename)
            raise
        except Exception:
            print "ERROR: Unexpected error"
            raise


    def display_file(self):
        """
        Prints contents of file out to standard output.

        """

        self.f.seek(0)
        for line in self.f:
            print line

        self.f.seek(self.pos)

    def get_position(self):
        """
        Returns current position in file.


        """

        self.pos = self.f.tell()

        return self.pos

    def seek(self, location, from_where=None):
        """
        Change current position in file.
        

        :param integer location:
            Position in file to seek to.
        :param char from_where: Optional -
            Where to seek from. Valid options are ``b`` for beginning, ``c`` for
            current and ``e`` for end.
        """

        from_switch = {'b': lambda: 0,
            'c': lambda: 1,
            'e': lambda: 2}

        from_val = from_switch.get(from_where, lambda: 0)()

        self.f.seek(location, from_val)
        self.pos = self.f.tell()


    def write(self, data):  #TODO: make write method more robust
        """
        Writes data to a file. Data must be in the form of a string, with line
        ends signified by ``\\n``.

        :param string data:
            Data to output to current file at current file position. Data must
            be a string, with ``\\n`` signifying line end.
        """

        self.f.write(data)
        self.pos = self.f.tell()

    def read(self, size=None):
        """
        Reads data in from file.

        :param int size: Optional -
            Number of bytes to read in from file. If left empty, entire file will
            be read in.

        :returns:
            String data from text file.
        :rtype: string
        """

        if size is None:
            filedata = self.f.read()
        else:
            filedata = self.f.read(size)

        self.pos = self.f.tell()

        return filedata

    def read_line(self):
        """
        Reads single line of data from file.
        """

        filedata = self.f.readline()
        self.pos = self.f.tell()

        return filedata

    def reset(self):
        """
        Returns to beginning of file
        """

        self.f.seek(0)
        self.pos = self.f.tell()


class EgadsCsv(EgadsFile):
    """
    Class for reading data from CSV files.
    """


    def __init__(self, filename=None, perms='r', delimiter=',', quotechar='"'):
        """
        Initializes instance of EgadsFile object.

        :param string filename: Optional -
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is the default
            value.
        :param string delimiter: Optional -
            One-character string used to separate fields. Default is ','.
        :param string quotechar: Optional -
            One-character string used to quote fields containing special characters.
            The default is '"'.
        """

        FileCore.__init__(self, filename, perms,
                           reader=None,
                           writer=None,
                           delimiter=delimiter,
                           quotechar=quotechar)


    def open(self, filename, perms, delimiter=None, quotechar=None):
        """
        Opens file.

        :param string filename:
            Name of file to open.
        :param char perms:  Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read.
            ``r`` is the default value.
        :param string delimiter: Optional -
            One-character string used to separate fields. Default is ','.
        :param string quotechar: Optional -
            One-character string used to quote fields containing special characters.
            The default is '"'.
        """


        if perms is not None:
            self.perms = perms
        else:
            perms = self.perms

        if delimiter is not None:
            self.delimiter = delimiter
        else:
            delimiter = self.delimiter

        if quotechar is not None:
            self.quotechar = quotechar
        else:
            quotechar = self.quotechar

        self._open_file(filename, perms)

    def display_file(self):
        """
        Prints contents of file out to standard output.

        """


        try:
            for row in self.reader:
                print row
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))

        self.seek(self.pos)

    def read(self, lines=None, format=None):
        """
        Reads in and returns contents of csv file.


        :param int lines: Optional -
            Number specifying the number of lines to read in. If left blank,
            the whole file will be read and returned.
        :param list format: Optional -
            List type composed of one character strings used to decompose elements
            read in to their proper types. Options are ``i`` for int, ``f`` for float,
            ``l`` for long and ``s`` for string.

        :returns:
            List of arrays of values read in from file. If a format string is provided,
            the arrays are returned with the proper data type.
        :rtype: list of arrays
        """

        data = []

        if lines is None:
            try:
                for row in self.reader:
                    data.append(row)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))

        else:
            try:
                for i in xrange(lines):
                    row = self.reader.next()
                    data.append(row)
            except csv.Error, e:
                sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))

        data = numpy.array(data)
        data = data.transpose()

        if format is None:
            return list(data)
        else:
            parsed_data = parse_string_array(data, format)
            return parsed_data

    def skip_line(self, amount=1):
        """
        Skips over line(s) in file.
        
        :param int amount: Optional -
            Number of lines to skip over. Default value is 1.
        
        """
        for i in xrange(amount):
            self.f.readline()

    def write(self, data):
        """
        Writes single row out to file.


        :param list data:
            Data to be output to file using specified delimiter.

        """

        self.writer.writerow(data)


    def writerows(self, data):
        """
        Writes data out to file.


        :param list data:
            List of variables to output.

        """



        data_arr = numpy.column_stack(tuple(data))

#        data_arr = data_arr.transpose()


        self.writer.writerows(data_arr)






    def _open_file(self, filename, perms):
        """
        Private method for opening file.

        :param string filename:
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is the default
            value.
        :param string delimiter: Optional -
            One-character string used to separate fields. Default is ','.
        :param string quotechar: Optional -
            One-character string used to quote fields containing special characters.
            The default is '"'.
        """

        self.close()

        try:
            self.f = open(filename, perms)
            self.filename = filename
            self.perms = perms
            self.pos = self.f.tell()
            if perms == 'r' or perms == 'r+':
                self.reader = csv.reader(self.f, delimiter=self.delimiter,
                                         quotechar=self.quotechar)
            if perms == 'w' or perms == 'a' or perms == 'r+':
                self.writer = csv.writer(self.f, delimiter=self.delimiter,
                                         quotechar=self.quotechar)
        except IOError:
            print "ERROR: File %s doesn't exist" % (filename)
            raise RuntimeError
        except Exception:
            print "ERROR: Unexpected error"
            raise


def parse_string_array(data, format):
    """
    Converts elements in string list using format list to their proper types.


    :param numpy.ndarray data:
        Input string array.
    :param list format:
        List type composed of one character strings used to decompose elements
        read in to their proper types. Options are 'i' for int, 'f' for float,
        'l' for long and 's' for string.

    :returns:
        Array parsed into its proper types.
    :rtype: numpy.ndarray
    """


    format_array_dict = {'i': 'i4', 'f': 'f8', 'l':'f8', 's':'a20'}


    parsed_data = list(data)

    i = 0


    for row in parsed_data:
        fmt_count = i % len(format)
        parsed_data[i] = numpy.asarray(row, dtype=format_array_dict[format[fmt_count]])
        i += 1

    return parsed_data



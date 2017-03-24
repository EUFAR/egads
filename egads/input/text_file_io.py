__author__ = "mfreer, ohenry"
__date__ = "$Date:: 2017-01-20 10:00#$"
__version__ = "$Revision:: 153       $"
__all__ = ["EgadsFile", "EgadsCsv", "parse_string_array"]

import csv
import sys
from egads.input import FileCore
import numpy
import logging

class EgadsFile(FileCore): 
    """
    Generic class for interfacing with text files.
    """

    def __init__(self, filename=None, perms='r'):
        """
        Initializes instance of EgadsFile object.

        :param string filename:
            Optional - Name of file to open.
        :param char perms: 
            Optional - Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is the 
            default value.
        """

        logging.debug('egads.input.EgadsFile.__init__ invoked: filename ' + str(filename) + ', perms' + str(perms))
        FileCore.__init__(self, filename, perms, pos=0)

    def close(self):
        """
        Close opened file.
        """

        logging.debug('egads.input.EgadsFile.close invoked')
        FileCore.close(self)
        self.pos = 0

    def _open_file(self, filename, perms):
        """
        Private method for opening file.

        :param string filename:
            Name of file to open.
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is the 
            default value.
        """

        logging.debug('egads.input.EgadsFile._open_file invoked: filename ' + str(filename) + ', perms' + str(perms))
        self.close()
        try:
            self.f = open(filename, perms)
            self.filename = filename
            self.perms = perms
            self.pos = self.f.tell()
        except RuntimeError:
            logging.error('egads.input.EgadsFile._open_file invoked: RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.error('egads.input.EgadsFile._open_file invoked: IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.error('egads.input.EgadsFile._open_file invoked: Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")

    def display_file(self):
        """
        Prints contents of file out to standard output.
        """

        logging.debug('egads.input.EgadsFile.display_file invoked')
        self.f.seek(0)
        for line in self.f:
            print line
        self.f.seek(self.pos)

    def get_position(self):
        """
        Returns current position in file.
        """
        
        logging.debug('egads.input.EgadsFile.get_position invoked')
        self.pos = self.f.tell()
        logging.debug('..........................................self.pos ' + str(self.pos))
        return self.pos

    def seek(self, location, from_where=None):
        """
        Change current position in file.

        :param integer location:
            Position in file to seek to.
        :param char from_where: 
            Optional - Where to seek from. Valid options are ``b`` for beginning, ``c`` for
            current and ``e`` for end.
        """

        logging.debug('egads.input.EgadsFile.seek invoked: location ' + str(location) + ', from_where ' + str(from_where))
        from_switch = {'b': lambda: 0,
            'c': lambda: 1,
            'e': lambda: 2}
        from_val = from_switch.get(from_where, lambda: 0)()
        self.f.seek(location, from_val)
        self.pos = self.f.tell()
        logging.debug('...................................................................self.pos ' + str(self.pos))

    def write(self, data):
        """
        Writes data to a file. Data must be in the form of a string, with line
        ends signified by ``\\n``.

        :param string data:
            Data to output to current file at current file position. Data must
            be a string, with ``\\n`` signifying line end.
        """

        logging.debug('egads.input.EgadsFile.write invoked')
        self.f.write(data)
        self.pos = self.f.tell()
        logging.debug('egads.input.EgadsFile.write invoked -> data write OK, self.pos ' + str(self.pos))

    def read(self, size=None):
        """
        Reads data in from file.

        :param int size: 
            Optional - Number of bytes to read in from file. If left empty, entire file will
            be read in.

        :returns:
            String data from text file.
        :rtype: string
        """

        logging.debug('egads.input.EgadsFile.read invoked: size' + str(size))
        if size is None:
            filedata = self.f.read()
        else:
            filedata = self.f.read(size)
        self.pos = self.f.tell()
        logging.debug('egads.input.EgadsFile.read invoked -> data read OK, self.pos ' + str(self.pos))
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

    logging.info('egads.input.EgadsFile has been loaded')


class EgadsCsv(EgadsFile):
    """
    Class for reading data from CSV files.
    """

    def __init__(self, filename=None, perms='r', delimiter=',', quotechar='"'):
        """
        Initializes instance of EgadsFile object.

        :param string filename:
            Optional - Name of file to open.
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is 
            the default value.
        :param string delimiter:
            Optional - One-character string used to separate fields. Default is ','.
        :param string quotechar:
            Optional - One-character string used to quote fields containing special characters.
            The default is '"'.
        """
        
        logging.debug('egads.input.EgadsCsv.__init__ invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms) + ', delimiter ' + str(delimiter) + ', quotechar ' +
                      str(quotechar))
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
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is 
            the default value.
        :param string delimiter:
            Optional - One-character string used to separate fields. Default is ','.
        :param string quotechar:
            Optional - One-character string used to quote fields containing special characters.
            The default is '"'.
        """
        
        logging.debug('egads.input.EgadsCsv.open invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms) + ', delimiter ' + str(delimiter) + ', quotechar ' +
                      str(quotechar))
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
        
        logging.debug('egads.input.EgadsCsv.display_file invoked')
        try:
            for row in self.reader:
                print row
        except csv.Error, e:
            logging.error('egads.input.EgadsCsv.display_file invoked: csv.Error, file ' +
                          str(self.filename) + ', line ' + str(self.reader.linenum) + ', message ' +
                          str(e))
            sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))
        self.seek(self.pos)

    def read(self, lines=None, out_format=None):
        """
        Reads in and returns contents of csv file.

        :param int lines:
            Optional - Number specifying the number of lines to read in. If left blank,
            the whole file will be read and returned.
        :param list format:
            Optional - List type composed of one character strings used to decompose elements
            read in to their proper types. Options are ``i`` for int, ``f`` for float,
            ``l`` for long and ``s`` for string.

        :returns:
            List of arrays of values read in from file. If a format string is provided,
            the arrays are returned with the proper data type.
        :rtype: list of arrays
        """

        logging.debug('egads.input.EgadsCsv.read invoked: lines ' + str(lines) + ', out_format ' +
                      str(out_format))
        data = []
        if lines is None:
            try:
                for row in self.reader:
                    data.append(row)
            except csv.Error, e:
                logging.error('egads.input.EgadsCsv.display_file invoked: csv.Error, file ' +
                          str(self.filename) + ', line ' + str(self.reader.linenum) + ', message ' +
                          str(e))
                sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))
        else:
            try:
                for _ in xrange(lines):
                    row = self.reader.next()
                    data.append(row)
            except csv.Error, e:
                logging.error('egads.input.EgadsCsv.display_file invoked: csv.Error, file ' +
                          str(self.filename) + ', line ' + str(self.reader.linenum) + ', message ' +
                          str(e))
                sys.exit('file %s, line %d: %s' % (self.filename, self.reader.linenum, e))
        data = numpy.array(data)
        data = data.transpose()
        if out_format is None:
            return list(data)
        else:
            parsed_data = parse_string_array(data, out_format)
            return parsed_data
        logging.debug('egads.input.EgadsCsv.read invoked -> data read OK')

    def skip_line(self, amount=1):
        """
        Skips over line(s) in file.
        
        :param int amount:
            Optional - Number of lines to skip over. Default value is 1.
        """
        
        logging.debug('egads.input.EgadsCsv.skip_line invoked: amount ' + str(amount))
        for _ in xrange(amount):
            self.f.readline()

    def write(self, data):
        """
        Writes single row out to file.

        :param list data:
            Data to be output to file using specified delimiter.
        """
        
        logging.debug('egads.input.EgadsCsv.write invoked')
        self.writer.writerow(data)
        logging.debug('egads.input.EgadsCsv.write invoked -> data write OK')

    def writerows(self, data):
        """
        Writes data out to file.

        :param list data:
            List of variables to output.
        """
        
        logging.debug('egads.input.EgadsCsv.writerows invoked')
        data_arr = numpy.column_stack(tuple(data))
        self.writer.writerows(data_arr)
        logging.debug('egads.input.EgadsCsv.writerows invoked -> data write OK')

    def _open_file(self, filename, perms):
        """
        Private method for opening file.

        :param string filename:
            Name of file to open.
        :param char perms:
            Optional - Permissions used to open file. Options are ``w`` for write (overwrites
            data), ``a`` for append ``r+`` for read and write, and ``r`` for read. ``r`` is 
            the default value.
        :param string delimiter:
            Optional - One-character string used to separate fields. Default is ','.
        :param string quotechar:
            Optional - One-character string used to quote fields containing special characters.
            The default is '"'.
        """

        logging.debug('egads.input.EgadsCsv._open_file invoked: filename ' + str(filename) + 
                      ', perms ' + str(perms))
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
        except RuntimeError:
            logging.error('egads.input.EgadsCsv._open_file invoked: RuntimeError, File '+
                           str(filename) + ' doesn''t exist')
            raise RuntimeError("ERROR: File %s doesn't exist" % (filename))
        except IOError:
            logging.error('egads.input.EgadsCsv._open_file invoked: IOError, File '+
                           str(filename) + ' doesn''t exist')
            raise IOError("ERROR: File %s doesn't exist" % (filename))
        except Exception:
            logging.error('egads.input.EgadsCsv._open_file invoked: Exception, Unexpected error')
            raise Exception("ERROR: Unexpected error")
        
    logging.info('egads.input.EgadsCsv has been loaded')


def parse_string_array(data, data_format):
    """
    Converts elements in string list using format list to their proper types.

    :param numpy.ndarray data:
        Input string array.
    :param list data_format:
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
        fmt_count = i % len(data_format)
        parsed_data[i] = numpy.asarray(row, dtype=format_array_dict[data_format[fmt_count]])
        i += 1
    return parsed_data


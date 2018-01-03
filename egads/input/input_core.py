__author__ = "mfreer"
__date__ = "2011-09-15 17:09"
__version__ = "1.6"
__all__ = ["FileCore", "get_file_list"]

import glob
import logging

class FileCore(object):
    """
    Abstract class which holds basic file access methods and attributes.
    Designed to be subclassed by NetCDF, NASA Ames and basic text file
    classes.

    **Constructor Variables**
    
    :param string filename: Optional -
        Name of file to open.
    :param char perms: Optional -
        Permissions used to open file. Options are ``w`` for write (overwrites data in file),
        ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
    """

    def __init__(self, filename=None, perms='r', **kwargs):
        """
        Initializes file instance.

        :param string filename: Optional -
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
        """

        logging.debug('egads - input_core.py - FileCore - __init__ - filename ' + str(filename) + 
                      ', perms ' + perms + ', kwargs ' + str(kwargs))
        self.f = None
        self.filename = filename
        self.perms = perms
        for key, val in kwargs.iteritems():
            setattr(self, key, val)
        if filename is not None:
            self._open_file(filename, perms)

    def open(self, filename, perms=None):
        """
        Opens file given filename.

        :param string filename:
            Name of file to open.
        :param char perms: Optional -
            Permissions used to open file. Options are ``w`` for write (overwrites data in file),
            ``a`` and ``r+`` for append, and ``r`` for read. ``r`` is the default value
        """

        logging.debug('egads - input_core.py - FileCore - open - filename ' + str(filename) + ', perms ' + str(perms))
        if perms is not None:
            self.perms = perms
        else:
            perms = self.perms
        self._open_file(filename, perms)

    def close(self):
        """
        Close opened file.
        """
        
        logging.debug('egads - input_core.py - FileCore - close - filename ' + str(self.filename))
        if self.f is not None:
            self.f.close()
            self.f = None
            self.filename = None

    def get_perms(self):
        """
        Returns the current permissions on the file that is open. Returns None if
        no file is currently open. Options are ``w`` for write (overwrites
        data in file),``a`` and ``r+`` for append, and ``r`` for read.
        """
        
        logging.debug('egads - input_core.py - FileCore - get_perms - perms ' + str(self.perms))
        if self.f is not None:
            return self.perms
        else:
            return

    def get_filename(self):
        """
        If file is open, returns the filename.
        """
        
        logging.debug('egads - input_core.py - FileCore - get_filename - filename ' + str(self.filename))
        return self.filename

    logging.info('egads - input_core.py - FileCore has been loaded')

def get_file_list(path):
    """
    Given path, returns a list of all files in that path. Wildcards are supported.

    Example::
    
        file_list = get_file_list('data/*.nc')
    """

    logging.debug('egads - input_core.py - get_file_list - path ' + str(path))
    return glob.glob(path)


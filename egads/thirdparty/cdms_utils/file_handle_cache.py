"""
file_handle_cache.py
====================

Holds FileHandleCache class.

"""

# Import python modules
import os
import glob



class FileHandleCache:
    """
    Class to manage a dictionary of CDMS file objects (mode='r')
    open at the same time. Needs an internal limit after which it
    will close the oldest and delete it from the dictionary.

    Note: max number of files in any HadGEM1 dir is 3177 (aebti),
          for virtual vars you might need ape/apa therefore could
          get up to 7400.

    Note: so we set file limit to 7400 just in case.

    Note: On test system CPU and MEM usage were up to 2.5% and 2.3% when
          375 files were open. If you scale this up they could be up to
          50% with 7500 files open.

    Usage:
    >>> import file_handle_cache as fhc
    >>> cache = fhc.FileHandleCache()
    >>> # Now to open a file
    >>> cache.openFile(cdms_file_path)
    >>> # later on
    >>> cache.closeAll()
    >>> del cache
    """

    def __init__(self):
        self.d = {}
        self.l = []
        self.limit = 1000

    def __len__(self):
        return len(self.d)

    def openFile(self, opener, path):
        """
        Takes in an opener callable (could be cdms.open, or self.parent.openFile)
        and the path name.
        Checks if file is in cache, if so returns file handle.
        If not, first checks file limit has not been exceeded and then
        opens file and adds to cache dictionary. If file limit is exceeded
        then the oldest file handle is closed and removed from the dictionary.
        """
        print "Opening:", path
        if path in self.d.keys():
            return self.d[path]
        # Now already open so check if limit reached
        if (self.__len__()) >= self.limit:
            oldest = self.l[0]
            print "Hit limit, closing oldest:", oldest
            self.closeFile(oldest)

        self.d[path] = apply(opener, [path], {"mode":"r"})
        self.l.append(path)
        return self.d[path]

    def closeFile(self, path):
        "Closes individual file in cache."
        if path not in self.d.keys():
            raise Exception("Path '" + path + "' not in cached files so cannot close!")
        self.d[path].close()

        print self.d
        del self.d[path]
        # And remove from list
        print "Removing", path, "from", self.l
        self.l.remove(path)
        print "Has", path, "been removed?", self.l
        print self.d

        return True

    def closeAll(self):
        "Closes all files in cache."
        print "Closing all cache files..."
        self.l = []
        for path, file in self.d.items():
            file.close()
            del self.d[path]
        return True

if __name__ == "__main__":

    files = glob.glob("/badc/hadgem1/data/aebtd/ape/*.pp")
    cache = FileHandleCache()
    cache.limit = 2
    cache.openFile(files[0])
    cache.openFile(files[1])
    cache.openFile(files[0])
    cache.openFile(files[2])
    cache.closeFile(files[1])
    cache.openFile(files[0])
    cache.d
    cache.closeAll()

    cache.limit = 1000
    print "\nNow trying opening 5 with high limit..."
    for f in files[:5]:
        cache.openFile(f)
        print "Count:", len(cache)

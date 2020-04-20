Working with raw text files
********************************

EGADS provides the :class:`egads.input.text_file_io.EgadsFile` class as a simple wrapper for interacting with generic text files. :class:`~.EgadsFile` can read, write and display data from text files, but does not have any tools for automatically formatting input or output data. 

Opening
--------

To open a text file, simply create a :class:`~.EgadsFile` instance with the parameters *filename* and *perms*:

    >>> import egads
    >>> f = egads.input.EgadsFile('/pathname/filename.nc', 'r')

.. function:: EgadsFile(filename[, perms='r'])

   Open a text file.

   :param filename: path and filename of a text file
   :type filename: string
   :param perms: permissions ; optional
   :type perms: string
   :rtype: text file

Valid values for permissions are:

* ``r`` -- Read: opens file for reading only. Default value if nothing is provided.
* ``w`` -- Write: opens file for writing, and overwrites data in file.
* ``a`` -- Append: opens file for appending data.
* ``r+`` -- Read and write: opens file for both reading and writing.

File Manipulation
------------------

The following methods are available to control the current position in the file and display more information about the file.

.. function:: f.display_file()

   Prints contents of the file out to a standard output.

.. function:: f.get_position()

   Returns the current position in the file as an integer.

.. function:: f.seek(location[, from_where='b'])

   Seeks to a specified location in the text file.

   :param location: it is an integer specifying how far to seek
   :type location: int
   :param from_where: it is an option to specify from where to seek, valid options for *from_where* are ``b`` to seek from beginning of file, ``c`` to seek from current position in file and ``e`` to seek from the end of the file ; optional
   :type from_where: string
   :rtype: position in the text file

.. function:: f.reset()

   Resets the position to the beginning of the file.


Reading Data
----------------

Reading data is done using the ``read(size)`` method on a file that has been opened with ``r`` or ``r+`` permissions:

    >>> import egads
    >>> f = egads.input.EgadsFile()
    >>> f.open('myfile.txt','r')
    >>> single_char_value = f.read()
    >>> multiple_chars = f.read(10)

If the ``size`` parameter is not specified, the ``read()`` function will input a single character from the open file. Providing an integer value *n* as the ``size`` parameter to ``read(size)`` will return *n* characters from the open file.

Data can be read line-by-line from text files using ``read_line()``:

   >>> line_in = f.read_line()

Writing Data
--------------

To write data to a file, use the ``write(data)`` method on a file that has been opened with ``w``, ``a`` or ``r+`` permissions:

   >>> import egads
   >>> f = egads.input.EgadsFile()
   >>> f.open('myfile.txt','a')
   >>> data = 'Testing output data to a file.\n This text will appear on the 2nd line.'
   >>> f.write(data) 

Closing
----------

To close a file, simply call the ``close()`` method:

   >>> f.close()

Tutorial
---------

Here is a basic ASCII file, created by EGADS:
    
.. literalinclude:: example_files/main_raw_file.dat

This file has been created with the following commands:

* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', standard_name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', standard_name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', standard_name='time')
    
* create a new EgadsFile instance:

    >>> f = egads.input.EgadsFile()

* use the following function to open a new file:

    >>> f.open('main_raw_file.dat', 'w')
    
* prepare the headers if necessary:

    >>> headers = '# The current file has been created with EGADS\n# Institution: My Institution\n# Author(s): John Doe\n'
    >>> headers += time.metadata["standard_name"] + '    ' + data1.metadata["standard_name"] + '    ' + data2.metadata["standard_name"])

* prepare an object to receive all data:

    >>> data = ''
    >>> for i, _ in enumerate(time.value):
        ... data += str(time.value[i]) + '    ' + str(data1.value[i]) + '    ' + str(data2.value[i]) + '\n'
    
* write the headers and data into the file

    >>> f.write(headers)
    >>> f.write(data)
    
* and do not forget to close the file:

    >>> f.close()
   
.. raw:: latex

    \newpage

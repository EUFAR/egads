Working with CSV files
***********************

:class:`egads.input.text_file_io.EgadsCsv` is designed to easily input or output data in CSV format. Data input using :class:`~.EgadsCsv` is separated into a list of arrays, which each column a separate array in the list. 

Opening
----------

To open a csv file, simply create a :class:`~.EgadsCsv` instance with the parameters *filename*, *perms*, *delimiter* and *quotechar*:

    >>> import egads
    >>> f = egads.input.EgadsCsv('/pathname/filename.nc', 'r', ',','"')

.. function:: EgadsCsv(filename[, perms='r', delimiter=',', quotechar='"'])

   Open a text file.

   :param filename: path and filename of a text file
   :type filename: string
   :param perms: permissions ; optional
   :type perms: string
   :param delimiter: a one-character string used to separate fields ; optional
   :type delimiter: string
   :param quotechar: a one-character string used to quote fields containing special characters ; optional
   :type quotechar: string
   :rtype: csv file

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
------------

Reading data is done using the ``read(lines, format)`` method on a file that has been opened with ``r`` or ``r+`` permissions:

    >>> import egads
    >>> f = egads.input.EgadsCsv()
    >>> f.open('mycsvfile.csv','r')
    >>> single_line_as_list = f.read(1)
    >>> all_lines_as_list = f.read()

.. function:: f.read([lines=None, format=None])

   Returns a list of items read in from the CSV file.

   :param lines: if it is provided, the function will read in the specified number of lines, otherwise it will read the whole file ; optional
   :type lines: int
   :param format: it is an optional list of characters used to decompose the elements read in from the CSV files to their proper types, options are  ; optional
   :type format: string
   :rtype: list of items read in from the CSV file

Valid options for *format*:

* ``i`` -- int
* ``f`` -- float
* ``l`` -- long
* ``s`` -- string

Thus to read in the line:

``FGBTM,20050105T143523,1.5,21,25``

the command to input with proper formatting would look like this:

   >>> data = f.read(1, ['s','s','f','f'])

Writing Data
--------------

To write data to a file, use the ``write(data)`` method on a file that has been opened with ``w``, ``a`` or ``r+`` permissions:

   >>> import egads
   >>> f = egads.input.EgadsCsv()
   >>> f.open('mycsvfile.csv','a')
   >>> titles = ['Aircraft ID','Timestamp','Value1','Value2','Value3']
   >>> f.write(titles) 

where the ``titles`` parameter is a list of strings. This list will be output to the CSV, with each strings separated by the delimiter specified when the file was opened (default is ``,``).

To write multiple lines out to a file, ``writerows(data)`` is used:

   >>> data = [['FGBTM','20050105T143523',1.5,21,25],['FGBTM','20050105T143524',1.6,20,25.6]]
   >>> f.writerows(data)

Closing
---------

To close a file, simply call the ``close()`` method:

   >>> f.close()
   
Tutorial
---------

Here is a basic CSV file, created by EGADS:
    
.. literalinclude:: example_files/main_csv_file.csv

This file has been created with the following commands:

* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', standard_name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', standard_name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', standard_name='time')
    
* create a new EgadsFile instance:

    >>> f = egads.input.EgadsCsv()

* use the following function to open a new file:

    >>> f.open('main_csv_file.csv','w',',','"')
    
* prepare the headers if necessary:

    >>> headers = ['time', 'sea level', 'corrected sea level']

* prepare an object to receive all data:

    >>> data = [time.value, data1.value, data2.value]
    
* write the headers and data into the file

    >>> f.write(headers)
    >>> f.write(data)
    
* and do not forget to close the file:

    >>> f.close()
   
.. raw:: latex

    \newpage

.. raw:: latex

    \newpage

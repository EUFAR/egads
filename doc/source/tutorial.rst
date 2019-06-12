========
Tutorial
========


Exploring EGADS
****************

The simplest way to start working with EGADS is to run it from the Python command line. 
To load EGADS into the Python name-space, simply import it:

    >>> import egads

You may then begin working with any of the algorithms and functions contained in EGADS.

There are several useful methods to explore the routines contained in EGADS. 
The first is using the Python built-in ``dir()`` command:

    >>> dir(egads)

returns all the classes and subpackages contained in EGADS. EGADS follows the naming conventions from the Python Style Guide (http://www.python.org/dev/peps/pep-0008), so classes are always ``MixedCase``, functions and modules are generally ``lowercase`` or ``lowercase_with_underscores``. As a further example,

    >>> dir(egads.input)

would returns all the classes and subpackages of the ``egads.input`` module.

Another way to explore EGADS is by using tab completion, if supported by your Python installation. Typing 

    >>> egads.

then hitting ``TAB`` will return a list of all available options. 

Python has built-in methods to display documentation on any function known as docstrings. 
The easiest way to access them is using the ``help()`` function:

   >>> help(egads.input.NetCdf)

or

   >>> egads.input.NetCdf?

will return all methods and their associated documentation for the :class:`~.NetCdf` class.
  
Simple operations with EGADS
-----------------------------

To have a list of file in a directory, use the following function:

   >>> egads.input.get_file_list('path/to/all/netcdf/files/*.nc')

.. raw:: latex

    \newpage

The :class:`~.EgadsData` class
*******************************

At the core of the EGADS package is a data class intended to handle data and associated metadata in a consistent way between files, algorithms and within the framework. This ensures that important metadata is not lost when combining data form various sources in EGADS.

Additionally, by subclassing the Quantities and Numpy packages, :class:`~.EgadsData` incorporates unit comprehension to reduce unit-conversion errors during calculation, and supports broad array manipulation capabilities. This section describes how to employ the :class:`~.EgadsData` class in the EGADS program scope.


Creating :class:`~.EgadsData` instances
----------------------------------------

The :class:`~.EgadsData` class takes four basic arguments:

* value
   Value to assign to :class:`~.EgadsData` instance. Can be scalar, array, or other :class:`~.EgadsData` instance.

* units
   Units to assign to :class:`~.EgadsData` instance. Should be string representation of units, and can be a compound units type such as 'g/kg', 'm/s^2', 'feet/second', etc.

* variable metadata
   An instance of the :class:`~.VariableMetadata` type or dictionary, containing keywords and values of any metadata to be associated with this :class:`~.EgadsData` instance.

* other attributes
   Any other attributes added to the class are automatically stored in the :class:`~.VariableMetadata` instance associated with the :class:`~.EgadsData` instance.

The following are examples of creating :class:`~.EgadsData` instances:

   >>> x = egads.EgadsData([1,2,3], 'm')
   >>> a = [1,2,3,4]
   >>> b = egads.EgadsData(a, 'km', b_metadata)
   >>> c = egads.EgadsData(28, 'degC', long_name="current temperature")

If, during the call to :class:`~.EgadsData`, no units are provided, but a variable metadata instance is provided with a units property, this will then be used to define the :class:`~.EgadsData` units:

   >>> x_metadata = egads.core.metadata.VariableMetadata({'units':'m', 'long_name':'Test Variable'})
   >>> x = egads.EgadsData([1,2,3], x_metadata)
   >>> print x.units
   m
   >>> print x.metadata
   {'units': 'm', 'long_name': 'Test Variable'}
   
The :class:`~.EgadsData` is a subclass of the Quantities and Numpy packages. Thus it allows different kind of operations like addition, substraction, slicing, and many more. For each of those operations, a new :class:`~.EgadsData` class is created with all their attributes. 

.. NOTE::
  With mathematical operands, as metadata define an :class:`~.EgadsData` before an operation, and may not reflect the new :class:`~.EgadsData`, it has been decided to not keep the metadata attribute. It's the responsability of the user to add a new :class:`~.VariableMetadata` instance or a dictionary to the new :class:`~.EgadsData` object. It is not true if a user wants to slice an :class:`~.EgadsData`. In that case, metadata are automatically attributed to the new :class:`~.EgadsData`.


Metadata
---------

The metadata object used by :class:`~.EgadsData` is an instance of :class:`~.VariableMetadata`, a dictionary object containing methods to recognize, convert and validate known metadata types. It can reference parent metadata objects, such as those from an algorithm or data file, to enable users to track the source of a particular variable. 

When reading in data from a supported file type (NetCDF, NASA Ames), or doing calculations with an EGADS algorithm, EGADS will automatically populate the associated metadata and assign it to the output variable. However, when creating an :class:`~.EgadsData` instance manually, the metadata must be user-defined.

As mentioned, :class:`~.VariableMetadata` is a dictionary object, thus all metadata are stored as keyword:value pairs. To create metadata manually, simply pass in a dictionary object containing the desired metadata:

   >>> var_metadata_dict = {'long_name':'test metadata object',
                            '_FillValue':-9999}
   >>> var_metadata = egads.core.metadata.VariableMetadata(var_metadata_dict)

To take advantage of its metadata recognition capabilities, a ``conventions`` keyword can be passed with the variable metadata to give a context to these metadata. 

   >>> var_metadata = egads.core.metadata.VariableMetadata(var_metadata_dict, conventions='CF-1.0')

If a particular :class:`~.VariableMetadata` object comes from a file or algorithm, the class attempts to assign the ``conventions`` automatically. While reading from a file, for example, the class attempts to discover the conventions used based on the "Conventions" keyword, if present.


Working with units
-------------------

:class:`~.EgadsData` subclasses Quantities, thus all of the latter's unit comprehension methods are available when using :class:`~.EgadsData`. This section will outline the basics of unit comprehension. A more detailed tutorial of the unit comprehension capabilities can be found at https://python-quantities.readthedocs.io/en/latest

In general, units are assigned to :class:`~.EgadsData` instances when they are being created. 

   >>> a = egads.EgadsData([1,2,3], 'm')
   >>> b = egads.EgadsData([4,5,6], 'meters/second')

Once a unit type has been assigned to an :class:`~.EgadsData` instance, it will remain that class of unit and can only be converted between other types of that same unit. The ``rescale`` method can be used to convert between similar units, but will give an error if an attempt is made to convert to non-compatible units.

   >>> a = egads.EgadsData([1,2,3], 'm')
   >>> a_km = a.rescale('km')
   >>> print a_km
   ['EgadsData', array([0.001, 0.002, 0.003]), 'km']
   >>> a_grams = a.rescale('g')
   ValueError: Unable to convert between units of "m" and "g"

Likewise, arithmetic operations between :class:`~.EgadsData` instances are handled using the unit comprehension provided by Quantities, and behave . For example adding units of a similar type is permitted:

   >>> a = egads.EgadsData(10, 'm')
   >>> b = egads.EgadsData(5, 'km')
   >>> a + b
   ['EgadsData', array(5010.0), 'm']

But, non-compatible types cannot be added. They can, however, be multiplied or divided:

   >>> distance = egads.EgadsData(10, 'm')
   >>> time = egads.EgadsData(1, 's')
   >>> distance + time
   ValueError: Unable to convert between units of "s" and "m"
   >>> distance/time
   ['EgadsData', array(10), 'm/s']

.. raw:: latex

    \newpage

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

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', name='time')
    
* create a new EgadsFile instance:

    >>> f = egads.input.EgadsFile()

* use the following function to open a new file:

    >>> f.open('main_raw_file.dat', 'w')
    
* prepare the headers if necessary:

    >>> headers = '# The current file has been created with EGADS\n# Institution: My Institution\n# Author(s): John Doe\n'
    >>> headers += time.metadata["long_name"] + '    ' + data1.metadata["long_name"] + '    ' + data2.metadata["long_name"] + '\n''My institution')

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
   
Working with CSV files
***********************

:class:`egads.input.text_file_io.EgadsCsv` is designed to easily input or output data in CSV format. Data input using :class:`~.EgadsCsv` is separated into a list of arrays, which each column a separate array in the list. 

Opening
----------

To open a csv file, simply create a :class:`~.EgadsCsv` instance with the parameters *filename*, *perms*, *delimiter* and *quotechar*:

    >>> import egads
    >>> f = egads.input.EgadsCsv('/pathname/filename.nc', 'r', ',','"')

.. function:: EgadsFile(filename[, perms='r', delimiter=',', quotechar='"'])

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

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', name='time')
    
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
   
Working with NetCDF files
**************************

EGADS provides two classes to work with NetCDF files. The simplest, :class:`egads.input.netcdf_io.NetCdf`, allows simple read/write operations to NetCDF files. The other, :class:`egads.input.netcdf_io.EgadsNetCdf`, is designed to interface with NetCDF files conforming to the EUFAR Standards & Protocols data and metadata regulations. This class directly reads or writes NetCDF data using instances of the :class:`~.EgadsData` class.

Opening
--------

To open a NetCDF file, simply create a :class:`~.EgadsNetCdf` instance or a :class:`~.NetCdf` instance with the parameters *filename* and *perms*:

    >>> import egads
    >>> f = egads.input.EgadsNetCdf('/pathname/filename.nc', 'r')

.. function:: EgadsNetCdf(filename[, perms='r'])

   Open a NetCDF file conforming the the EUFAR Standards & Protocols data and metadata regulations.

   :param filename: path and filename of a NetCDF file
   :type filename: string
   :param perms: permissions ; optional
   :type perms: string
   :rtype: NetCDF file.

Valid values for permissions are:

* ``r`` -- Read: opens file for reading only. Default value if nothing is provided.
* ``w`` -- Write: opens file for writing, and overwrites data in file.
* ``a`` -- Append: opens file for appending data.
* ``r+`` -- Same as ``a``.

Getting info
-------------

.. function:: f.get_dimension_list([varname=None])

   Returns a dictionary of all dimensions with their sizes. *varname* is optional and if provided, the function returns a dictionary of all dimensions and their sizes attached to *varname*.

   :param varname: name of a variable ; optional
   :type varname: string
   :rtype: dictionary of dimensions

.. function:: f.get_attribute_list([varname=None])

   Returns a list of all top-level attributes. *varname* is optional and if provided, the function returns a dictionary of all attributes attached to *varname*.
   
   :param varname: name of a variable ; optional
   :type varname: string
   :rtype: dictionary of attributes

.. function:: f.get_variable_list()

   Returns a list of all variables.

   :rtype: list of variables

.. function:: f.get_filename()

   Returns the filename for the currently opened file.

   :rtype: filename
   
.. function:: f.get_perms()

   Returns the current permissions on the file that is open.

   :rtype: permissions


Reading data
-------------

To read data from a file, use the ``read_variable()`` function:

    >>> data = f.read_variable(varname, input_range, read_as_float, replace_fill_value)
	
.. function:: f.read_variable(varname[, input_range=None, read_as_float=False, replace_fill_value=False])

   If using the :class:`~.NetCdf` class, an array of values contained in *varname* will be returned. If using the :class:`~.EgadsNetCdf` class, an instance of the :class:`~.EgadsData` class will be returned containing the values and attributes of *varname*.

   :param varname: name of a variable in the NetCDF file
   :type varname: string
   :param input_range: list of min/max values ; optional
   :type input_range: list
   :param read_as_float: if True, EGADS reads the data and convert them to float numbers, if False, the data type is the type of data in file ; optional
   :type read_as_float: bool
   :param replace_fill_value: if True, EGADS reads the data and replace ``_FillValue`` or ``missing_value`` (if one of the attributes exists) in data by NaN (numpy.nan) ; optional
   :type replace_fill_value: bool
   :rtype: data, :class:`~.EgadsData` or array


Writing data
------------

The following describe how to add dimensions or attributes to a file.

.. function:: f.add_dim(name, size)

   Add a dimension to the NetCDF file.

   :param name: the name of the dimension
   :type name: string
   :param size: the size of the dimension
   :type size: int

.. function:: f.add_attribute(attrname, value[, varname=None])

   Add an attribute to the NetCDF file. If *varname* is None, the attribute is a global attribute, and if not, the attribute is a variable attribute attached to *varname*.

   :param attrname: the name of the attribute
   :type attrname: string
   :param value: the value of the attribute
   :type value: string|float|int
   :param varname: the name of the variable to which to attach the attribute ; optional
   :type varname: string

Data can be output to variables using the ``write_variable()`` function as follows:

    >>> f.write_variable(data, varname, dims, ftype, fillvalue)

.. function:: f.write_variable(data, varname[, dims=None, ftype='double', fillvalue=None])
   
   Write the values contained in *data* in the variable *varname* in a NetCDF file. If using :class:`~.NetCdf`, values for *data* passed into ``write_variable`` must be scalar or array. Otherwise, if using :class:`~.EgadsNetCdf`, an instance of :class:`~.EgadsData` must be passed into ``write_variable``. In this case, any attributes that are contained within the :class:`~.EgadsData` instance are applied to the NetCDF variable as well. If an attribute with a name equal to ``_FillValue`` or ``missing_value`` is found, NaN in data will be automatically replaced by the missing value.

   :param data: values to be stored in the NetCDF file
   :type data: EgadsData|array|vector|scalar
   :param varname: the name of the variable in the NetCDF file
   :type varname: string
   :param dims: a tuple of dimension names for data (not needed if the variable already exists) ; optional
   :type dims: tuple
   :param ftype: the data type of the variable, the default value is *double*, other valid options are *float*, *int*, *short*, *char* and *byte* ; optional
   :type ftype: string
   :param fillvalue: if it is provided, it overrides the default NetCDF _FillValue ; optional, it doesn't exist if using :class:`~.EgadsNetCdf`
   :type fillvalue: float|int


Conversion from NetCDF to NASA Ames file format
------------------------------------------------

The conversion is only possible on opened NetCDF files. If modifications have been made and haven't been saved, the conversion won't take into account those modifications. Actually, the only File Format Index supported by the conversion is 1001. Consequently, if more than one independant variables are present in the NetCDF file, the file won't be converted and the function will raise an exception. If the user needs to convert a complex file with variables depending on multiple independant variables, the conversion should be done manually by creating a NasaAmes instance and a NasaAmes dictionary, by populating the dictionary and by saving the file.

To convert a NetCDF file to NasaAmes file format, simply use:

.. function:: f.convert_to_nasa_ames([na_file=None, float_format=None, delimiter='    ', no_header=False])
   
   Convert the opened NetCDF file to NasaAmes file.

   :param na_file: it is the name of the output file once it has been converted, by default the name of the NetCDF file will be used with the extension .na (*na_file* is None); optional
   :type na_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param delimiter: it is a character or a sequence of character to use between data items in the data file ; optional (by default '    ', 4 spaces)
   :type delimiter: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool

To convert a NetCDF file to NasaAmes CSV file format, simply use:

.. function:: f.convert_to_csv([csv_file=None, float_format=None, no_header=False])
   
   Convert the opened NetCDF file to NasaAmes CSV file.

   :param csv_file: it is the name of the output file once it has been converted, by default the name of the NetCDF file will be used with the extension .csv (*csv_file* is None); optional
   :type csv_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool


Other operations
-----------------

.. function:: f.get_attribute_value(attrname[, varname=None])
   
   Return the value of the global attribute *attrname*, or the value of the variable attribute *attrname* if *varname* is not None.

   :param attrname: the name of the attribute
   :type attrname: string
   :param varname: the name of the variable to which the attribute is attached
   :type varname: string
   :rtype: value of the attribute

.. function:: f.change_variable_name(varname, newname)
   
   Change a variable name in the currently opened NetCDF file..

   :param attrname: the actual name of the variable
   :type attrname: string
   :param varname: the new name of the variable
   :type varname: string


Closing
---------

To close a file, simply use the ``close()`` method:

    >>> f.close()

.. NOTE::
  The EGADS :class:`~.NetCdf` and :class:`~.EgadsNetCdf` use the official NetCDF I/O routines, therefore, as described in the NetCDF documentation, it is not possible to remove a variable or more, and to modify the values of a variable. As attributes, global and those linked to a variable, are more dynamic, it is possible to remove, rename, or replace them.


Tutorial
---------

Here is a NetCDF file, created by EGADS, and viewed by the command ``ncdump -h ....``:
    
.. literalinclude:: example_files/ncdump_example_file.txt

This file has been created with the following commands:

* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', name='time')
    
* create a new EgadsNetCdf instance with a file name:

    >>> f = egads.input.EgadsNetCdf('main_netcdf_file.nc', 'w')
    
* add the global attributes to the NetCDF file:

    >>> f.add_attribute('Conventions', 'CF-1.0')
    >>> f.add_attribute('history', 'the netcdf file has been created by EGADS')
    >>> f.add_attribute('comments', 'no comments on the netcdf file')
    >>> f.add_attribute('institution', 'My institution')

* add the dimension(s) of your variable(s), here it is ``time``:

    >>> f.add_dim('time', len(time))
    
* write the variable(s), it is a good practice to write at the first place the independant variable ``time``:

    >>> f.write_variable(time, 'time', ('time',), 'double')
    >>> f.write_variable(data1, 'sea_level', ('time',), 'double')
    >>> f.write_variable(data2, 'corrected_sea_level', ('time',), 'double')
    
* and do not forget to close the file:

    >>> f.close()

.. raw:: latex

    \newpage

Working with NASA Ames files
*****************************

EGADS provides two classes to work with NASA Ames files. The simplest, :class:`egads.input.nasa_ames_io.NasaAmes`, allows simple read/write operations. The other, :class:`egads.input.nasa_ames_io.EgadsNasaAmes`, is designed to interface with NASA Ames files conforming to the EUFAR Standards & Protocols data and metadata regulations. This class directly reads or writes NASA Ames file using instances of the :class:`~.EgadsData` class. Actually, only the FFI 1001 has been interfaced with EGADS.

Opening
--------

To open a NASA Ames file, simply create a :class:`.EgadsNasaAmes` instance with the parameters *pathname* and *permissions*:

    >>> import egads
    >>> f = egads.input.EgadsNasaAmes('/pathname/filename.na','r')

.. function:: EgadsNasaAmes(pathname[, permissions='r'])
   
   Open a NASA Ames file conforming the the EUFAR Standards & Protocols data and metadata regulations.

   :param filename: path and filename of a NASA Ames file
   :type filename: string
   :param perms: permissions ; optional
   :type perms: string
   :rtype: NasaAmes file.

Valid values for permissions are:

* ``r`` -- Read: opens file for reading only. Default value if nothing is provided.
* ``w`` -- Write: opens file for writing, and overwrites data in file.
* ``a`` -- Append: opens file for appending data.
* ``r+`` -- Same as ``a``.

Once a file has been opened, a dictionary of NASA/Ames format elements is loaded into memory. That dictionary will be used to overwrite the file or to save a new file.

Getting info
------------

.. function:: f.get_dimension_list([na_dict=None])

   Returns a list of all variable dimensions.

   :param na_dict: if provided, the function get dimensions from the NasaAmes dictionary *na_dict*, if not dimensions are from the opened file ; optional
   :type na_dict: dict
   :rtype: dictionary of dimensions

.. function:: f.get_attribute_list([varname=None, vartype='main', na_dict=None])

   Returns a dictionary of all top-level attributes.
   
   :param varname: name of a variable, if provided, the function returns a dictionary of all attributes attached to *varname* ; optional
   :type varname: string
   :param vartype: if provided and *varname* is not ``None``, the function will search in the variable type *vartype* by default ; optional
   :type vartype: string
   :param na_dict: if provided, it will return a list of all top-level attributes, or all *varname* attributes, from the NasaAmes dictionary *na_dict* ; optional
   :type na_dict: dict
   :rtype: dictionary of attributes

.. function:: f.get_attribute_value(attrname[, varname=None, vartype='main', na_dict=None])

   Returns the value of a top-level attribute named *attrname*.
   
   :param attrname: the name of the attribute
   :type attrname: string
   :param varname: name of a variable, if provided, the function returns the value of the attribute attached to *varname* ; optional
   :type varname: string
   :param vartype: if provided and *varname* is not ``None``, the function will search in the variable type *vartype* by default ; optional
   :type vartype: string
   :param na_dict: if provided, it will return the value of an attribute from the NasaAmes dictionary *na_dict* ; optional
   :type na_dict: dict
   :rtype: value of attribute

.. function:: f.get_variable_list([na_dict=None])

   Returns a list of all variables.

   :param na_dict: if provided, it will return the list of all variables from the NasaAmes dictionary *na_dict* ; optional
   :type na_dict: dict
   :rtype: list of variables

.. function:: f.get_filename()

   Returns the filename for the currently opened file.

   :rtype: filename
   
.. function:: f.get_perms()

   Returns the current permissions on the file that is open.

   :rtype: permissions


Reading data
------------

To read data from a file, use the ``read_variable()`` function:

    >>> data = f.read_variable(varname, na_dict, read_as_float, replace_fill_value)

.. function:: f.read_variable(varname[, na_dict=None, read_as_float=False, replace_fill_value=False])

   If using the :class:`~.NasaAmes` class, an array of values contained in *varname* will be returned. If using the :class:`~.EgadsNasaAmes` class, an instance of the :class:`~.EgadsData` class will be returned containing the values and attributes of *varname*.

   :param varname: name of a variable in the NasaAmes file
   :type varname: string
   :param na_dict: it will tell to EGADS in which Nasa Ames dictionary to read data, if na_dict is ``None``, data are read in the opened file ; optional
   :type na_dict: dict
   :param read_as_float: if True, EGADS reads the data and convert them to float numbers, if False, the data type is the type of data in file ; optional
   :type read_as_float: bool
   :param replace_fill_value: if True, EGADS reads the data and replace ``_FillValue`` or ``missing_value`` (if one of the attributes exists) in data by NaN (numpy.nan) ; optional
   :type replace_fill_value: bool
   :rtype: data, :class:`~.EgadsData` or array


Writing data
-------------

To write data to the current file or to a new file, the user must save a dictionary of NasaAmes elements. Few functions are available to help him to prepare the dictionary:

.. function:: f.create_na_dict()

   Create a new dictionary populated with standard NasaAmes keys

.. function:: f.write_attribute_value(attrname, attrvalue[, na_dict=None, varname=None, vartype='main'])

   Write or replace a specific attribute (from the official NasaAmes attribute list) in the currently opened dictionary.

   :param attrname: name of the attribute in the NasaAmes dictionary
   :type attrname: string
   :param attrvalue: value of the attribute
   :type attrvalue: string|float|integer|list|array
   :param na_dict: if provided the function will write the attribute in the NasaAmes dictionary *na_dict* ; optional
   :type na_dict: dict
   :param varname: if provided, write or replace a specific attribute linked to the variable *var_name* in the currently opened dictionary ; accepted attributes for a variable are 'name', 'units', '_FillValue' and 'scale_factor', other attributes will be refused and should be passed as 'special comments' ; optional
   :type varname: string
   :param vartype: if provided and *varname* is not ``None``, the function will search in the variable type *vartype* by default ; optional
   :type vartype: string

.. function:: f.write_variable(data[, varname=None, vartype='main', attrdict=None, na_dict=None])

   Write or replace a variable in the currently opened dictionary. If using the :class:`~.NasaAmes` class, an array of values for *data* is asked. If using the :class:`~.EgadsNasaAmes` class, an instance of the :class:`~.EgadsData` class must be injected for *data*. If a :class:`~.EgadsData` is passed into the ``write_variable`` function, any attributes that are contained within the :class:`~.EgadsData` instance are automatically populated in the NASA Ames dictionary as well, those which are not mandatory are stored in the 'SCOM' attribute. If an attribute with a name equal to ``_FillValue`` or ``missing_value`` is found, NaN in data will be automatically replaced by the missing value.

   :param data: values to be stored in the NasaAmes file
   :type data: EgadsData|array|vector|scalar
   :param varname: the name of the variable ; if data is an :class:`~.EgadsData`, mandatory if 'standard_name' or 'long_name' is not an attribute of *data* ; absolutely mandatory if *data* is not an :class:`~.EgadsData` ; optional
   :type varname: string
   :param vartype: the type of *data*, 'independant' or 'main', only mandatory if *data* must be stored as an independant variable (dimension) ; optional
   :type vartype: string
   :param attrdict: a dictionary containing mandatory attributes ('name', 'units', '_FillValue' and 'scale_factor'), only mandatory if *data* is not an :class:`~.EgadsData` ; optional
   :type attrdict: dict
   :param na_dict: if provided, the function stores the variable in the NasaAmes dictionary *na_dict*
   :type na_dict: dict


Saving a file
--------------

Once a dictionary is ready, use the ``save_na_file()`` function to save the file:

    >>> data = f.save_na_file(filename, na_dict, float_format, delimiter, no_header):

.. function:: f.save_na_file([filename=None, na_dict=None, float_format=None, delimiter='    ', no_header=False])

   Save the opened NasaAmes dictionary and file.

   :param filename: is the name of the new file, if not provided, the name of the opened NasaAmes file is used ; optional
   :type filename: string
   :param na_dict: the name of the NasaAmes dictionary to be saved, if not provided, the opened dictionary will be used  ; optional
   :type na_dict: dict
   :param float_format: the format of the floating numbers in the file (by default, no round up) ; optional
   :type float_format: string
   :param delimiter: it is a character or a sequence of character to use between data items in the data file ; optional (by default '    ', 4 spaces)
   :type delimiter: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool


Conversion from NASA/Ames file format to NetCDF
------------------------------------------------

When a NASA/Ames file is opened, all metadata and data are read and stored in memory in a dedicated dictionary. The conversion will convert that dictionary to generate a NetCDF file. If modifications are made to the dictionary, the conversion will take into account those modifications. Actually, the only File Format Index supported by the conversion in the NASA Ames format is 1001. Consequently, if variables depend on multiple independant variables (e.g. ``data`` is function of ``time``, ``longitude`` and ``latitude``), the file won't be converted and the function will raise an exception. If the user needs to convert a complex file with variables depending on multiple independant variables, the conversion should be done manually by creating a NetCDF instance and by populating the NetCDF files with NASA/Ames data and metadata.

To convert a NASA/Ames file, simply use:

.. function:: f.convert_to_netcdf([nc_file=None, na_dict=None])

   Convert the opened NasaAmes file to NetCDF file format.
   
   :param nc_file: if provided, the function will use *nc_file* for the path and name of the new_file, if not, the function will take the name and path of the opened NasaAmes file and replace the extension by '.nc' ; optional
   :type nc_file: string
   :param na_dict: the name of the NasaAmes dictionary to be converted, if not provided, the opened dictionary will be used  ; optional
   :type na_dict: dict


Other operations
-----------------

.. function:: f.read_na_dict()

   Returns a deep copy of the current opened file dictionary
   
   :rtype: deep copy of a dictionary

.. function:: egads.input.nasa_ames_io.na_format_information()

   Returns a text explaining the structure of a NASA/Ames file to help the user to modify or to create his own dictionary
   
   :rtype: string


Closing
---------

To close a file, simply use the ``close()`` method:

    >>> f.close()

Tutorial
---------

Here is a NASA/Ames file:
    
.. literalinclude:: example_files/na_example_file.na

This file has been created with the following commands:


* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', name='sea level', scale_factor=1, _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', name='corr sea level', scale_factor=1, _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', name='time')
    
* create a new NASA/Ames empty instance:

    >>> f = egads.input.NasaAmes()
    
* initialize a new NASA/Ames dictionary:

    >>> na_dict = f.create_na_dict()

* prepare the normal and special comments if needed, in a list, one cell for each line, or only one string with lines separated by ``\n``:

    >>> scom = ['========SPECIAL COMMENTS===========','this file has been created with egads','=========END=========']
    >>> ncom = ['========NORMAL COMMENTS===========','headers:','time    sea level   corrected sea level','=========END=========']
    or
    >>> scom = '========SPECIAL COMMENTS===========\nthis file has been created with egads\n=========END========='
    >>> ncom = '========NORMAL COMMENTS===========\nheaders:\ntime    sea level   corrected sea level\n=========END========='
    
* populate the main NASA/Ames attributes:

    >>> f.write_attribute_value('ONAME', 'John Doe', na_dict = na_dict) # ONAME is the name of the author(s)
    >>> f.write_attribute_value('ORG', 'An institution', na_dict = na_dict) # ORG is tne name of the organization responsible for the data
    >>> f.write_attribute_value('SNAME', 'tide gauge', na_dict = na_dict) # SNAME is the source of data (instrument, observation, platform, ...)
    >>> f.write_attribute_value('MNAME', 'ATESTPROJECT', na_dict = na_dict) # MNAME is the name of the mission, campaign, programme, project dedicated to data
    >>> f.write_attribute_value('DATE', [2017, 1, 30], na_dict = na_dict) # DATE is the date at which the data recorded in this file begin (YYYY MM DD)
    >>> f.write_attribute_value('NIV', 1, na_dict = na_dict) # NIV is the number of independent variables
    >>> f.write_attribute_value('NSCOML', 3, na_dict = na_dict) # NSCOML is the number of special comments lines or the number of elements in the SCOM list
    >>> f.write_attribute_value('NNCOML', 4, na_dict = na_dict) # NNCOML is the number of special comments lines or the number of elements in the NCOM list
    >>> f.write_attribute_value('SCOM', scom, na_dict = na_dict) # SCOM is the special comments attribute
    >>> f.write_attribute_value('NCOM', ncom, na_dict = na_dict) # NCOM is the normal comments attribute
    
* write each variable in the dictionary:

    >>> f.write_variable(time, 'time', vartype="independant", na_dict = na_dict)
    >>> f.write_variable(data1, 'sea level', vartype="main", na_dict = na_dict)
    >>> f.write_variable(data2, 'corrected sea level', vartype="main", na_dict = na_dict)

    
* and finally, save the dictionary to a NASA/Ames file:

    >>> f.save_na_file('na_example_file.na', na_dict)

.. raw:: latex

    \newpage

Working with algorithms
************************

Algorithms in EGADS are stored in the :mod:`egads.algorithms` module, and separated into sub-modules by category (microphysics, thermodynamics, radiation, etc). Each algorithm follows a standard naming scheme, using the algorithm's purpose and source:

``{CalculatedParameter}{Detail}{Source}``

For example, an algorithm which calculates static temperature, which was provided by CNRM would be named:

``TempStaticCnrm``

Getting algorithm information
-----------------------------

There are several methods to get information about each algorithm contained in EGADS. The EGADS Algorithm Handbook is available for easy reference outside of Python. In the handbook, each algorithm is described in detail, including a brief algorithm summary, descriptions of algorithm inputs and outputs, the formula used in the algorithm, algorithm source and links to additional references. The handbook also specifies the exact name of the algorithm as defined in EGADS. The handbook can be found on the EGADS website.

Within Python, usage information on each algorithm can be found using the ``help()`` command::

   	>>> help(egads.algorithms.thermodynamics.VelocityTasCnrm)
	
	>>> Help on class VelocityTasCnrm in module egads.algorithms.thermodynamics.
	    velocity_tas_cnrm:

	class VelocityTasCnrm(egads.core.egads_core.EgadsAlgorithm)
	 |  FILE        velocity_tas_cnrm.py
	 | 
	 |  VERSION     $Revision: 104 $
	 |  
	 |  CATEGORY    Thermodynamics
	 |  
	 |  PURPOSE     Calculate true airspeed
	 |  
	 |  DESCRIPTION Calculates true airspeed based on static temperature, 
	 |              static pressure and dynamic pressure using St Venant's 
	 |              formula.
	 |  
	 |  INPUT       T_s         vector  K or C      static temperature
	 |              P_s         vector  hPa         static pressure
	 |              dP          vector  hPa         dynamic pressure
	 |              cpa         coeff.  J K-1 kg-1  specific heat of air (dry 
	 |                                              air is 1004 J K-1 kg-1)
	 |              Racpa       coeff.  ()          R_a/c_pa
	 |  
	 |  OUTPUT      V_p         vector  m s-1       true airspeed
	 |  
	 |  SOURCE      CNRM/GMEI/TRAMM
	 |  
	 |  REFERENCES  "Mecanique des fluides", by S. Candel, Dunod.
	 |  
	 |               Bulletin NCAR/RAF Nr 23, Feb 87, by D. Lenschow and
	 |               P. Spyers-Duran
	 |  
	...


Calling algorithms
-------------------

Algorithms in EGADS generally accept and return arguments of :class:`~.EgadsData` type, unless otherwise noted. This has the advantages of constant typing between algorithms, and allows metadata to be passed along the whole processing chain. Units on parameters being passed in are also checked for consistency, reducing errors in calculations, and rescaled if needed. However, algorithms will accept any normal data type, as well. They can also return non-:class:`~.EgadsData` instances, if desired.

To call an algorithm, simply pass in the required arguments, in the order they are described in the algorithm help function. An algorithm call, using the ``VelocityTasCnrm`` in the previous section as an example, would therefore be the following:

    >>> V_p = egads.algorithms.thermodynamics.VelocityTasCnrm().run(T_s, P_s, dP, 
        cpa, Racpa)	

where the arguments ``T_s``, ``P_s``, ``dP``, etc are all assumed to be previously defined in the program scope. In this instance, the algorithm returns an :class:`~.EgadsData` instance to ``V_p``. To run the algorithm, but return a standard data type (scalar or array of doubles), set the ``return_Egads`` flag to ``false``.

    >>> V_p = egads.algorithms.thermodynamics.VelocityTasCnrm(return_Egads=False).
        run(T_s, P_s, dP, cpa, Racpa)

.. NOTE::
  When injecting a variable in an EgadsAlgorithm, the format of the variable should follow closely the documentation of the algorithm. If the variable is a scalar, and the algorithm needs a vector, the scalar should be surrounded by brackets: 52.123 -> [52.123].
        
.. raw:: latex

    \newpage
        
Scripting
**********

The recommended method for using EGADS is to create script files, which are extremely useful for common or repetitive tasks. This can be done using a text editor of your choice. The example script belows shows the calculation of density for all NetCDF files in a directory.

.. literalinclude:: example_files/example.py

Scripting Hints
----------------

When scripting in Python, there are several important differences from other programming languages to keep in mind. This section outlines a few of these differences.

Importance of white space
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python differs from C++ and Fortran in how loops or nested statements are signified. Whereas C++ uses brackets ('``{``' and '``}``') and FORTRAN uses ``end`` statements to signify the end of a nesting, Python uses white space. Thus, for statements to nest properly, they must be set at the proper depth. As long as the document is consistent, the number of spaces used doesn't matter, however, most conventions call for 4 spaces to be used per level. See below for examples:

**FORTRAN**::

	X = 0
	DO I = 1,10
	  X = X + I
	  PRINT I
	END DO
	PRINT X

**Python**::

	x = 0
	for i in range(1,10):
	    x = x + i
	    print i
	print x

.. raw:: latex

    \newpage
	
Using the GUI
**************

Since September 2016, a Graphical User Interface is available at https://github.com/eufarn7sp/egads-gui. It gives the user the possibility to explore data, apply/create algorithms, display and plot data. Still in beta state, the user will have the possibility in the future to work on a batch of file. For now, EGADS GUI comes as a simple python script and need to be launch from the terminal, if EGADS is installed, and once in the EGADS GUI directory:

    >>> python egads_gui.py

It will be available soon as a stand alone (imbedding a version of EGADS CORE or using an already installed EGADS package).

.. NOTE::
  As for EGADS, the Graphical User Interface is available from two branches: master and Lineage (https://github.com/EUFAR/egads-gui/tree/Lineage). The Lineage one is only compatible with Python 3 and the earlier versions of EGADS Lineage.

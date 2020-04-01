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


Conversion from NASA/Ames file format to Hdf5
------------------------------------------------

When a NASA/Ames file is opened, all metadata and data are read and stored in memory in a dedicated dictionary. The conversion will convert that dictionary to generate a Hdf file. If modifications are made to the dictionary, the conversion will take into account those modifications. Actually, the only File Format Index supported by the conversion in the NASA Ames format is 1001. Consequently, if variables depend on multiple independant variables (e.g. ``data`` is function of ``time``, ``longitude`` and ``latitude``), the file won't be converted and the function will raise an exception. If the user needs to convert a complex file with variables depending on multiple independant variables, the conversion should be done manually by creating a Hdf instance and by populating the Hdf files with NASA/Ames data and metadata.

To convert a NASA/Ames file, simply use:

.. function:: f.convert_to_hdf([hdf_file=None, na_dict=None])

   Convert the opened NasaAmes file to Hdf file format.
   
   :param hdf_file: if provided, the function will use *hdf_file* for the path and name of the new_file, if not, the function will take the name and path of the opened NasaAmes file and replace the extension by '.h5' ; optional
   :type hdf_file: string
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

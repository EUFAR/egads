Working with Hdf files
**************************

EGADS provides two classes to work with Hdf files. The simplest, :class:`egads.input.hdf_io.Hdf`, allows simple read/write operations to Hdf files. The other, :class:`egads.input.hdf_io.EgadsHdf`, is designed to interface with Hdf files conforming to the EUFAR Standards & Protocols data and metadata regulations. This class directly reads or writes Hdf data using instances of the :class:`~.EgadsData` class.

Opening
--------

To open a Hdf file, simply create a :class:`~.EgadsHdf` instance or a :class:`~.Hdf` instance with the parameters *filename* and *perms*:

    >>> import egads
    >>> f = egads.input.EgadsHdf('/pathname/filename.nc', 'r')

.. function:: EgadsHdf(filename[, perms='r'])

   Open a Hdf file conforming the the EUFAR Standards & Protocols data and metadata regulations.

   :param filename: path and filename of a Hdf file
   :type filename: string
   :param perms: permissions ; optional
   :type perms: string
   :rtype: Hdf file.

Valid values for permissions are:

* ``r`` -- Read: opens file for reading only. Default value if nothing is provided.
* ``w`` -- Write: opens file for writing, and overwrites data in file.
* ``a`` -- Append: opens file for appending data.
* ``r+`` -- Same as ``a``.


Getting info
-------------

.. function:: f.get_dimension_list([varname=None, group_walk=False, details=False])

   Returns a dictionary of all dimensions with their sizes. *varname* is optional and can take three different forms: *varname* is a variable name, and in that case the function returns a dictionary of all dimensions and their sizes attached to *varname* at the root of the Hdf file ; *varname* is a path to a group + a variable name, the function returns a dictionary of all dimensions and their sizes attached to *varname* in the specified group ; *varname* is a path to a group + a group name, the function returns a dictionary of all dimensions and their sizes in the specified group. *group_walk* is optional and if True, the function will explore the entire file is *varname* is None, or from a specified group if *varname* is a group path. *details* is optional, and if True, the path of each dimension is included in the final dictionary.

   :param varname: Name of variable or group to get the list of associated dimensions from. If no variable name is provided, the function returns all dimensions at the root of the Hdf file ; optional
   :type varname: string
   :param bool group_walk: if True, the function visits all groups (if at least one exists) to list all dimensions. False by default ; optional
   :type group_walk: bool
   :param bool details: if True, dimension path is provided in the dictionary. False by default ; optional
   :type details: bool
   :rtype: ordered dictionary of dimensions
   
   >>> print(f.get_dimension_list('temperature'))
   >>> print(f.get_dimension_list('test1/data/temperature'))
   >>> print(f.get_dimension_list('test1/data'))

.. function:: f.get_attribute_list([objectname=None])

   Returns a list of all top-level attributes. *varname* is optional and can take three different forms: *objectname* is a variable name, and in that case the function returns all attributes and their values attached to *objectname* at the root of the Hdf file ; *objectname* is a path to a group + a variable name, the function returns all attributes and their values attached to *objectname* in the specified group ; *objectname* is a path to a group + a group name, the function returns all attributes and their values attached to the specified group.
   
   :param objectname: name of a variable / group ; optional
   :type objectname: string
   :rtype: dictionary of attributes
   
   >>> print(f.get_attribute_list('temperature'))
   >>> print(f.get_attribute_list('test1/data/temperature'))
   >>> print(f.get_attribute_list('test1/data'))

.. function:: f.get_variable_list([groupname=None, group_walk=False, details=False])

   Returns a list of all variables at the root of the Hdf file if *groupname* is None, otherwise a list of all variables in the group *groupname*. If *group_walk* is True, the the function will explore all the file or from *groupname* if *groupname* is provided. If *details* is True, the function returns a list of dictionary containing the name of the variable and its path in the Hdf file. By default, details is False and the function returns a simple list of variable names.
   
   :param groupname: the name of the group to get the list from ; optional
   :type groupname: string
   :param group_walk: if True, the function visits all groups (if at least one exists) to list all variables. False by default ; optional
   :type group_walk: bool
   :param details: if True, the function returns a list of dictionary in which the key is the name of the variable, and the value is the path of the variable in the Hdf file ; optional
   :type details: bool
   :rtype: list of variables
   
   >>> print(f.get_variable_list())
   >>> print(f.get_variable_list(details=True))

.. function:: f.get_file_structure()

   Returns a view of the file structure, groups and datasets.
   
   :rtype: list of strings and Hdf objects
   
   >>> print(f.get_file_structure())

.. function:: f.get_group_list([groupname=None, details=False])

   Returns a list of groups found in the Hdf file. If *groupname* is provided, the function returns all groups from *groupname* to the last group in *groupname*. The function returns a list of string if details is False. If details is True, it returns a list of dictionary in which the key is the name of the group and the value its path in the Hdf file.
   
   :param groupname: name of a group where to get the group list ; optional
   :type groupname: string
   :param details: if True, the function returns a list of dictionary in which the key is the name of the group and the value its path in the Hdf file ; optional
   :type details: bool
   :rtype: list of strings or list of dictionary
   
   >>> print(f.get_group_list())
   >>> print(f.get_group_list('test1', True))

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

   If using the :class:`~.Hdf` class, an array of values contained in *varname* will be returned. If using the :class:`~.EgadsHdf` class, an instance of the :class:`~.EgadsData` class will be returned containing the values and attributes of *varname*. If a group path is present in *varname*, then the function reads the variable *varname* in that specified group.

   :param varname: name of a variable, with or without group path, in the Hdf file
   :type varname: string
   :param input_range: list of min/max values ; optional
   :type input_range: list
   :param read_as_float: if True, EGADS reads the data and convert them to float numbers, if False, the data type is the type of data in file ; optional
   :type read_as_float: bool
   :param replace_fill_value: if True, EGADS reads the data and replace ``_FillValue`` or ``missing_value`` (if one of the attributes exists) in data by NaN (numpy.nan) ; optional
   :type replace_fill_value: bool
   :rtype: data, :class:`~.EgadsData` or array
   
   >>> data = f.read_variable('temperature')
   >>> data = f.read_variable('test1/data/temperature')


Writing data
------------

The following describe how to add dimensions or attributes to a file.

.. function:: f.add_dim(name, data[, ftype='double'])

   Add a dimension to the Hdf file. The name of the dimension can include a path to a group where to store the dimension. In that case, the group has to be created before. If using :class:`~.Hdf`, values for *data* passed into ``add_dim`` must be scalar or array. Otherwise, if using :class:`~.EgadsHdf`, an instance of :class:`~.EgadsData` must be passed into ``add_dim``. In this case, any attributes that are contained within the :class:`~.EgadsData` instance are applied to the Hdf variable as well.

   :param name: the name of the dimension, or the path to a group + the name of the dimension
   :type name: string
   :param data: values to be stored in the Hdf file
   :type data: EgadsData|array|vector|scalar
   :param ftype: the data type of the variable, the default value is *double*, other valid options are *float*, *int*, *short*, *char* and *byte* ; optional
   :type ftype: string
   
   >>> f.add_dim('time', time_data, len(time))
   >>> f.add_dim('test1/data/time', time_data, len(time))

.. function:: f.add_attribute(attrname, value[, objname=None])

   Add an attribute to the Hdf file. If *objname* is None, the attribute is a global attribute, and if not, the attribute is attached to *objname*. *objname* can be a group (with or without a path) or variable (with or without a path).

   :param attrname: the name of the attribute
   :type attrname: string
   :param value: the value of the attribute
   :type value: string|float|int
   :param objname: the name of the variable | group to which to attach the attribute ; optional
   :type objname: string
   
   >>> f.add_attribute('project', 'my project')
   >>> f.add_attribute('project', 'my project', 'temperature')
   >>> f.add_attribute('project', 'my project', 'test1/data/temperature')
   >>> f.add_attribute('project', 'my project', 'test1/data')
   
Data can be output to variables using the ``write_variable()`` function as follows:

    >>> f.write_variable(data, varname, dims, ftype, fillvalue)

.. function:: f.write_variable(data, varname[, dims=None, ftype='double'])
   
   Write the values contained in *data* in the variable *varname* in a Hdf file. If *varname* contains a path to a group, the variable will be created in the specified group, but in that case the group has to be created before. If using :class:`~.Hdf`, values for *data* passed into ``write_variable`` must be scalar or array. Otherwise, if using :class:`~.EgadsHdf`, an instance of :class:`~.EgadsData` must be passed into ``write_variable``. In this case, any attributes that are contained within the :class:`~.EgadsData` instance are applied to the Hdf variable as well.

   :param data: values to be stored in the Hdf file
   :type data: EgadsData|array|vector|scalar
   :param varname: the name of the variable, or the path of group + the name of the variable, in the Hdf file
   :type varname: string
   :param dims: a tuple of dimension names for data (not needed if the variable already exists) ; optional
   :type dims: tuple
   :param ftype: the data type of the variable, the default value is *double*, other valid options are *float*, *int*, *short*, *char* and *byte* ; optional
   :type ftype: string
   
   >>> f.write_variable(data, 'particle_size', ('time', ))
   >>> f.write_variable(data, 'test1/data/particle_size', ('time', ))


Conversion from Hdf5 to NASA Ames file format
------------------------------------------------

The conversion is only possible on opened Hdf files and with variables at the root of the Hdf file. If modifications have been made and haven't been saved, the conversion won't take into account those modifications. Actually, the only File Format Index supported by the conversion is 1001. Consequently, if more than one independant variables are present in the Hdf file, the file won't be converted and the function will raise an exception. If the user needs to convert a complex file with variables depending on multiple independant variables, and with the presence of groups, the conversion should be done manually by creating a NasaAmes instance and a NasaAmes dictionary, by populating the dictionary and by saving the file.

To convert a Hdf file to NasaAmes file format, simply use:

.. function:: f.convert_to_nasa_ames([na_file=None, float_format=None, delimiter='    ', no_header=False])
   
   Convert the opened NetCDF file to NasaAmes file.

   :param na_file: it is the name of the output file once it has been converted, by default, *na_file* is None, and the name of the Hdf file will be used with the extension .na ; optional
   :type na_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param delimiter: it is a character or a sequence of character to use between data items in the data file ; optional (by default '    ', 4 spaces)
   :type delimiter: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool
   
   >>> f.convert_to_nasa_ames(na_file='nc_converted_to_na.na', float_format='%.8f', delimiter=';', no_header=False)

To convert a Hdf file to NasaAmes CSV file format, simply use:

.. function:: f.convert_to_csv([csv_file=None, float_format=None, no_header=False])
   
   Convert the opened Hdf file to NasaAmes CSV file.

   :param csv_file: it is the name of the output file once it has been converted, by default, *na_file* is None, and the name of the Hdf file will be used with the extension .csv ; optional
   :type csv_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool


Conversion from Hdf5 to NetCDF file format
------------------------------------------

EGADS Lineage offers a direct possibility to convert a full Hdf file to NetCDF file format. In the case of complexe Hdf5 files, a manual NetCDF file creation and editing is still possible.

.. function:: f.convert_to_netcdf([filename=None])

	Converts the opened Hdf file to NetCdf format following the EUFAR and EGADS convention. If groups exist, they are preserved in the new NetCDF file.
	
	:param filename: if only a name is given, a NetCDF file named ``filename`` is created in the HDF file folder ; if a path and a name are given, a NetCDF file named ``name`` is created in the folder ``path`` ; optional
	:type filename: string


Other operations
-----------------

.. function:: f.get_attribute_value(attrname[, objectname=None])
   
   Return the value of the global attribute *attrname*, or the value of the variable attribute *attrname* if *objectname* is not None. If *objectname* contains a path to a group + a variable name, the function returns the attribute value attached to the variable in the specified group. If *objectname* is simple path of group, the functions returns the attribute value attached to the group.

   :param attrname: the name of the attribute
   :type attrname: string
   :param objectname: the name of the variable | group to which the attribute is attached
   :type objectname: string
   :rtype: value of the attribute
   
   >>> print(f.get_attribute_value('project'))
   >>> print(f.get_attribute_value('long_name', 'temperature'))
   >>> print(f.get_attribute_value('long_name', 'test1/data/temperature'))
   >>> print(f.get_attribute_value('project', 'test1/data'))

.. function:: f.add_group(groupname)

   Create a group in the Hdf file. *groupname* can be a path + a group name or a sequence of group, in both cases, intermediary groups are created if needed.
   
   :param groupname: a group name or a list of group name
   :type groupname: string|list
   
   >>> f.add_group('MSL/north_atlantic/data')
   >>> f.add_group(['MSL', 'north_atlantic', 'data'])

.. function:: f.delete_attribute(attrname[, objectname=None])
   
   Delete the attribute *attrname* at the root of the Hdf file if *objectname* is None, or attached to *objectname*. *objectname* can be the name of a variable or a group, or a path to a group plus the name of a variable or a group.
   
   :param attrname: the name of the attribute
   :type attrname: string
   :param objectname: the name of the variable | group to which the attribute is attached
   :type objectname: string
   
   >>> f.delete_attribute('long_name')
   >>> f.delete_attribute('long_name', 'temperature')
   >>> f.delete_attribute('long_name', 'test1/data/temperature')
   >>> f.delete_attribute('project', 'test1/data')

.. function:: f.delete_group(groupname)
   
   Delete the group *groupname* in the Hdf file. *groupname* can be a name of a group at the root of the Hdf file, or a path to a group plus the name of a a group.
   
   :param attrname: the name of the group
   :type attrname: string
   
   >>> f.delete_group('data')
   >>> f.delete_group('test1/data')

.. function:: f.delete_variable(varname)
   
   Delete the variable *varname* in the Hdf file. *varname* can be the name of a variable or a path to a group plus the name of a variable.

   :param varname: the name of the variable
   :type varname: string
   
   >>> f.delete_variable('temperature')
   >>> f.delete_variable('test1/data/temperature')


Closing
---------

To close a file, simply use the ``close()`` method:

    >>> f.close()


Dataset with compound data
--------------------------

Dataset with compound data are not specifically handled by EGADS. When a dataset is read and contains compound data, it is possible to access the different fields in this way:

    >>> temperature = f.read_variable('temperature')
    >>> date_field = temperature['date']

Obviously, if the user declared an EgadsHdf instance to read the file, the compound data is still an EgadsData instance, with the same metadata and units. If the user declared an Hdf instance to read the file, the compound data is a Numpy ndarray instance.
In EGADS, units are handled automatically. Thus, with compound data and multiple data in the same dataset, it is highly likely that units won't be handled properly, and will be set to dimensionless most of the time.

.. NOTE::
  With the instance EgadsHdf, an attribute has been added to the EgadsData instance, ``compound_data``, which informs the user about the dataset type. If the dataset contains compound data, the attribute ``compound_data`` is set to ``True`` ; if not it is set to ``False``. Then it is the responsability of the user to explore the different fields in the dataset.


Tutorial
---------

Here is a Hdf file, created by EGADS, and viewed by the command ``ncdump -h ....``:
    
.. literalinclude:: example_files/ncdump_hdf_example_file.txt

This file has been created with the following commands:

* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', name='time')
    
* create a new EgadsHdf instance with a file name:

    >>> f = egads.input.EgadsHdf('main_hdf_file.hdf5', 'w')
    
* add the global attributes to the Hdf file:

    >>> f.add_attribute('Conventions', 'CF-1.0')
    >>> f.add_attribute('history', 'the hdf file has been created by EGADS')
    >>> f.add_attribute('comments', 'no comments on the hdf file')
    >>> f.add_attribute('institution', 'My institution')

* add the dimension(s) of your variable(s), here it is ``time``:

    >>> f.add_dim('time', time)
    
* write the variable(s), and no need to write the variable ``time``, it has already been added by the command ``add_dim()``:

    >>> f.write_variable(data1, 'sea_level', ('time',), 'double')
    >>> f.write_variable(data2, 'corrected_sea_level', ('time',), 'double')
    
* and do not forget to close the file:

    >>> f.close()

.. raw:: latex

    \newpage

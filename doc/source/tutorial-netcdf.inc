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

.. function:: f.get_dimension_list([varname=None, group_walk=False, details=False])

   Returns a dictionary of all dimensions with their sizes. *varname* is optional and can take three different forms: *varname* is a variable name, and in that case the function returns a dictionary of all dimensions and their sizes attached to *varname* at the root of the NetCDF file ; *varname* is a path to a group + a variable name, the function returns a dictionary of all dimensions and their sizes attached to *varname* in the specified group ; *varname* is a path to group + a group name, the function returns a dictionary of all dimensions and their sizes in the specified group. *group_walk* is optional and if True, the function will explore the entire file is *varname* is None, or from a specified group if *varname* is a group path. *details* is optional, and if True, the path of each dimension is included in the final dictionary.

   :param varname: Name of variable or group to get the list of associated dimensions from. If no variable name is provided, the function returns all dimensions at the root of the NetCDF file ; optional
   :type varname: string
   :param bool group_walk: if True, the function visits all groups (if at least one exists) to list all dimensions. False by default ; optional
   :type group_walk: bool
   :param bool details: if True, dimension path is provided in the dictionary. False by default ; optional
   :type details: bool
   :rtype: ordered dictionary of dimensions
   
   >>> print(f.get_dimension_list('temperature'))
   >>> print(f.get_dimension_list('test1/data/temperature', details=True))
   >>> print(f.get_dimension_list('test1/data', group_walk=True))

.. function:: f.get_attribute_list([varname=None])

   Returns a list of all top-level attributes. *varname* is optional and can take three different forms: *varname* is a variable name, and in that case the function returns all attributes and their values attached to *varname* at the root of the NetCDF file ; *varname* is a path to a group + a variable name, the function returns all attributes and their values attached to *varname* in the specified group ; *varname* is a path to group + a group name, the function returns all attributes and their values attached to the specified group.
   
   :param varname: Name of variable or group to get the list of attributes from. If no variable name is provided, the function returns top-level NetCDF attributes ; optional
   :type varname: string
   :rtype: dictionary of attributes
   
   >>> print(f.get_attribute_list('temperature'))
   >>> print(f.get_attribute_list('test1/data/temperature'))
   >>> print(f.get_attribute_list('test1/data'))

.. function:: f.get_variable_list([groupname=None, group_walk=False, details=False])

   Returns a list of all variables at the root of the NetCDF file. If *groupname* is provided, the function will list all variables located at *groupname*. If group_walk is True, the function will list all variables in the NetCDF file from root, or from *groupname* if *groupname* is provided, to the last folder. If details is True, the function returns a list of dictionary containing the name of the variable and its path in the NetCDF file. By default, details is False and the function returns a simple list of variable names.
	
   :param groupname: the name of the group to get the variable list from ; optional
   :type groupname: string
   :param group_walk: if True, the function lists all variables from the root of the file, or from *groupname* if provided, to the last group ; optional
   :type group_walk: bool
   :param details: if True, the function returns a list of dictionary in which the key is the name of the variable, and the value is the path of the variable in the NetCDF file ; optional
   :type details: bool
   :rtype: list of variables
   
   >>> print(f.get_variable_list())
   >>> print(f.get_variable_list('test1/data'))
   >>> print(f.get_variable_list('test1/data', group_walk=True, details=True))

.. function:: f.get_group_list([groupname=None, details=False])

   Returns a list of groups found in the NetCDF file. If *groupname* is provided, the function returns all groups from *groupname* to the last group in *groupname*. The function returns a list of string if details is False. If details is True, it returns a list of dictionary in which the key is the name of the group and the value its path in the NetCDF file.
   
   :param groupname: name of a group where to get the group list ; optional
   :type groupname: string
   :param details: if True, the function returns a list of dictionary in which the key is the name of the group and the value its path in the NetCDF file ; optional
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

   If using the :class:`~.NetCdf` class, an array of values contained in *varname* will be returned. If using the :class:`~.EgadsNetCdf` class, an instance of the :class:`~.EgadsData` class will be returned containing the values and attributes of *varname*. If a group path is present in *varname*, then the function reads the variable *varname* in that specified group.

   :param varname: name of a variable, with or without group path, in the NetCDF file
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

.. function:: f.add_dim(name, size)

   Add a dimension to the NetCDF file. If a path to a group plus the dimension name is included in *name*, the dimension is
            added to the group. In that case, the group has to be created before.

   :param name: the name of the dimension
   :type name: string
   :param size: the size of the dimension
   :type size: int
   
   >>> f.add_dim('time', len(time))
   >>> f.add_dim('time', len(time), 'test1/data')
   >>> f.add_dim('time', len(time), ['test1', 'data'])

.. function:: f.add_attribute(attrname, value[, varname=None])

   Add an attribute to the NetCDF file. If *varname* is None, the attribute is a global attribute, and if not, the attribute is a variable attribute attached to *varname*. If the path of a group is present in *varname*, the attribute is attached to the variable stored in the specified group. If *varname* is simply the path of a group, attribute is attached to the group.

   :param attrname: the name of the attribute
   :type attrname: string
   :param value: the value of the attribute
   :type value: string|float|int
   :param varname: the name of the variable | group to which to attach the attribute ; optional
   :type varname: string
   
   >>> f.add_attribute('project', 'my project')
   >>> f.add_attribute('project', 'my project', 'temperature')
   >>> f.add_attribute('project', 'my project', 'test1/data/temperature')
   >>> f.add_attribute('project', 'my project', 'test1/data')
   
If using :class:`~.EgadsNetCdf`, data can be output to variables using the ``write_variable()`` function as follows:

    >>> f.write_variable(data, varname, dims, ftype, fillvalue)

.. function:: f.write_variable(data, varname[, dims=None, ftype='double', fillvalue=None])
   
   Write the values contained in *data* in the variable *varname* in a NetCDF file. If *varname* contains a path to a group, the variable will be created in the specified group, but in that case the group has to be created before. An instance of :class:`~.EgadsData` must be passed into ``write_variable``. Any attributes that are contained within the :class:`~.EgadsData` instance are applied to the NetCDF variable as well. If an attribute with a name equal to ``_FillValue`` or ``missing_value`` is found, NaN in data will be automatically replaced by the missing value. If attributes with the name ``scale_factor`` and/or ``add_offset`` are found, those attributes are automatically applied to the data.

   :param data: values to be stored in the NetCDF file
   :type data: EgadsData|array|vector|scalar
   :param varname: the name of the variable, or the path of group + the name of the variable, in the NetCDF file
   :type varname: string
   :param dims: a tuple of dimension names for data (not needed if the variable already exists) ; optional
   :type dims: tuple
   :param ftype: the data type of the variable, the default value is *double*, other valid options are *float*, *int*, *short*, *char* and *byte* ; optional
   :type ftype: string
   :param fillvalue: if it is provided, it overrides the default NetCDF _FillValue ; optional, it doesn't exist if using :class:`~.EgadsNetCdf`
   :type fillvalue: float|int
   
   >>> f.write_variable(data, 'particle_size', ('time', ))
   >>> f.write_variable(data, 'test1/data/particle_size', ('time', ))


If using :class:`~.NetCdf`, data can be output to variables using the ``write_variable()`` function as follows:

    >>> f.write_variable(data, varname, dims, ftype, fillvalue, scale_factor, add_offset)

.. function:: f.write_variable(data, varname[, dims=None, ftype='double', fillvalue=None, scale_factor=None, add_offset=None])
   
   Write the values contained in *data* in the variable *varname* in a NetCDF file. If *varname* contains a path to a group, the variable will be created in the specified group, but in that case the group has to be created before. Values for *data* passed into ``write_variable`` must be scalar or array.

   :param data: values to be stored in the NetCDF file
   :type data: EgadsData|array|vector|scalar
   :param varname: the name of the variable, or the path of group + the name of the variable, in the NetCDF file
   :type varname: string
   :param dims: a tuple of dimension names for data (not needed if the variable already exists) ; optional
   :type dims: tuple
   :param ftype: the data type of the variable, the default value is *double*, other valid options are *float*, *int*, *short*, *char* and *byte* ; optional
   :type ftype: string
   :param fillvalue: if it is provided, it overrides the default NetCDF _FillValue ; optional, it doesn't exist if using :class:`~.EgadsNetCdf`
   :type fillvalue: float|int
   :param scale_factor: if data must be scaled, use this parameter ; optional
   :type scale_factor: float|int
   :param add_offset: if an offset must be added to data, use this parameter ; optional
   :type add_offset: float|int
   
   >>> f.write_variable(data, 'particle_size', ('time', ))
   >>> f.write_variable(data, 'test1/data/particle_size', ('time', ), scale_factor=1.256, add_offset=5.56)


Conversion from NetCDF to NASA Ames file format
------------------------------------------------

The conversion is only possible on opened NetCDF files and with variables at the root of the NetCDF file. If modifications have been made and haven't been saved, the conversion won't take into account those modifications. Actually, the only File Format Index supported by the conversion is 1001. Consequently, if more than one independant variables are present in the NetCDF file, the file won't be converted and the function will raise an exception. If the user needs to convert a complex file with variables depending on multiple independant variables, and with the presence of groups, the conversion should be done manually by creating a NasaAmes instance and a NasaAmes dictionary, by populating the dictionary and by saving the file.

To convert a NetCDF file to NasaAmes file format, simply use:

.. function:: f.convert_to_nasa_ames([na_file=None, float_format=None, delimiter='    ', no_header=False])
   
   Convert the opened NetCDF file to NasaAmes file.

   :param na_file: it is the name of the output file once it has been converted, by default, *na_file* is None, and the name of the NetCDF file will be used with the extension .na ; optional
   :type na_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param delimiter: it is a character or a sequence of character to use between data items in the data file ; optional (by default '    ', 4 spaces)
   :type delimiter: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool
   
   >>> f.convert_to_nasa_ames(na_file='nc_converted_to_na.na', float_format='%.8f', delimiter=';', no_header=False)

To convert a NetCDF file to NasaAmes CSV file format, simply use:

.. function:: f.convert_to_csv([csv_file=None, float_format=None, no_header=False])
   
   Convert the opened NetCDF file to NasaAmes CSV file.

   :param csv_file: it is the name of the output file once it has been converted, by default, *na_file* is None, and the name of the NetCDF file will be used with the extension .csv ; optional
   :type csv_file: string
   :param float_format: it is the formatting string used for formatting floats when writing to output file ; optional
   :type float_format: string
   :param no_header: if it is set to ``True``, then only the data blocks are written to file ; optional
   :type no_header: bool


Conversion from NetCDF to Hdf5 file format
-------------------------------------------

EGADS Lineage offers a direct possibility to convert a full NetCDF file to Hdf file format. In the case of complexe NetCdf files, a manual Hdf file creation and editing is still possible.

.. function:: f.convert_to_hdf([filename=None])

	Converts the opened NetCdf file to Hdf format following the EUFAR and EGADS convention. If groups exist, they are preserved in the new Hdf file.
	
	:param filename: if only a name is given, a Hdf file named ``filename`` is created in the NetCdf file folder ; if a path and a name are given, a Hdf file named ``name`` is created in the folder ``path`` ; optional
	:type filename: string


Other operations
-----------------

.. function:: f.get_attribute_value(attrname[, varname=None])
   
   Return the value of the global attribute *attrname*, or the value of the variable attribute *attrname* if *varname* is not None. If *varname* contains a path to a group + a variable name, the function returns the attribute value attached to the variable in the specified group. If *varname* is simple path of group, the functions returns the attribute value attached to the group.

   :param attrname: the name of the attribute
   :type attrname: string
   :param varname: the name of the variable | group to which the attribute is attached
   :type varname: string
   :rtype: value of the attribute
   
   >>> print(f.get_attribute_value('project'))
   >>> print(f.get_attribute_value('long_name', 'temperature'))
   >>> print(f.get_attribute_value('long_name', 'test1/data/temperature'))
   >>> print(f.get_attribute_value('project', 'test1/data'))

.. function:: f.change_variable_name(varname, newname)
   
   Change a variable name in the currently opened NetCDF file. If *varname* contains a path to a group + a variable name, the variable name in the specified group is changed.

   :param attrname: the actual name of the variable
   :type attrname: string
   :param varname: the new name of the variable
   :type varname: string
   
   >>> f.change_variable_name('particle_nbr', 'particle_number')
   >>> f.change_variable_name('test1/data/particle_nbr', 'particle_number')

.. function:: f.add_group(groupname)

   Create a group in the NetCDF file. *groupname* can be a path + a group name or a sequence of group, in both cases, intermediary groups are created if needed.
   
   :param groupname: a group name or a list of group name
   :type groupname: string|list
   
   >>> f.add_group('MSL/north_atlantic/data')
   >>> f.add_group(['MSL', 'north_atlantic', 'data'])

Closing
---------

To close a file, simply use the ``close()`` method:

    >>> f.close()

.. NOTE::
  The EGADS :class:`~.NetCdf` and :class:`~.EgadsNetCdf` use the official NetCDF I/O routines, therefore, as described in the NetCDF documentation, it is not possible to remove a variable or more, and to modify the values of a variable. As attributes, global and those linked to a variable, are more dynamic, it is possible to remove, rename, or replace them.


Tutorial
---------

Here is a NetCDF file, created by EGADS, and viewed by the command ``ncdump -h ....``:
    
.. literalinclude:: example_files/ncdump_nc_example_file.txt

This file has been created with the following commands:

* import EGADS module:

    >>> import egads
    
* create two main variables, following the official EGADS convention:

    >>> data1 = egads.EgadsData(value=[5.0,2.0,-2.0,0.5,4.0], units='mm', standard_name='sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    >>> data2 = egads.EgadsData(value=[1.0,3.0,-1.0,2.5,6.0], units='mm', standard_name='corr sea level', scale_factor=1., add_offset=0., _FillValue=-9999)
    
* create an independant variable, still by following the official EGADS convention:

    >>> time = egads.EgadsData(value=[1.0,2.0,3.0,4.0,5.0], units='seconds since 19700101T00:00:00', standard_name='time')
    
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

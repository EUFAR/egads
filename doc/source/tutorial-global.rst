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
   >>> print(x.units)
   m
   >>> print(x.metadata)
   {'units': 'm', 'long_name': 'Test Variable'}
   
The :class:`~.EgadsData` is a subclass of the Quantities and Numpy packages. Thus it allows different kind of operations like addition, substraction, slicing, and many more. For each of those operations, a new :class:`~.EgadsData` class is created with all their attributes. 

.. NOTE::
  With mathematical operands, as metadata define an :class:`~.EgadsData` before an operation, and may not reflect the new :class:`~.EgadsData`, it has been decided to not keep the metadata attribute. It's the responsability of the user to add a new :class:`~.VariableMetadata` instance or a dictionary to the new :class:`~.EgadsData` object. It is not true if a user wants to slice an :class:`~.EgadsData`. In that case, metadata are automatically attributed to the new :class:`~.EgadsData`.


Metadata
---------

The metadata object used by :class:`~.EgadsData` is an instance of :class:`~.VariableMetadata`, a dictionary object containing methods to recognize, convert and validate known metadata types. It can reference parent metadata objects, such as those from an algorithm or data file, to enable users to track the source of a particular variable. 

When reading in data from a supported file type (NetCDF, NASA Ames, Hdf), or doing calculations with an EGADS algorithm, EGADS will automatically populate the associated metadata and assign it to the output variable. However, when creating an :class:`~.EgadsData` instance manually, the metadata must be user-defined.

As mentioned, :class:`~.VariableMetadata` is a dictionary object, thus all metadata are stored as keyword:value pairs. To create metadata manually, simply pass in a dictionary object containing the desired metadata:

   >>> var_metadata_dict = {'long_name':'test metadata object', '_FillValue':-9999}
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
   >>> print(a_km)
   ['EgadsData', array([0.001, 0.002, 0.003]), 'km']
   >>> a_grams = a.rescale('g')
   ValueError: Unable to convert between units of "m" and "g"

Likewise, arithmetic operations between :class:`~.EgadsData` instances are handled using the unit comprehension provided by Quantities. For example adding units of a similar type is permitted:

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
	
.. include:: tutorial-raw.inc
.. include:: tutorial-csv.inc
.. include:: tutorial-netcdf.inc
.. include:: tutorial-hdf.inc
.. include:: tutorial-nasaames.inc
.. include:: tutorial-end.inc

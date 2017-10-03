=============
Installation
=============
The latest version of EGADS can be obtained from https://github.com/eufarn7sp/egads


Prerequisites
*************
Use of EGADS requires the following packages:

* Python 2.7.10 or newer. Available at https://www.python.org/
* numpy 1.10.1 or newer. Available at http://numpy.scipy.org/
* scipy 0.15.0 or newer. Available at http://www.scipy.org/
* Python netCDF4 libraries 1.1.9 or newer. Available at https://pypi.python.org/pypi/netCDF4
* python_dateutil 2.4.2 or newer. Available at https://pypi.python.org/pypi/python-dateutil


Optional Packages
*****************
The following are useful when using or compiling EGADS:

* IPython - An optional package which simplifies Python command line usage (http://ipython.scipy.org). IPython is an enhanced interactive Python shell which supports tab-completion, debugging, command history, etc. 
* setuptools - An optional package which allows easier installation of Python packages (http://pypi.python.org/pypi/setuptools). It gives access to the ``easy_install`` command which allows packages to be downloaded and installed in one step from the command line.


Installation
************
Since EGADS is a pure Python distribution, it does not need to be built. However, to use it, it must be installed to a location on the Python path. To install EGADS, first download and decompress the file. From the directory containing the file ``setup.py``, type ``python setup.py install`` or ``pip install egads`` from the command line. To install to a user-specified location, type ``python setup.py install --prefix=$MYDIR``. To avoid the installation of dependencies, use the option ``--no-depts``. On Linux systems, the installation of EGADS in the user home directory is encouraged to ensure the proper operation of the EGADS logging system and of the new Graphical User Interface algorithm creation system.


Testing
*******
To test EGADS after it is installed, run the run_tests.py Python script, or from Python, run the following commands:

   >>> import egads
   >>> egads.test()


Log
***
A logging system has been introduced in EGADS since the version 0.7.0. By default, the output file is available in the 'Python local site-packages/EGADS x.x.x/egads' directory and the logging level has been set to INFO. Both options for logging level and logging location have been set in a config file. Both options can be changed through EGADS using the ``egads.set_log_options()`` function, by passing a dictionary of option keys and values:

   >>> import egads
   >>> config_dict = {'level': 'INFO', 'path': '/path/to/log/directory/'}
   >>> egads.set_log_options(config_dict)
   >>> exit()

Actual options to control the logging system are for now:

* ``level``: the logging level (``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR``).
* ``path``: the path of the file containing all logs.
   
New logging options will be loaded at the next import of EGADS. Logging levels are the standard Python ones (``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR``). It is also possible to change dynamically the logging level in a script:

   >>> egads.change_log_level('DEBUG')

That possibility is not permanent and will last until the script run is over.

=============
Installation
=============
The latest version of EGADS can be obtained from https://github.com/EUFAR/egads


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


Options
*******
Since version 0.7.0, an .ini file has been added to EGADS to welcome few options: log level and path, automatic check for a new EGADS version on GitHub. If the file is not present in EGADS directory, when importing, EGADS will create it automatically with default options. It is possible to display the status of the configuration file:

   >>> import egads
   >>> egads.print_options()
   The logging level is set on DEBUG and the log file is available in default directory.
   The option to check automatically for an update is set on False.

Actually, the number of option is limited and will probably incrase in the future. Here is a list of the options:

* ``level`` in ``LOG`` section: one of the items in the following list ``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR`` ; it is used to set the logging level when EGADS is imported.
* ``path`` in ``LOG`` section: a string corresponding to an OS path ; it is used to set the directory path where the log file is saved.
* ``check_update`` in ``OPTIONS`` section: True or False ; it is used to let EGADS check for an update automatically when it is imported.


Log
***
A logging system has been introduced in EGADS since the version 0.7.0. By default, the output file is available in the 'Python local site-packages/EGADS x.x.x/egads' directory and the logging level has been set to INFO. Both options for logging level and logging location have been set in a config file. Both options can be changed through EGADS using the ``egads.set_log_options()`` function, by passing a dictionary of option keys and values:

   >>> import egads
   >>> egads.set_log_options(log_level='INFO', log_path='/path/to/log/directory/')
   >>> exit()

Actual options to control the logging system are for now:

* ``level``: the logging level (``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR``).
* ``path``: the path of the file containing all logs.

New logging options will be loaded at the next import of EGADS. Logging levels are the standard Python ones (``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR``). It is also possible to change dynamically the logging level in a script:

   >>> egads.change_log_level('DEBUG')

That possibility is not permanent and will last until the script run is over.


Update
******
Since version 0.8.6, EGADS can check for an update on GitHub. The check system is launched in a separate thread and can be used this way:

   >>> import egads
   >>> egads.check_update()
   EGADS vx.x.x is available on GitHub. You can update EGADS by using pip (pip install egads --upgrade)
   or by using the following link: https://github.com/eufarn7sp/egads/releases/download/x.x.x/egads-x.
   x.x.tar.gz

If the ``check_update`` option is set on True in the egads.ini file, EGADS will check automatically for an update each time it is imported. The user can modify the option this way:

   >>> import egads
   >>> egads.set_update_check_option(True)
   >>> exit()

The use of pip or easy_install is still required to update EGADS package.

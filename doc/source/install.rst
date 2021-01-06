=============
Installation
=============
The latest version of EGADS Lineage can be obtained from GitHub (https://github.com/EUFAR/egads/tree/Lineage) or from PyPi (https://pypi.org/project/egads-lineage/)


Prerequisites
*************
Use of EGADS requires the following packages:

* Python 3.5.4 or newer. Available at https://www.python.org/
* numpy 1.14 or newer. Available at http://numpy.scipy.org/
* scipy 1.0 or newer. Available at http://www.scipy.org/
* Python netCDF4 libraries 1.3.0 or newer. Available at https://pypi.python.org/pypi/netCDF4
* h5py 2.10.0 or newer. Available at https://pypi.org/project/h5py
* python_dateutil 2.6.1 or newer. Available at https://pypi.python.org/pypi/python-dateutil
* quantities 0.12.1 or newer. Available at https://pypi.org/project/quantities
* requests 2.18.4 or newer. Optional, only for update checking. Available at https://pypi.org/project/requests/


Installation
************
Since EGADS is a pure Python distribution, it does not need to be built. However, to use it, it must be installed to a location on the Python path. To install EGADS, first download and decompress the file. From the directory containing the file ``setup.py``, type ``python setup.py install`` or ``pip install egads-lineage`` from the command line. To install to a user-specified location, type ``python setup.py install --prefix=$MYDIR``. To avoid the installation of dependencies, use the option ``--no-depts``.


Testing
*******
To test EGADS after it is installed, from Python terminal, run the following commands:

   >>> import egads
   >>> egads.test()

On Linux, if issues occure with NetCDF4 or H5py, please check the last section of this chapter for a possible solution.


Options
*******
Since version 0.7.0, an .ini file has been added to EGADS to welcome few options: log level and path, automatic check for a new EGADS version on GitHub. If the file is not present in EGADS directory, when importing, EGADS will create it automatically with default options. It is possible to display the status of the configuration file:

   >>> import egads
   >>> egads.print_options()
   EGADS options:
       - logging level: DEBUG
       - log path: PATH_TO_PYTHON\Python35\lib\site-packages\egads
       - update automatic check: False

Actually, the number of option is limited and will probably incrase in the future. Here is a list of all options:

* ``level`` in ``LOG`` section: one of the items in the following list ``DEBUG``, ``INFO``, ``WARNING``, ``CRITICAL``, ``ERROR`` ; it is used to set the logging level when EGADS is imported.
* ``path`` in ``LOG`` section: a string corresponding to an OS path ; it is used to set the directory path where the log file is saved.
* ``check_update`` in ``OPTIONS`` section: True or False ; it is used to let EGADS check for an update automatically when it is imported.

The file containing all options is now stored in the folder ``.egads_lineage`` in the user $HOME directory.


Log
***
A logging system has been introduced in EGADS since the version 0.7.0. By default, the output file is available in the ``.egads_lineage`` directory and the logging level has been set to INFO. Both options for logging level and logging location have been set in a config file. Both options can be changed through EGADS using the ``egads.set_log_options()`` function, by passing a dictionary of option keys and values:

   >>> import egads
   >>> egads.set_options(log_level='INFO', log_path='/path/to/log/directory/')
   >>> egads.set_options(log_level='INFO')
   >>> egads.set_options(log_path='/path/to/log/directory/')
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
   EGADS Lineage vx.x.x is available on GitHub. You can update EGADS Lineage by using pip (``pip install egads-lineage --upgrade``)
   or by using the following link: https://github.com/eufarn7sp/egads/releases/download/x.x.x/egads-x.x.x.tar.gz

If the ``check_update`` option is set on True in the egads.ini file, EGADS will check automatically for an update each time it is imported. By default, the option is set on False. The user can modify the option this way:

   >>> import egads
   >>> egads.set_options(check_update=True)
   >>> exit()

The module Requests is optional for EGADS but is mandatory to check for an update.


Uninstallation
**************
Just run the following command from your terminal:

   >>> pip uninstall egads-lineage

or
  remove manually all folders in your Python site-packages folder containing egads name.

In the $HOME directory, delete .egads_lineage directory if you don't want to keep options and logs of EGADS Lineage.


Issues with NetCDF4 and/or H5py on a Linux distribution
*******************************************************
If NetCDF4 and H5py libraries are installed through Pypi, a crash can occure when trying to read/write a netcdf or an hdf file. Here are the different steps to fix that particular issue:

#. Uninstall entirely NetCDF4
#. Download NetCDF4 sources corresponding to the version installed with Pypi
#. Unzip the package, launch a terminal and build NetCDF4 module -> ``python setup.py build``
#. Finally install NetCDF4 module -> ``python setup.py install``
#. Check NetCDF4 integration into EGADS with EGADS test function

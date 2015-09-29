
=============
Installation
=============
The latest version of EGADS can be obtained from http://eufar-egads.googlecode.com

Prerequisites
**************
Use of EGADS requires the following packages:

* Python 2.6 or newer. Available at http://www.python.org/
* numpy 1.3.0 or newer. Available at http://numpy.scipy.org/
* scipy 0.6.0 or newer. Available at http://www.scipy.org/
* Python netCDF4 libraries 0.8.2. Available at http://code.google.com/p/netcdf4-python/
* NAPpy 0.9.9 or newer. Available at http://proj.badc.rl.ac.uk/ndg/wiki/nappy

Optional Packages
*****************

The following are useful when using or compiling EGADS:

* IPython - An optional package which simplifies Python command line usage (http://ipython.scipy.org). IPython is an enhanced interactive Python shell which supports tab-completion, debugging, command history, etc. 
* setuptools - An optional package which allows easier installation of Python packages (http://pypi.python.org/pypi/setuptools). It gives access to the ``easy_install`` command which allows packages to be downloaded and installed in one step from the command line. 

Installation
************
Since EGADS is a pure Python distribution, it does not need to be built. However, to use it, it must 
be installed to a location on the Python path. To install EGADS, first download and decompress the file. From the directory
containing the file ``setup.py``, type ``python setup.py install`` 
from the command line. To install to a user-specified location, type ``python setup.py install --prefix=$MYDIR``.

Another option to install EGADS is using the ``easy_install`` command, which is included in the 
setuptools Python package. The advantage of easy_install is that it downloads and installs Python packages 
automatically from the online repository. To install EGADS using this method, simply type:

   => easy_install -U egads

from the command line. For more information on easy_install, type ``easy_install --help``.


Testing
********
To test EGADS after it is installed, run the run_tests.py Python script, or from Pythno, run the following commands:

   >>> import egads
   >>> egads.test()

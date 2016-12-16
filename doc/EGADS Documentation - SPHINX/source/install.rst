=============
Installation
=============
The latest version of EGADS can be obtained from https://github.com/eufarn7sp/egads


Prerequisites
*************
Use of EGADS requires the following packages:

* Python 2.7.10 or newer. Available at http://www.python.org/
* numpy 1.10.1 or newer. Available at http://numpy.scipy.org/
* scipy 0.15.0 or newer. Available at http://www.scipy.org/
* Python netCDF4 libraries 1.1.9. Available at https://pypi.python.org/pypi/netCDF4


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


Testing
********
To test EGADS after it is installed, run the run_tests.py Python script, or from Pythno, run the following commands:

   >>> import egads
   >>> egads.test()

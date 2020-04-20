Working with algorithms
************************

Algorithms in EGADS are stored in the :mod:`egads.algorithms` module for embedded algorithms and in :mod:`egads.user_algorithms` module for user-defined algorithms. They are separated into sub-modules by category (microphysics, thermodynamics, radiation, etc). Each algorithm follows a standard naming scheme, using the algorithm's purpose and source:

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
	 |  VERSION     Revision: 1.02
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

If an algorithm has been created by a user and is not embedded by default in EGADS, it should be called like this:

    >>> V_p = egads.user_algorithms.thermodynamics.VelocityTasCnrm().run(T_s, P_s, dP, 
        cpa, Racpa)

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
	    x += i
	    print i
	print x

.. raw:: latex

    \newpage
	
Using the GUI
**************

Since September 2016, a Graphical User Interface is available at https://github.com/eufarn7sp/egads-gui. It gives the user the possibility to explore data, apply/create algorithms, display and plot data. 

.. image:: images/EGADS_GUI_005.png
   :width: 936px
   :height: 647px
   :scale: 45 %
   :align: center

EGADS GUI can be launched as a simple python script from the terminal, if EGADS is installed, and once in the EGADS GUI directory:

    >>> python egads_gui.py

Since version 1.0.0, a stand-alone package is available for those who wants to use the GUI without a Python installation. In that case, look for ``EGADS Lineage GUI STA`` in the release part of the repository. For Windows (from Windows 7 32), donwload the .msi package and launch the installation, it should be installed outside ProgramFiles to avoid issues with admin rights, then the GUI can be run by double clicking on egads_gui.exe or from the shortcut in the Startup menu. A .zip package is also available for those who don't want to install it. For Linux (from Linux 4.15), download the tar.gz package somewhere on your hard drive (preferably in your home directory), extract it and run egads_gui.
The stand-alone versions for Linux and Windows have been created with PyInstaller, Windows 7 and Ubuntu 18.04.

.. NOTE::
  As for EGADS, the Graphical User Interface is available from two branches: master and Lineage (https://github.com/EUFAR/egads-gui/tree/Lineage). The Lineage one is only compatible with Python 3 and the earlier versions of EGADS Lineage.

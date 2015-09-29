

========
Algorithm Development
========

Introduction
*******************

The EGADS framework is designed to facilitate integration of third-party algorithms. This is accomplished
through creation of Python modules containing the algorithm code, and corresponding LaTeX files which 
contain the algorithm methodology documentation. This section will explain the elements
necessary to create these files, and how to incorporate them into the broader package.

Python module creation
************************

To guide creation of Python modules containing algorithms in EGADS, an algorithm template has been included
in the distribution. It can be found in ./egads/algorithms/algorithm_template.py and is shown below:

.. literalinclude:: algorithm_template.py

The best practice before starting an algorithm is to copy this file and name it following the EGADS algorithm
file naming conventions, which is all lowercase with words separated by underscores. As an example, the file
name for an algorithm calculating the wet bulb temperature contributed by DLR would be called
'temperature_wet_bulb_dlr.py'.

Within the file itself, there are several elements in this template that will need to be modified before this
can be usable as an EGADS algorithm:

1. Class name
   The class name is currently 'AlgorithmTemplate', but this must be changed to the actual name of the
   algorithm. The conventions here are the same name as the filename (see above), but using MixedCase. So,
   following the example above, the class name would be TemperatureWetBulbDlr

2. Algorithm docstring
   The docstring is everything following the three quote marks just after the class definition. This 
   section describes several essential aspects of the algorithm for easy reference directly from Python. 
   Each field following the word in ALLCAPS should be changed to reflect the properties of the algorithm
   (with the exception of VERSION, which will be changed automatically by Subversion when the file is 
   committed to the server).

3. Algorithm and output metadata
   In the __init__ method of the module, two important parameters are defined. The first is the
   'output_metadata', which defines the metadata elements that will be assigned to the variable 
   output by the algorithm. A few recommended elements are included, but a broader list of variable
   metadata parameters can be found in the NetCDF standards document on the N6SP wiki (www.eufar.net/n6sp).
   In the case that there are multiple parameters output by the algorithm, the output_metadata parameter
   can be defined as a list VariableMetadata instances.
   
   Next, the 'metadata' parameter defines metadata concerning the algorithm itself. These information
   include the names of inputs and their units; names of outputs; name, date and version of the
   algorithm; date processed; and a reference to the output parameters. Of these parameters, only the names
   and units of the inputs and names of the outputs need to be altered. The other parameters (name,
   date and version of the processor; date processed) are populated automatically.

   **Note** -- for algorithms in which the output units depend on the input units (i.e. a purely mathematical
   transform, derivative, etc), there is a specific methodology to tell EGADS how to set the output units.
   To do this, set the appropriate 'units' parameter of output_metadata to 'inputn' where *n* is the
   number of the input parameter from which to get units (starting at 0). The units on the input parameter 
   from which the output is to be derived should be set to 'None'.

4. Definition of parameters
   In both the run and _algorithm methods, the local names intended for inputs need to be included. There
   are three locations where the same list must be added (marked in bold):
   
   * def run(self, **inputs**)
   * return egads_core.EgadsAlgorithm.run(self, **inputs**)
   * def _algorithm(self, **inputs**)
   
5. Implementation of algorithm
   The algorithm itself gets written in the _algorithm method and uses variables passed in by the user.
   The variables which arrive here are simply scalar or arrays, and if the source is an instance of 
   EgadsData, the variables will be converted to the units you specified in the InputUnits of the 
   algorithm metadata. 


Documentation creation
***********************

Within the EGADS structure, each algorithm has accompanying documentation in the EGADS Algorithm Handbook.
These descriptions are contained in LaTeX files, organized in a structure similar to the toolbox itself,
with one algorithm per file. These files can be found in the SVN/doc directory on the SVN server 
(http://eufar-egads.googlecode.com).

A template is provided to guide creation of the documentation files. This can be found at 
doc/algorithms/algorithm_template.tex. The template is divided into 8 sections, enclosed 
in curly braces. These sections are explained below:

* Algorithm name
   Simply the name of the Python file where the algorithm can be found.

* Algorithm summary
   This is a short description of what the algorithm is designed to calculate, and should contain
   any usage caveats, constraints or limitations.

* Category
   The name of the algorithm category (e.g. Thermodynamics, Microphysics, Radiation, Turbulence, etc).

* Inputs
   At the minimum, this section should contain a table containing the symbol, data type (vector
   or coefficient), full name and units of the input parameters. An example of the expected 
   table layout is given in the template.

* Outputs
   This section describes the parameters output from the algorithm, using the same fields as the 
   input table (symbol, data type, full name and units). An example of the expected table layout is
   given in the template.

* Formula
   The mathematical formula for the algorithm is given in this section, if possible, along with a
   description of the techniques employed by the algorithm.

* Author
   Any information about the algorithm author (e.g. name, institution, etc) should be given here.

* References
   The references section should contain citations to publications which describe the algorithm.

In addition to these sections, the ``index`` and ``algdesc`` fields at the top of the file 
need to be filled in. The value of the ``index`` field should be the same as the algorithm name.
The ``algdesc`` field should be the full English name of the algorithm. 

.. NOTE::
   * Any "_" character in plain text in LaTeX needs to be offset by a "\". Thus if the algorithm
     name is ``temp_static_cnrm``, in LaTex, it should be input as ``temp\_static\_cnrm``.


Example
--------------

An example algorithm is shown below with all fields completed.

.. literalinclude:: temp_static_cnrm.tex





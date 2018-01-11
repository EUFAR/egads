=====================
Algorithm Development
=====================

Introduction
*******************

The EGADS framework is designed to facilitate integration of third-party algorithms. This is accomplished through creation of Python modules containing the algorithm code, and corresponding LaTeX files which contain the algorithm methodology documentation. This section will explain the elements necessary to create these files, and how to incorporate them into the broader package.

Python module creation
************************

To guide creation of Python modules containing algorithms in EGADS, an algorithm template has been included in the distribution. It can be found in ./egads/algorithms/file_templates/algorithm_template.py and is shown below:

.. literalinclude:: example_files/algorithm_template.py

The best practice before starting an algorithm is to copy this file and name it following the EGADS algorithm file naming conventions, which is all lowercase with words separated by underscores. As an example, the file name for an algorithm calculating the wet bulb temperature contributed by DLR would be called
``temperature_wet_bulb_dlr.py``.

Within the file itself, there are one rule to respect and several elements in this template that will need to be modified before this can be usable as an EGADS algorithm.:

1. Format
    An algorithm file is composed of different elements: metadata, class name, algorithm docstring, ... It is critical to respect the format of each element of an algorithm file, in particular the first metadata and the docstring, in term of beginning white spaces, line length, ... Even if it is not mandatory for EGADS itself, it will facilitate the integration of those algorithms in the new Graphical User Interface. 

2. Class name
    The class name is currently 'AlgorithmTemplate', but this must be changed to the actual name of the algorithm. The conventions here are the same name as the filename (see above), but using MixedCase. So, following the example above, the class name would be TemperatureWetBulbDlr

3. Algorithm docstring
    The docstring is everything following the three quote marks just after the class definition. This section describes several essential aspects of the algorithm for easy reference directly from Python. This part is critical for the understanding of the algorithm by different users.

4. Algorithm and output metadata
    In the ``__init__`` method of the module, two important parameters are defined. The first is the 'output_metadata', which defines the metadata elements that will be assigned to the variable output by the algorithm. A few recommended elements are included, but a broader list of variable metadata parameters can be found in the NetCDF standards document on the EUFAR website (http://www.eufar.net/documents/6140, Annexe III). In the case that there are multiple parameters output by the algorithm, the output_metadata parameter can be defined as a list VariableMetadata instances.
   
    Next, the 'metadata' parameter defines metadata concerning the algorithm itself. These information include the names, types, descriptions and units of inputs; names and descriptions of outputs; name, description, purpose, category, source, reference, date and version of the algorithm; date processed; and a reference to the output parameters. Of these parameters, only the names, types, descriptions and units of the inputs, names and descriptions of the outputs and category, source, reference, description and purpose of the algorithm need to be altered. The other parameters (name, date and version of the processor, date processed) are populated automatically.

    self.output_metadata:
        * units: units of the output.
        * long_name: the name describing the output.
        * standard_name: a short name for the output.
        * Category: Name(s) of probe category - comma separated list (cf. EUFAR document http://www.eufar.net/documents/6140 for an example of possible categories).

    self.metadata:
        * Inputs: representation of each input in the documentation and in the code (ex: P_a for altitude pressure).
        * InputUnits: a list of all input units, one unit per input, '' for dimensionless input and 'None' for the input accepting every kind of units.
        * InputTypes: the type of the input (array, vector, coeff, ...) linked to the ``var_type`` string in the algorithm template ; the string ``_optional`` can be added to inform that the input is optional (used in the EGADS GUI).
        * InputDescription: short description of each input.
        * Outputs: representation of each output (ex: P_a for altitude pressure).
        * OutputUnits: units of each output (cf. self.output_metadata['units']).
        * OutputTypes: type of each output (ex: vector).
        * OutputDescription: short description of each output.
        * Purpose: the goal of the algorithm.
        * Description: a description of the algorithm.
        * Category: the category of the algorithm (ex: Transforms, Thermodynamis, ...).
        * Source : the source of the algorithm (ex: CNRM).
        * Reference : the reference of the algorithm (ex: Doe et al, My wonderful algorithm, Journal of Algorithms, 11, pp 21-22, 2017).
        * Processor: self.name.
        * ProcessorDate: ``__date__``.
        * ProcessorVersion: ``__version__``.
        * DateProcessed: self.now().
   
   
.. NOTE::
  For algorithms in which the output units depend on the input units (i.e. a purely mathematical transform, derivative, etc), there is a specific methodology to tell EGADS how to set the output units. To do this, set the appropriate ``units`` parameter of output_metadata to ``inputn`` where *n* is the number of the input parameter from which to get units (starting at 0). For algorithms in which the units of the input has no importance, the input units should set to ``None``. For algorithms in which the input units are dimensionless (a factor, a quantity, a coefficient), the units on the input parameter should be set to ``''``.
   
.. NOTE::
  EGADS accepts different kind of input type: coeff. for coefficient, vector, array, string, ... When writing the docstring of an algorithm and the metadata ``InputTypes``, the user should write the type carefully as it is interpreted by EGADS. If a type depends on another variable or multiple variables, for example the time, or geographic coordinates, the variable name should be written between brackets (ex: array[lon,lat]). If a variable is optional, the user should add ``, optional`` to the type in the doctstring, and ``_optional`` to the type in the metadata ``InputTypes``.

  
5. Definition of parameters
    In both the run and _algorithm methods, the local names intended for inputs need to be included. There are three locations where the same list must be added (marked in bold):
   
    * def run(self, **inputs**)
    * return egads_core.EgadsAlgorithm.run(self, **inputs**)
    * def _algorithm(self, **inputs**)
   
6. Implementation of algorithm
    The algorithm itself gets written in the _algorithm method and uses variables passed in by the user. The variables which arrive here are simply scalar or arrays, and if the source is an instance of EgadsData, the variables will be converted to the units you specified in the InputUnits of the algorithm metadata.
   
7. Integration of the algorithm in EGADS
    Once the algorithm file is ready, the user has to move it in the appropriate directory in the ``./egads/algorithms/user`` directory. Once it has been done, the ``__init__.py`` file has to be modified to declare the new algorithm. The following line can be added to the ``__init__.py`` file: ``from the_name_of_the_file import \*``.
    
    If the algorithm requires a new directory, the user has to create it in the ``user`` directory, move the file inside and create a ``__init__.py`` file to declare the new directory and the algoritm to EGADS. A template can be found in ``./egads/algorithms/user/file_templates/init_template.py`` and is shown below:
    
    .. literalinclude:: example_files/init_template.py


Documentation creation
***********************

Within the EGADS structure, each algorithm has accompanying documentation in the EGADS Algorithm Handbook. These descriptions are contained in LaTeX files, organized in a structure similar to the toolbox itself, with one algorithm per file. These files can be found in the Documentation/EGADS Algorithm Handbook directory in the EGADS package downloaded from GitHub repository: https://github.com/eufarn7sp/egads.

A template is provided to guide creation of the documentation files. This can be found at Documentation/EGADS Algorithm Handbook/algorithms/algorithm_template.tex. The template is divided into 8 sections, enclosed in curly braces. These sections are explained below:

* Algorithm name
   Simply the name of the Python file where the algorithm can be found.

* Algorithm summary
   This is a short description of what the algorithm is designed to calculate, and should contain any usage caveats, constraints or limitations.

* Category
   The name of the algorithm category (e.g. Thermodynamics, Microphysics, Radiation, Turbulence, etc).

* Inputs
   At the minimum, this section should contain a table containing the symbol, data type (vector or coefficient), full name and units of the input parameters. An example of the expected table layout is given in the template.

* Outputs
   This section describes the parameters output from the algorithm, using the same fields as the input table (symbol, data type, full name and units). An example of the expected table layout is given in the template.

* Formula
   The mathematical formula for the algorithm is given in this section, if possible, along with a description of the techniques employed by the algorithm.

* Author
   Any information about the algorithm author (e.g. name, institution, etc) should be given here.

* References
   The references section should contain citations to publications which describe the algorithm.

In addition to these sections, the ``index`` and ``algdesc`` fields at the top of the file need to be filled in. The value of the ``index`` field should be the same as the algorithm name. The ``algdesc`` field should be the full English name of the algorithm. 

.. NOTE::
    Any "_" character in plain text in LaTeX needs to be offset by a "\\". Thus if the algorithm name is ``temp_static_cnrm``, in LaTex, it should be input as ``temp\_static\_cnrm``.


Example
--------

An example algorithm is shown below with all fields completed.

.. literalinclude:: example_files/temp_static_cnrm.tex

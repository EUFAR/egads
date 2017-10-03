=============
Introduction
=============
The EGADS (EUFAR General Airborne Data-processing Software) core is a Python-based library of processing and file I/O routines designed to help analyze a wide range of airborne atmospheric science data. EGADS purpose is to provide a benchmark for airborne data-processing through its community-provided algorithms, and to act as a reference by providing guidance to researchers with an open-source design and well-documented processing routines.

Python is used in development of EGADS due to its straightforward syntax and portability between systems. Users interact with data processing algorithms using the Python command-line, by creating Python scripts for more complex tasks, or by using the EGADS GUI for a simplified interaction. The core of EGADS is built upon a data structure that encapsulates data and metadata into a single object. This simplifies the housekeeping of data and metadata and allows these data to be easily passed between algorithms and data files. Algorithms in EGADS also contain metadata elements that allow data and their sources to be tracked through processing chains.

.. NOTE::
  Even if EGADS is easily accessible, a certain knowledge in Python is still required to use EGADS.

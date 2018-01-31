#!/usr/bin/env python
"""EGADS: EUFAR General Airborne Data-processing Software

EGADS (EUFAR General Airborne Data-processing Software) is a Python-based
toolbox for processing airborne atmospheric data. EGADS provides a framework
for researchers to apply expert-contributed algorithms to data files, and acts
as a platform for data intercomparison. Algorithms used in EGADS were
contributed by members of the EUFAR Expert Working Groups and are mature and
well-established in the scientific community.
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = """\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Natural Language :: English
Programming Language :: Python
Topic :: Scientific/Engineering :: Atmospheric Science
"""

doclines = __doc__.split('\n')

setup(name='egads',
      version='0.8.9',
      description=doclines[0],
      long_description='\n'.join(doclines[2:]),
      author='EUFAR',
      author_email='bureau@eufar.net',
      maintainer='Olivier Henry',
      maintainer_email='olivier.henry@meteo.fr',
      url='http://www.eufar.net',
      download_url='http://www.eufar.net/software-tools/tool/eufar-general-airborne-data-processing-software-core-da-cedg-osr',
      license='New BSD License',
      keywords=['airbornescience', 'netcdf', 'nasa-ames', 'eufar', 'science',
                  'microphysics', 'thermodynamics'],
      platforms=['Windows', 'Linux', 'MacOS'],
      packages=['egads',
          'egads.core',
          'egads.algorithms',
		  'egads.algorithms.comparisons',
		  'egads.algorithms.corrections',
		  'egads.algorithms.mathematics',
          'egads.algorithms.microphysics',
          'egads.algorithms.radiation',
          'egads.algorithms.thermodynamics',
          'egads.algorithms.transforms',
          'egads.algorithms.user',
          'egads.algorithms.user.comparisons',
          'egads.algorithms.user.corrections',
          'egads.algorithms.user.mathematics',
          'egads.algorithms.user.microphysics',
          'egads.algorithms.user.radiation',
          'egads.algorithms.user.thermodynamics',
          'egads.algorithms.user.transforms',
          'egads.input',
          'egads.tests',
		  'egads.thirdparty.nappy',
		  'egads.thirdparty.nappy.config',
		  'egads.thirdparty.nappy.contrib',
		  'egads.thirdparty.nappy.na_error',
		  'egads.thirdparty.nappy.na_file',
		  'egads.thirdparty.nappy.nc_interface',
		  'egads.thirdparty.nappy.script',
		  'egads.thirdparty.nappy.utils',
          'egads.thirdparty.quantities',
		  'egads.thirdparty.quantities.constants',
		  'egads.thirdparty.quantities.tests',
		  'egads.thirdparty.quantities.units',
          'Documentation',
          'Documentation.EGADS Algorithm Handbook - LATEX',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.biophysics',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.corrections',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.mathematics',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.microphysics',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.quality_control',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.radiation',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.thermodynamics',
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.transforms',
          'Documentation.EGADS Algorithm Handbook - LATEX.cover',
          'doc',
          'doc.source',
          'doc.source.example_files',
          'doc.source.images',
          'doc.source._static'],
      package_data={
	  'egads.thirdparty.nappy': ['*.ini'],
          'egads.thirdparty.nappy.config':['*.ini'],
          'Documentation': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.biophysics': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.corrections': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.mathematics': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.microphysics': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.quality_control': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.radiation': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.thermodynamics': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.algorithms.transforms': ['*.*'],
          'Documentation.EGADS Algorithm Handbook - LATEX.cover': ['*.*'],
          'doc': ['*.*'],
          'doc.source': ['*.*'],
          'doc.source.example_files': ['*.*'],
          'doc.source.images': ['*.*'],
          'doc.source._static': ['*.*']
          },
      classifiers=filter(None, classifiers.split("\n")),
      requires=['numpy (>=1.10.1)', 'scipy (>=0.15.0)', 'netCDF4 (>=1.1.9)', 'python_dateutil (>=2.4.2)'],
      install_requires=['numpy >= 1.10.1', 'scipy >=0.15.0', 'netCDF4 >= 1.1.9', 'python_dateutil >= 2.4.2'],
      )

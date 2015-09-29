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
      version='0.5.8',
      description=doclines[0],
      long_description='\n'.join(doclines[2:]),
      author='EUFAR',
      author_email='bureau@eufar.net',
      maintainer='Matt Freer',
      maintainer_email='eufarsp@eufar.net',
      url='http://www.eufar.net',
      download_url='http://code.google.com/p/eufar-egads/',
      license='New BSD License',
      keywords=['airbornescience', 'netcdf', 'nasa-ames', 'eufar', 'science',
                  'microphysics', 'thermodynamics'],
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
                  'egads.input',
                  'egads.tests',
		  'egads.third-party.cdms_utils',
		  'egads.third-party.nappy',
		  'egads.third-party.nappy.config',
		  'egads.third-party.nappy.contrib',
		  'egads.third-party.nappy.na_error',
		  'egads.third-party.nappy.na_file',
		  'egads.third-party.nappy.nc_interface',
		  'egads.third-party.nappy.script',
		  'egads.third-party.nappy.utils',
		  'egads.third-party.pml_wq',
          'egads.third-party.pml_wq.iop_model',
          'egads.third-party.pml_wq.iop_model',
          'egads.third-party.pml_wq.iop_model.config',
          'egads.third-party.pml_wq.iop_model.data',
          'egads.third-party.pml_wq.test_data',
          'egads.third-party.quantities',
		  'egads.third-party.quantities.constants',
		  'egads.third-party.quantities.tests',
		  'egads.third-party.quantities.units'],
      package_data={
	      'egads.third-party.nappy': ['*.ini'],
          'egads.third-party.nappy.config':['*.ini']
	      },
      classifiers=filter(None, classifiers.split("\n")),
      requires=['numpy (>=1.3.0)', 'netCDF4 (>=0.8.2)', 'quantities (>=0.10.0)', 'python_dateutil (>=1.5)', 'cdat_lite'],
      install_requires=['numpy >= 1.3.0', 'netCDF4 >= 0.8.2' , 'quantities >= 0.10.0', 'python_dateutil >= 1.5', 'cdat_lite'],
      )


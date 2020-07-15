"""EGADS: EUFAR General Airborne Data-processing Software

EGADS (EUFAR General Airborne Data-processing Software) is a Python-based
toolbox for processing airborne atmospheric data. EGADS provides a framework
for researchers to apply expert-contributed algorithms to data files, and acts
as a platform for data intercomparison. Algorithms used in EGADS were
contributed by members of the EUFAR Expert Working Groups and are mature and
well-established in the scientific community. EGADS Lineage is a new branch in
EGADS development maintained outside the scope of EUFAR et compatible with Python 3.
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: GNU General Public License v3 (GPLv3)
Natural Language :: English
Programming Language :: Python
Topic :: Scientific/Engineering :: Atmospheric Science
"""

doclines = __doc__.split('\n')

setup(name='egads-lineage',
      version='1.2.7',
      description=doclines[0],
      long_description='\n'.join(doclines[2:]),
      author='EUFAR, Olivier Henry',
      author_email='olivier.pascal.henry@gmail.com',
      maintainer='Olivier Henry',
      maintainer_email='olivier.pascal.henry@gmail.com',
      url='https://github.com/EUFAR/egads/tree/Lineage',
      download_url='https://github.com/EUFAR/egads/tree/Lineage',
      license='GNU General Public License v3 (GPLv3)',
      keywords=['airbornescience', 'netcdf', 'nasa-ames', 'eufar', 'science', 'microphysics', 'thermodynamics'],
      platforms=['Windows', 'Linux', 'MacOS'],
      project_urls={'Documentation': 'https://egads.readthedocs.io/en/lineage/'},
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
                'egads.utils',
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
      package_data={'Documentation': ['*.*'],
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
                    'doc.source._static': ['*.*']},
      classifiers=filter(None, classifiers.split("\n")),
      requires=['numpy (>=1.14)', 'netCDF4 (>=1.3.0)', 'python_dateutil (>=2.6.1)', 'quantities (>=0.12.1)',
                'h5py (>=2.10.0)'],
      install_requires=['numpy >= 1.14', 'netCDF4 >= 1.3.0', 'python_dateutil >= 2.6.1', 'quantities >= 0.12.1',
                        'h5py >=2.10.0'],
      )

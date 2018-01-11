__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.2"
__all__ = ['PlanckEmission']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class PlanckEmission(egads_core.EgadsAlgorithm):
    
    """
    FILE        planck_emission.py

    VERSION     1.2

    CATEGORY    Radiation

    PURPOSE     Calculates the radiance of a surface at a given wavelength given its temperature.

    DESCRIPTION Calculates the radiance of a surface at a given wavelength given its temperature.

    INPUT       T        vector        K        temperature
                Lambda   coeff         nm       wavelength

    OUTPUT      rad      vector        W m-2 sr-1 nm-1    Black body radiance

    SOURCE      Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)
        
        self.output_metadata = egads_metadata.VariableMetadata({'units':'W m^-2 sr^-1 nm^-1',
                                                               'long_name':'radiance',
                                                               'standard_name':'',
                                                               'Category':['Radiation']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T', 'Lambda'],
                                                          'InputUnits':['K', 'nm'],
                                                          'InputTypes':['vector', 'coeff'],
                                                          'InputDescription':['Temperature', 'Wavelength'],
                                                          'Outputs':['rad'],
                                                          'OutputUnits':['W m^-2 sr^-1 nm^-1'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Black body radiance'],
                                                          'Purpose':'Calculates the radiance of a surface at a given wavelength given its temperature',
                                                          'Description':'No description',
                                                          'Category':'Radiation',
                                                          'Source':'Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, T, Lambda):
        return egads_core.EgadsAlgorithm.run(self, T, Lambda)

    def _algorithm(self, T, Lambda):
        h = 6.62606957e-34  # J s
        kb = 1.3806e-23
        c = 2.997925e8
        l = Lambda * 1e-9
        rad = 2 * h * c ** 2 / (l ** 5 * (numpy.exp(h * c / (kb * l * T)) - 1.0)) * 1e-9
        return rad


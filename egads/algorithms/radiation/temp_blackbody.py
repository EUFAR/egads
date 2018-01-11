__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.2"
__all__ = ['TempBlackbody']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class TempBlackbody(egads_core.EgadsAlgorithm):
    
    """
    FILE        temp_blackbody.py

    VERSION     1.2

    CATEGORY    Radiation

    PURPOSE     Calculates the blackbody temperature for a given radiance at a specific wavelength

    DESCRIPTION Calculates the blackbody temperature for a given radiance at a specific wavelength

    INPUT       rad        vector    W m-2 sr-1 nm-1     blackbody radiance
                Lambda     coeff     nm                  wavelength

    OUTPUT      T          vector    K                   temperature

    SOURCE      Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)

    REFERENCES
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'blackbody temperature',
                                                               'standard_name':'',
                                                               'Category':['Radiation']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['rad', 'lambda'],
                                                          'InputUnits':['W m^-2 sr^-1 nm^-1', 'nm'],
                                                          'InputTypes':['vector','coeff'],
                                                          'InputDescription':['Blackbody radiance','Wavelength'],
                                                          'Outputs':['T'],
                                                          'OutputUnits':['K'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Temperature'],
                                                          'Purpose':'Calculates the blackbody temperature for a given radiance at a specific wavelength',
                                                          'Description':'No description',
                                                          'Category':'Radiation',
                                                          'Source':'Andre Ehrlich, Leipzig Institute for Meteorology (a.ehrlich@uni-leipzig.de)',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, rad, Lambda):
        return egads_core.EgadsAlgorithm.run(self, rad, Lambda)

    def _algorithm(self, rad, Lambda):
        h = 6.62606957e-34  # J s
        kb = 1.3806e-23
        c = 2.997925e8
        l = Lambda * 1e-9
        rad = rad * 1e9
        T = h * c / (kb * l * numpy.log(2 * h * c ** 2 / (l ** 5 * rad) + 1))
        return T


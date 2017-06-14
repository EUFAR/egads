__author__ = "mfreer, ohenry"
__date__ = "2012-02-07 17:23"
__version__ = "125"
__all__ = ['DiameterEffectiveDmt']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class DiameterEffectiveDmt(egads_core.EgadsAlgorithm):

    """
    FILE        diameter_effective_dmt.py

    VERSION     125

    CATEGORY    Microphysics

    PURPOSE     Calculation of effective radius of a size distribution.

    DESCRIPTION This algorithm calculates the effective radius given a size distribution.
                In general, this definition is only meaningful for water clouds.

    INPUT       n_i    array[time, bins]    cm-3    number concentration of hydrometeors
                                                    in size category i
                d_i    vector[bins]         um      average diameter in size category i

    OUTPUT      D_e    vector[time]         um      effective diameter

    SOURCE      

    REFERENCES  "Data Analysis User's Guide, Chapter 1, Section 1.3.2.4", Droplet Measurement 
                Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/Manuals
                Guides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'um',
                                                               'long_name':'Effective Diameter',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i'],
                                                          'InputUnits':['cm^-3', 'um'],
                                                          'InputTypes':['array','vector'],
                                                          'InputDescription':['Number concentration of hydrometeors in size category i','Average diameter in size category i'],
                                                          'Outputs':['D_e'],
                                                          'OutputDescription':['Effective diameter'],
                                                          'Purpose':'Calculation of effective radius of a size distribution',
                                                          'Description':'This algorithm calculates the effective radius given a size distribution. In general, this definition is only meaningful for water clouds',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, n_i, d_i):
        return egads_core.EgadsAlgorithm.run(self, n_i, d_i)


    def _algorithm(self, n_i, d_i):
        sum_third_moment = numpy.sum(n_i * d_i ** 3, axis=1) # um^3/cm^3
        sum_second_moment = numpy.sum(n_i * d_i ** 2, axis=1) # um^2/cm^3
        
        """
        D_e = sum_third_moment / sum_second_moment
        original code, but a factor 3/4, present in DMT guide, is missing
        """
        
        D_e = (3. * sum_third_moment) / (4. * sum_second_moment) # um
        
        return D_e


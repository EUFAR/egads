__author__ = "mfreer, ohenry"
__date__ = "2017-01-26 13:07"
__version__ = "1.2"
__all__ = ['MassConcDmt']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class MassConcDmt(egads_core.EgadsAlgorithm):

    """
    FILE        mass_conc_dmt.py

    VERSION     1.2

    CATEGORY    Microphysics

    PURPOSE     Calculates mass concentration given a size distribution.

    DESCRIPTION Calculates mass concentration given a size distribution. Can be used
                to calculate liquid or ice water content depending on the types of hydrometeors
                being sampled.

    INPUT       c_i    array[time, bins]    cm-3    number concentration of hydrometeors
                                                    in size category i
                d_i    vector[bins]         um      average diameter of size category i
                s_i    array[time,bins]     _       shape factor of hydrometeor in size
                                                    category i to account for asphericity
                rho_i  vector[bins]         g/cm3   density of the hydrometeor in size category
                                                    i

    OUTPUT      M      vector[time]         g/cm3   mass concentration         

    SOURCE      

    REFERENCES  "Data Analysis User's Guide, Chapter 1, Section 1.3.2", Droplet Measurement 
                Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/Manuals
                Guides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'g/cm^3',
                                                               'long_name':'Mass concentration',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['c_i', 'd_i', 's_i', 'rho_i'],
                                                          'InputUnits':['cm^-3', 'um', '', 'g/cm^3'],
                                                          'InputTypes':['array[time, bins]','vector[bins]','array[time,bins]','vector[bins]'],
                                                          'InputDescription':['Number concentration of hydrometeors in size category i',
                                                                              'Average diameter of size category i',
                                                                              'Shape factor of hydrometeor in size category i to account for asphericity',
                                                                              'density of the hydrometeor in size category i'],
                                                          'Outputs':['M'],
                                                          'OutputUnits':['g/cm^3'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Mass concentration'],
                                                          'Purpose':'Calculates mass concentration given a size distribution',
                                                          'Description':'Calculates mass concentration given a size distribution. Can be used to calculate liquid or ice water content depending on the types of hydrometeors being sampled',
                                                          'Category':'Microphysics',
                                                          'Source':'',
                                                          'References':"Data Analysis User's Guide, Chapter 1, Section 1.3.2, Droplet Measurement Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/ManualsGuides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf",
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, c_i, d_i, s_i, rho_i):
        return egads_core.EgadsAlgorithm.run(self, c_i, d_i, s_i, rho_i)

    def _algorithm(self, c_i, d_i, s_i, rho_i):
        d_i = d_i * 1.0e-4
        if c_i.ndim <= 1:
            M = (numpy.pi / 6.0) * numpy.sum(s_i * rho_i * c_i * d_i ** 3)
        else:
            M = (numpy.pi / 6.0) * numpy.sum(s_i * rho_i * c_i * d_i ** 3, axis=1)
        return M


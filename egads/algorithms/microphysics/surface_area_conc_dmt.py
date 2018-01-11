__author__ = "mfreer, ohenry"
__date__ = "2016-01-10 11:58"
__version__ = "1.1"
__all__ = ['SurfaceAreaConcDmt']

import numpy
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class SurfaceAreaConcDmt(egads_core.EgadsAlgorithm):

    """
    FILE        surface_area_conc_dmt.py

    VERSION     1.1

    CATEGORY    Microphysics

    PURPOSE     Calculates surface area concentration given size distribution from 
                particle probe.

    DESCRIPTION Calculates surface area concentration (2nd moment) given size distribution 
                from particle probe.

    INPUT       n_i    array[time,bins]    cm-3    number concentration of hydrometeors
                                                   in size category i
                d_i    vector[bins]        um      average diameter of size category i
                s_i    array[time,bins]    _       shape factor of hydrometeor in size category
                                                   i to account for asphericity

    OUTPUT      S      vector[time]        um2 cm3 Surface area concentration

    SOURCE      

    REFERENCES  "Data Analysis User's Guide, Chapter 1, Section 1.3.2", Droplet Measurement 
                Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/Manuals
                Guides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'um^2/cm^3',
                                                               'long_name':'surface area concentration',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i', 's_i'],
                                                          'InputUnits':['cm^-3', 'um', ''],
                                                          'InputTypes':['array', 'vector', 'array'],
                                                          'InputDescription':['number concentration of hydrometeors in size category i',
                                                                              'average diameter of size category i',
                                                                              'shape factor of hydrometeor in size category i to account for asphericity'],
                                                          'Outputs':['S'],
                                                          'OutputUnits':['um^2/cm^3'],
                                                          'OutputTypes':['vector[time]'],
                                                          'OutputDescription':['Surface area concentration'],
                                                          'Purpose':'Calculates surface area concentration given size distribution from particle probe',
                                                          'Description':'Calculates surface area concentration (2nd moment) given size distribution from particle probe',
                                                          'Category':'Microphysics',
                                                          'Source':'',
                                                          'References':"Data Analysis User's Guide, Chapter 1, Section 1.3.2, Droplet Measurement Technologies, 2009, http://www.dropletmeasurement.com/sites/default/files/ManualsGuides/Data%20Analysis%20Guide/DOC-0222%20Rev%20A%20Data%20Analysis%20Guide%20Ch%201.pdf",
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, n_i, d_i, s_i):
        return egads_core.EgadsAlgorithm.run(self, n_i, d_i, s_i)

    def _algorithm(self, n_i, d_i, s_i):
        S = numpy.pi * numpy.sum(s_i * n_i * d_i ** 2, axis=1) # um^2/cm^3
        return S

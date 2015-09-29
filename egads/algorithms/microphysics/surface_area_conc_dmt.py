__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__version__ = "$Revision:: 125       $"
__all__ = ['SurfaceAreaConcDmt']

import numpy

import egads
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class SurfaceAreaConcDmt(egads_core.EgadsAlgorithm):

    """
    FILE        surface_area_conc_dmt.py

    VERSION     $Revision: 125 $

    CATEGORY    Microphysics

    PURPOSE     Calculates surface area concentration given size distribution
                from particle probe.

    DESCRIPTION Calculates surface area concentration (2nd moment) given
                size distribution from particle probe.

    INPUT       n_i    array[time,bins]    cm-3    number concentration of hydrometeors
                                                   in size category i
                d_i    vector[bins]        um      average diameter of size category i
                s_i    array[time,bins]    _       shape factor of hydrometeor in size category
                                                   i to account for asphericity

    OUTPUT      S      vector[time]        um2 cm3 Surface area concentration

    SOURCE      

    REFERENCES  "Data Analysis User's Guide", Droplet Measurement Technologies, 2009,
                44 pp.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'um^2/cm^3',
                                                               'long_name':'surface area concentration',
                                                               'standard_name':'',
                                                               'Category':['microphysics']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['n_i', 'd_i', 's_i'],
                                                          'InputUnits':['cm^-3', 'um', ''],
                                                          'Outputs':['S'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, n_i, d_i, s_i):

        return egads_core.EgadsAlgorithm.run(self, n_i, d_i, s_i)


    def _algorithm(self, n_i, d_i, s_i):


        S = egads.units.pi * numpy.sum(s_i * n_i * d_i ** 2, axis=1) # um^2/cm^3

        return S



__author__ = "mfreer"
__date__ = "$Date:: 2013-02-17 18:01#$"
__version__ = "$Revision:: 163       $"
__all__ = ['MassConcDmt']

import numpy

import egads
import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class MassConcDmt(egads_core.EgadsAlgorithm):

    """
    FILE        mass_conc_dmt.py

    VERSION     $Revision: 163 $

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

    REFERENCES  "Data Analysis User's Guide", Droplet Measurement Technologies, 2009,
                44 pp.

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'g/cm^3',
                                                               'long_name':'Mass concentration',
                                                               'standard_name':'',
                                                               'Category':['Microphysics']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['c_i', 'd_i', 's_i', 'rho_i'],
                                                          'InputUnits':['cm^-3', 'um', '', 'g/cm^3'],
                                                          'Outputs':['M'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, c_i, d_i, s_i, rho_i):

        return egads_core.EgadsAlgorithm.run(self, c_i, d_i, s_i, rho_i)

    def _algorithm(self, c_i, d_i, s_i, rho_i):

        d_i = d_i * 1.0e-4  # convert from um to cm

        if c_i.ndim <= 1:
            M = egads.units.pi / 6.0 * numpy.sum(s_i * rho_i * c_i * d_i ** 3)
        else:
            M = egads.units.pi / 6.0 * numpy.sum(s_i * rho_i * c_i * d_i ** 3, axis=1)



        return M



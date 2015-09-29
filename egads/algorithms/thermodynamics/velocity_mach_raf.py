__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__version__ = "$Revision:: 125       $"
__all__ = ['VelocityMachRaf']

import numpy

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata


class VelocityMachRaf(egads_core.EgadsAlgorithm):
    """
    FILE        velocity_mach_raf.py

    VERSION     $Revision: 125 $

    CATEGORY    Thermodynamics

    PURPOSE     Calculates mach number based on dynamic and static pressure

    DESCRIPTION 

    INPUT       dP        vector[time]    hPa    dynamic pressure
                Ps        vector[time]    hPa    static pressure

    OUTPUT      M         vector[time]    _      mach number

    SOURCE      NCAR-EOL

    REFERENCES  NCAR-RAF Bulletin #23

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)


        self.output_metadata = egads_metadata.VariableMetadata({'units':'',
                                                               'long_name':'mach number',
                                                               'standard_name':'',
                                                               'Category':['']})


        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['dP', 'Ps'],
                                                          'InputUnits':['hPa', 'hPa'],
                                                          'Outputs':['M'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)


    def run(self, dP, Ps):

        return egads_core.EgadsAlgorithm.run(self, dP, Ps)


    def _algorithm(self, dP, Ps):

        gamma = 1.4

        M = numpy.sqrt(2.0 / (gamma - 1.0) * ((dP / Ps + 1.0) ** ((gamma - 1) / gamma) - 1))

        return M



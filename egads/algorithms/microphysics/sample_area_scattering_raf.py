__author__ = "mfreer"
__date__ = "$Date:: 2012-02-07 17:23#$"
__version__ = "$Revision:: 125       $"
__all__ = ['SampleAreaScattingRaf']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class SampleAreaScattingRaf(egads_core.EgadsAlgorithm):
    """

    FILE        sample_area_scattering_raf.py

    VERSION     $Revision: 125 $

    CATEGORY    Microphysics

    PURPOSE     Calculation of sampling area for scattering probes

    DESCRIPTION Calculation of sampling area for scattering probes such as the FSSP,
                CAS, CIP, etc., given depth of field and beam diameter.

    INPUT       DOF     coeff.      m   Depth of field
                BD      coeff.      m   Beam diameter

    OUTPUT      SA      coeff.      m2  Sample area

    SOURCE      NCAR-RAF

    REFERENCES  NCAR-RAF Bulletin No. 24

    """


    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m^2',
                                                               'long_name':'sample area',
                                                               'standard_name':'',
                                                               'Category':['PMS Probe']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['DOF', 'BD'],
                                                          'InputUnits':['m', 'm'],
                                                          'InputTypes':['coeff','coeff'],
                                                          'InputDescription':['Depth of field','Beam diameter'],
                                                          'Outputs':['SA'],
                                                          'OutputDescription':['Sample area'],
                                                          'Purpose':'Calculation of sampling area for scattering probes',
                                                          'Description':'Calculation of sampling area for scattering probes such as the FSSP, CAS, CIP, etc., given depth of field and beam diameter',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)



    def run(self, DOF, BD):

        return egads_core.EgadsAlgorithm.run(self, DOF, BD)

    def _algorithm(self, DOF, BD):

        SA = DOF * BD

        return SA


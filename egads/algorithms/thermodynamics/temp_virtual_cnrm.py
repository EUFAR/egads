__author__ = "mfreer"
__date__ = "2011-05-27 14:27"
__version__ = "1.0"
__all__ = ["TempVirtualCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class TempVirtualCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        temp_virtual_cnrm.py

    VERSION     1.0

    CATEGORY    Thermodynamics

    PURPOSE     Calculate virtual temperature

    DESCRIPTION Calculates virtual temperature given static pressure and mixing ratio.

    INPUT       T_s     vector      K or C           static temperature
                r       vector      g/kg             water vapor mixing ratio

    OUTPUT      T_v     vector      K or C           virtual temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Triplet-Roche, page 56.
    """
    
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'virtual temperature',
                                                               'standard_name':'virtual_temperature',
                                                               'Category':['Thermodynamics','Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_s', 'r'],
                                                          'InputUnits':['K','g/kg'],
                                                          'InputTypes':['vector','vector'],
                                                          'InputDescription':['Static temperature','Water vapor mixing ratio'],
                                                          'Outputs':['T_v'],
                                                          'OutputUnits':['K'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Virtual temperature'],
                                                          'Purpose':'Calculate virtual temperature',
                                                          'Description':'Calculates virtual temperature given static pressure and mixing ratio',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'Triplet-Roche, page 56',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, T_s, r):
        return egads_core.EgadsAlgorithm.run(self, T_s, r)

    def _algorithm(self, T_s, r):
        RvRa = 1.608
        T_v = T_s * (1 + RvRa * r) / (1 + r)
        return T_v


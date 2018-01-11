__author__ = "mfreer, ohenry"
__date__ = "2017-01-17 11:44"
__version__ = "1.0"
__all__ = ["TempStaticCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class TempStaticCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        temp_static_cnrm.py

    VERSION     1.0

    CATEGORY    Thermodynamic

    PURPOSE     Calculate static temperature.

    DESCRIPTION Calculates static temperature of the air based on total temperature and dynamic
                pressure. This method applies to probe types such as the Rosemount.

    INPUT       T_t         vector  K or C  measured total temperature
                dP          vector  hPa     dynamic pressure
                P_s         vector  hPa     static pressure
                r_f         coeff.  _       probe recovery coefficient
                Racpa       coeff.  _       R_a/c_pa

    OUTPUT      T_s         vector  K       static temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES
    """
    
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'static temperature',
                                                               'standard_name':'air_temperature',
                                                               'Category':['Thermodynamics','Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_t', 'dP', 'P_s', 'r_f', 'Racpa'],
                                                          'InputUnits':['K','hPa','hPa','', ''],
                                                          'InputTypes':['vector','vector','vector','coeff','coeff'],
                                                          'InputDescription':['Total temperature','Dynamic pressure','Static pressure','','R_a/c_pa'],
                                                          'Outputs':['T_s'],
                                                          'OutputUnits':['K'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Static temperature'],
                                                          'Purpose':'Calculate static temperature',
                                                          'Description':'Calculates static temperature of the air based on total temperature and dynamic pressure',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, Tt, dP, P_s, r_f, Racpa):
        return egads_core.EgadsAlgorithm.run(self, Tt, dP, P_s, r_f, Racpa)

    def _algorithm(self, Tt, dP, P_s, r_f, Racpa):
        T_s = Tt / (1 + r_f * ((1 + dP / P_s) ** Racpa - 1))
        return T_s


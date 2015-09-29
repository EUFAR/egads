__author__ = "mfreer"
__date__ = "$Date:: 2011-05-27 14:27#$"
__version__ = "$Revision:: 59        $"
__all__ = ["TempStaticCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class TempStaticCnrm(egads_core.EgadsAlgorithm):
    """

    FILE        temp_static_cnrm.py

    VERSION     $Revision: 59 $

    CATEGORY    Thermodynamic

    PURPOSE     Calculate static temperature

    DESCRIPTION Calculates static temperature of the air based on total temperature and dynamic
                pressure

    INPUT       T_t         vector  K or C  total temperature
                dP          vector  hPa     dynamic pressure
                P_s         vector  hPa     static pressure
                r_f         coeff.  ()
                Racpa       coeff.  ()      R_a/c_pa

    OUTPUT      T_s         vector  K       static temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """
    
    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'static temperature',
                                                               'standard_name':'air_temperature',
                                                               'Category':['Thermodynamic','Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_t', 'dP', 'P_s', 'r_f', 'Racpa'],
                                                          'InputUnits':['K','hPa','hPa','', ''],
                                                          'Outputs':['T_s'],
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


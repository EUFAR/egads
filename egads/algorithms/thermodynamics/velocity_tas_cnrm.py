__author__ = "mfreer"
__date__ = "$Date:: 2012-01-27 16:41#$"
__version__ = "$Revision:: 100       $"
__all__ = ["VelocityTasCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class VelocityTasCnrm(egads_core.EgadsAlgorithm):
    """

    FILE        velocity_tas_cnrm.py

    VERSION     $Revision: 100 $

    CATEGORY    Thermodynamics

    PURPOSE     Calculate true airspeed

    DESCRIPTION Calculates true airspeed based on static temperature, static pressure
                and dynamic pressure using St Venant's formula.

    INPUT       T_s         vector  K or C      static temperature
                P_s         vector  hPa         static pressure
                dP          vector  hPa         dynamic pressure
                cpa         coeff.  J K-1 kg-1  specific heat of air (dry air is 1004 J K-1 kg-1)
                Racpa       coeff.  ()          R_a/c_pa

    OUTPUT      V_p         vector  m s-1       true airspeed

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  "Mecanique des fluides", by S. Candel, Dunod.

                 Bulletin NCAR/RAF Nr 23, Feb 87, by D. Lenschow and
                 P. Spyers-Duran

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'True Air Speed',
                                                               'standard_name':'platform_speed_wrt_air',
                                                               'Category':['Thermodynamic', 'Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_s', 'P_s', 'dP', 'cpa', 'Racpa'],
                                                          'InputUnits':['K', 'hPa', 'hPa', 'J/K/kg', ''],
                                                          'Outputs':['V_p'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, T_s, P_s, dP, cpa, Racpa):

        return egads_core.EgadsAlgorithm.run(self, T_s, P_s, dP, cpa, Racpa)


    def _algorithm(self, T_s, P_s, dP, cpa, Racpa):

        V_p = (2 * cpa * T_s * ((1 + dP / P_s) ** Racpa
                        - 1)) ** .5

        return V_p




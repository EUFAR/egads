__author__ = "mfreer, ohenry"
__date__ = "2017-01-17 13:29"
__version__ = "1.0"
__all__ = ["VelocityTasCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class VelocityTasCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        velocity_tas_cnrm.py

    VERSION     1.0

    CATEGORY    Thermodynamics

    PURPOSE     Calculate true airspeed.

    DESCRIPTION Calculates true airspeed based on static temperature, static pressure
                and dynamic pressure using St Venant's formula.

    INPUT       T_s         vector  K or C      static temperature
                P_s         vector  hPa         static pressure
                dP          vector  hPa         dynamic pressure
                cpa         coeff.  J K-1 kg-1  specific heat of air (dry air is 1004 J K-1 kg-1)
                Racpa       coeff.  _           R_a/c_pa

    OUTPUT      V_p         vector  m s-1       true airspeed

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  "Mecanique des fluides", by S. Candel, Dunod.

                 Bulletin NCAR/RAF Nr 23, Feb 87, by D. Lenschow and P. Spyers-Duran
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m/s',
                                                               'long_name':'True Air Speed',
                                                               'standard_name':'platform_speed_wrt_air',
                                                               'Category':['Thermodynamics', 'Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_s', 'P_s', 'dP', 'cpa', 'Racpa'],
                                                          'InputUnits':['K', 'hPa', 'hPa', 'J/K/kg', ''],
                                                          'InputTypes':['vector','vector','vector','coeff','coeff'],
                                                          'InputDescription':['Static temperature','Static pressure','Dynamic pressure','specific heat of air (dry air is 1004 J K-1 kg-1)','R_a/c_pa'],
                                                          'Outputs':['V_p'],
                                                          'OutputUnits':['m/s'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['true airspeed'],
                                                          'Purpose':'Calculate true airspeed',
                                                          'Description':"Calculates true airspeed based on static temperature, static pressure and dynamic pressure using St Venant's formula",
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'"Mecanique des fluides", by S. Candel, Dunod. Bulletin NCAR/RAF Nr 23, Feb 87, by D. Lenschow and P. Spyers-Duran',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, T_s, P_s, dP, cpa, Racpa):
        return egads_core.EgadsAlgorithm.run(self, T_s, P_s, dP, cpa, Racpa)

    def _algorithm(self, T_s, P_s, dP, cpa, Racpa):
        V_p = numpy.sqrt(2 * cpa * T_s * ((1 + dP / P_s) ** Racpa - 1))
        return V_p


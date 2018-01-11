__author__ = "mfreer"
__date__ = "2012-01-27 16:41"
__version__ = "10.0"
__all__ = ["DensityDryAirCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class DensityDryAirCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        density_dry_air_cnrm.py

    VERSION     1.0

    CATEGORY    Thermodynamics

    PURPOSE     Calculates density of dry air

    DESCRIPTION Calculates density of dry air given static temperature and
                pressure. If virtual temperature is used instead of static, this
                algorithm calculates density of humid air.

    INPUT       P_s     vector  hPa     static pressure
                T_s     vector  K or C  static temperature

    OUTPUT      rho     vector  kg/m3   density

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Equation of state for a perfect gas, Triplet-Roche, page 34.
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'kg/m^3',
                                                               'long_name':'density',
                                                               'standard_name':'air_density',
                                                               'Category':['Thermodynamics', 'Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['P_s', 'T_s'],
                                                          'InputUnits':['hPa', 'K'],
                                                          'InputTypes':['vector','vector'],
                                                          'InputDescription':['Static pressure','Static temperature'],
                                                          'Outputs':['rho'],
                                                          'OutputUnits':['kg/m^3'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Density'],
                                                          'Purpose':'Calculates density of dry air',
                                                          'Description':'Calculates density of dry air given static temperature and pressure. If virtual temperature is used instead of static, this algorithm calculates density of humid air',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'Equation of state for a perfect gas, Triplet-Roche, page 34.',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, P_s, T_s):
        return egads_core.EgadsAlgorithm.run(self, P_s, T_s)

    def _algorithm(self, P_s, T_s):
        R_a = 287.05 #J/kg/K
        rho = (P_s * 100) / (R_a * T_s)
        return rho


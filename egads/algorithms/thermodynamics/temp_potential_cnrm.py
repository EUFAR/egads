__author__ = "mfreer"
__date__ = "2012-01-27 16:41"
__version__ = "1.0"
__all__ = ["TempPotentialCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class TempPotentialCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        temp_potential_cnrm.py

    VERSION     1.0

    CATEGORY    Thermodynamics

    PURPOSE     Calculates potential temperature.

    DESCRIPTION Calculates potential temperature given static temperature, pressure,
                and the ratio of gas constant and specific heat of air.

    INPUT       T_s     vector  K or C          static temperature
                P_s     vector  hPa             static pressure
                Racpa   coeff.                  gas constant of air divided by
                                                specific heat of air at constant pressure

    OUTPUT      theta   vector  same as T_s     potential temperature

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Triplet-Roche.
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'K',
                                                               'long_name':'potential temperature',
                                                               'standard_name':'air_potential_temperature',
                                                               'Category':['Thermodynamics', 'Atmos State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['T_s', 'P_s', 'Racpa'],
                                                          'InputUnits':['K', 'hPa', ''],
                                                          'InputTypes':['vector','vector','coeff'],
                                                          'InputDescription':['Static temperature','Static pressure','gas constant of air divided by specific heat of air at constant pressure'],
                                                          'Outputs':['theta'],
                                                          'OutputUnits':['K'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Potential temperature'],
                                                          'Purpose':'Calculates potential temperature',
                                                          'Description':'Calculates potential temperature given static temperature, pressure, and the ratio of gas constant and specific heat of air',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'Triplet-Roche.',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, T_s, P_s, Racpa):
        return egads_core.EgadsAlgorithm.run(self, T_s, P_s, Racpa)

    def _algorithm(self, T_s, P_s, Racpa):
        theta = T_s * (1000.0 / P_s) ** Racpa
        return theta


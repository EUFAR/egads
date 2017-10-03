__author__ = "ohenry"
__date__ = "2017-09-27 08:44"
__version__ = "1.1"
__all__ = ["AltitudePressureIncrementalCnrm"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class AltitudePressureIncrementalCnrm(egads_core.EgadsAlgorithm):
    
    """
    FILE        altitude_pressure_incremental_cnrm.py

    VERSION     1.1

    CATEGORY    Thermodynamics

    PURPOSE     Calculate pressure altitude incrementally

    DESCRIPTION Calculate a pressure altitude incrementally along the trajectory of an aircraft
                from the Laplace formula (Z2 = Z1 + Ra/g < Tv > log(P1/P2)).

    INPUT       P_s         vector           hPa       static pressure
                T_v         vector           K or C    virtual temperature
                t           vector           s         measurement period
                Z0          coeff            m         reference altitude (at S0 if S0 is provided,
                                                       can be airport altitude (m) if S0 is not 
                                                       provided and measurements start in airport)
                S0          coeff,optional   s         reference time (if not provided, S0 = t[0]
                
    OUTPUT      alt_p         vector           m         pressure altitude

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES  Equation of state for a perfect gas, Triplet-Roche, page 36.
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'m',
                                                               'long_name':'pressure altitude calculated incrementally',
                                                               'standard_name':'pressure altitude',
                                                               'Category':['Thermodynamics', 'Aircraft State']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['P_s','T_v','t','Z0','S0'],
                                                          'InputUnits':['hPa','K','s','m','s'],
                                                          'InputTypes':['vector','vector','vector','coeff','coeff_optional'],
                                                          'InputDescription':['Static pressure',
                                                                              'Virtual temperature',
                                                                              'Measurement period',
                                                                              'reference altitude (at S0 if S0 is provided,can be airport altitude (m) if S0 is not provided and measurements start in airport)',
                                                                              'reference time (if not provided, S0 = t[0]'],
                                                          'Outputs':['alt_p'],
                                                          'OutputUnits':['m'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Pressure altitude'],
                                                          'Purpose':'Calculate pressure altitude incrementally',
                                                          'Description':'Calculate a pressure altitude incrementally along the trajectory of an aircraft from the Laplace formula (Z2 = Z1 + Ra/g < Tv > log(P1/P2)).',
                                                          'Category':'Thermodynamics',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':"Equation of state for a perfect gas, Triplet-Roche, page 36.",
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, P_s, T_v, t, Z0, S0=None):
        return egads_core.EgadsAlgorithm.run(self, P_s, T_v, t, Z0, S0)

    def _algorithm(self, P_s, T_v, t, Z0, S0=None):
        R_a = 287.0531
        g = 9.80665
        R_ag = R_a / g
        nb_val = P_s.size
        alt_p = numpy.zeros(nb_val)
        if not S0:
            S0 = t[0]
        index_S0 = numpy.where(t > S0)[0][0] - 1
        alt_p[index_S0] = Z0
        before_S0 = list(reversed(range(index_S0)))
        after_S0 = range(index_S0 + 1, nb_val, 1)
        
        for i in before_S0:
            alt_p[i] = alt_p[i + 1] + R_ag * ((T_v[i] + T_v[i + 1])/2.)*numpy.log(P_s[i + 1]/P_s[i])
        for i in after_S0:
            alt_p[i] = alt_p[i - 1] + R_ag * ((T_v[i] + T_v[i - 1])/2.)*numpy.log(P_s[i - 1]/P_s[i])
        
        return alt_p
        

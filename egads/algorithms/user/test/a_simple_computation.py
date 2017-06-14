__author__ = "Olivier Henry"
__date__ = "2017-5-3 15:16"
__version__ = "100"
__all__ = ["ASimpleComputation"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class ASimpleComputation(egads_core.EgadsAlgorithm):

    """
    FILE        a_simple_computation.py

    VERSION     100

    CATEGORY    Test

    PURPOSE     To launch a simple computation.

    DESCRIPTION The algorithm runs a simple computation from a vector.

    INPUT       P_s    vector    hPa    static pressure
                                        test fdsfsdfdsf sdfsdfsdf
                                        fdsdfsdf fsd fsdfsdf sdfsdfsdf
                T_s    vector    K      static temperature

    OUTPUT      res    vector    _    the result once the computation is fin
                                      ished

    SOURCE      

    REFERENCES  
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0',
                                                               'long_name':'result',
                                                               'standard_name':'result',
                                                               'Category':['Computation']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['P_s','T_s'],
                                                          'InputUnits':['hPa','K'],
                                                          'InputTypes':['vector','vector'],
                                                          'InputDescription':['static pressure','static temperature'],
                                                          'Outputs':['res'],
                                                          'OutputDescription':['the result once the computation is finished'],
                                                          'Purpose':'To launch a simple computation.',
                                                          'Description':'The algorithm runs a simple computation from a vector.',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                         self.output_metadata)

    def run(self, P_s):
        return egads_core.EgadsAlgorithm.run(self, P_s)

    def _algorithm(self, P_s):
        res = (P_s * 10.)
        res = (res / 2.) / 5.
        return res
    
    
__author__ = "olivier"
__date__ = "$Date:: 2017-6-22 14:14#$"
__version__ = "$Revision:: 1       $"
__all__ = ["MyAlgorithmForCorrection"]

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class MyAlgorithmForCorrection(egads_core.EgadsAlgorithm):

    """
    FILE        my_algorithm_for_correction.py

    VERSION     $Revision: 100 $

    CATEGORY    Corrections

    PURPOSE     To correct an issue in a variable

    DESCRIPTION This algorithm has been designed to correct a variable for scale factor and
                 offset

    INPUT       var    vector    _    variable to be corrected

    OUTPUT      res    vector    _    variable corrected for scale factor a
                                      nd offset

    SOURCE      

    REFERENCES  
    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0',
                                                               'long_name':'input0 corrected for scale factor and offset',
                                                               'standard_name':'input0 corrected',
                                                               'Category':['Correction']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['var'],
                                                          'InputUnits':[None],
                                                          'InputTypes':['vector'],
                                                          'InputDescription':['variable to be corrected'],
                                                          'Outputs':['res'],
                                                          'OutputDescription':['variable corrected for scale factor and offset'],
                                                          'Purpose':'To correct an issue in a variable',
                                                          'Description':'This algorithm has been designed to correct a variable for scale factor and offset',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, var):
        return egads_core.EgadsAlgorithm.run(self, var)

    def _algorithm(self, var):
        res = (var / 3.45) - 15.
        return res

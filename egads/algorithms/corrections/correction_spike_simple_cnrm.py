__author__ = "mfreer"
__date__ = "2012-06-22 17:19"
__version__ = "1.1"
__all__ = ['CorrectionSpikeSimpleCnrm']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
from copy import deepcopy
from numpy import abs

class CorrectionSpikeSimpleCnrm(egads_core.EgadsAlgorithm):
    """
    FILE        correction_spike_simple_cnrm.py

    VERSION     1.1

    CATEGORY    Corrections

    PURPOSE     Detects and corrects spikes which exceed a specific threshold

    DESCRIPTION This algorithm detects spikes exceeding a specified threshold and corrects
                the spike with a mean of the surrounding values. This algorithm does not apply well
                to variables that are naturally discontinuous.

    INPUT       X        vector        _        Parameter for analysis
                S0       coeff         _        Spike detection threshold (same units 
                                                as X, must be positive)

    OUTPUT      X_corr   vector        _        Parameter with corrections applied

    SOURCE      CNRM/GMEI/TRAMM

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0',
                                                               'long_name':'input0 corrected',
                                                               'standard_name':'input0',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['X', 'S0'],
                                                          'InputUnits':[None, None],
                                                          'InputTypes':['vector','coeff'],
                                                          'InputDescription':['Parameter for analysis','Spike detection threshold (same units as X, must be positive)'],
                                                          'Outputs':['X_corr'],
                                                          'OutputUnits':['input0'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Parameter with corrections applied'],
                                                          'Purpose':'Detects and corrects spikes which exceed a specific threshold',
                                                          'Description':'This algorithm detects spikes exceeding a specified threshold and corrects the spike with a mean of the surrounding values. This algorithm does not apply well to variables that are naturally discontinuous',
                                                          'Category':'Corrections',
                                                          'Source':'CNRM/GMEI/TRAMM',
                                                          'References':'',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, X, S0):
        return egads_core.EgadsAlgorithm.run(self, X, S0)

    def _algorithm(self, X, S0):
        X_corr = deepcopy(X)
        for i, X_i in enumerate(X):
            i_up = i + 1
            i_down = i - 1
            if i_up < len(X) and i_down >= 0:
                if (abs(X_i - X[i_down]) > S0 and abs(X_i - X[i_up]) > S0 and
                        ((X_i - X[i_down]) * (X_i - X[i_up])) > 0):
                    X_corr[i] = (X[i_up] + X[i_down]) / 2.0
        return X_corr


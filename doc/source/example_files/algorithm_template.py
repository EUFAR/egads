__author__ = "mfreer, ohenry"
__date__ = "2016-12-14 15:04"
__version__ = "1.0"
__all__ = ['']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

# 1. Change class name to algorithm name (same as filename) but 
#    following MixedCase conventions. 

class AlgorithmTemplate(egads_core.EgadsAlgorithm):
    
# 2. Edit docstring to reflect algorithm description and input/output 
#    parameters used

    """
    This file provides a template for creation of EGADS algorithms.

    FILE        algorithm_template.py

    VERSION     1.0

    CATEGORY    None

    PURPOSE     Template for EGADS algorithm files

    DESCRIPTION ...

    INPUT       inputs      var_type    units   description

    OUTPUT      outputs     var_type    units   description

    SOURCE      sources

    REFERENCES  references

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        # 3. Complete output_metadata with metadata of the parameter(s) to be
        #    produced by this algorithm. In the case of multiple parameters, 
        #    use the  following formula:
        #        self.output_metadata = []
        #        self.output_metadata.append(egads_metadata.VariableMetadata(...)
        #        self.output_metadata.append(egads_metadata.VariableMetadata(...)
        #        ...
        
        self.output_metadata = egads_metadata.VariableMetadata({
            'units':'%',
            'long_name':'template',
            'standard_name':'',
            'Category':['']
            })

        # 3 cont. Complete metadata with parameters specific to algorithm, 
        #    including a list of inputs, a corresponding list of units, and 
        #    the list of outputs. InputTypes are linked to the different 
        #    var_type written in the docstring 
        
        self.metadata = egads_metadata.AlgorithmMetadata({
            'Inputs':['input'],
            'InputUnits':['unit'],
            'InputTypes':['vector'],
            'InputDescription':['A description for an input'],
            'Outputs':['template'],
            'OutputDescription':['A description for an output'],
            'Purpose':'Template for EGADS algorithm files',
            'Description':'...',
            'Category':'None',
            'Source':'sources',
            'Reference':'references',
            'Processor':self.name,
            'ProcessorDate':__date__,
            'ProcessorVersion':__version__,
            'DateProcessed':self.now()
            }, self.output_metadata)

    # 4. Replace the 'inputs' parameter in the three instances below with the 
    #    list of input parameters to be used in the algorithm.
    
    def run(self, inputs):

        return egads_core.EgadsAlgorithm.run(self, inputs)

    # 5. Implement algorithm in this section.
    
    def _algorithm(self, inputs):

        ## Do processing here:

        return result

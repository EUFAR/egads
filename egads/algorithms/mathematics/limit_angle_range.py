__author__ = "mfreer"
__date__ = "$Date:: 2013-02-17 18:01#$"
__version__ = "$Revision:: 163       $"
__all__ = ['LimitAngleRange']


import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

import numpy

class LimitAngleRange(egads_core.EgadsAlgorithm):
    """

    FILE        limit_angle_range.py

    VERSION     $Revision: 163 $

    CATEGORY    Mathematics

    PURPOSE     This function calculates the corresponding angle between 0 and 360 degrees given
                an angle of any size.

    DESCRIPTION 

    INPUT       angle            vector    degrees    angle to limit to between 0 and 360 degrees

    OUTPUT      angle_limited    vector    degrees    resulting angles

    SOURCE      

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'deg',
                                                               'long_name':'',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['angle'],
                                                          'InputUnits':['deg'],
                                                          'Outputs':['angle_limited'],
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, angle):

        return egads_core.EgadsAlgorithm.run(self, angle)

    def _algorithm(self, angle):

        angle_div = angle / 360.0

        angle_fraction = abs(angle_div - numpy.int0(angle_div))

        if angle.size == 1:
            if angle >= 0:
                angle_limited = 360 * angle_fraction
            else:
                angle_limited = 360 - 360 * angle_fraction
        else:
            angle_limited = numpy.zeros(angle.size)

            angle_limited[angle >= 0] = 360 * angle_fraction[angle >= 0]
            angle_limited[angle < 0] = 360 - 360 * angle_fraction[angle < 0]

        return angle_limited





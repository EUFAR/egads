__author__ = "mfreer"
__date__ = "2013-02-17 18:01"
__version__ = "1.3"
__all__ = ['LimitAngleRange']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy

class LimitAngleRange(egads_core.EgadsAlgorithm):
    """

    FILE        limit_angle_range.py

    VERSION     1.3

    CATEGORY    Mathematics

    PURPOSE     Function to calculate the corresponding angle.

    DESCRIPTION This function calculates the corresponding angle between 0 and 360 degrees given
                an angle of any size.

    INPUT       angle            vector    degree    angle to limit to between 0 and 360 degrees

    OUTPUT      angle_limited    vector    degree    resulting angles

    SOURCE      

    REFERENCES

    """

    def __init__(self, return_Egads=True):
        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'degree',
                                                               'long_name':'',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['angle'],
                                                          'InputUnits':['degree'],
                                                          'InputTypes':['vector'],
                                                          'InputDescription':['Angle to limit to between 0 and 360 degrees'],
                                                          'Outputs':['angle_limited'],
                                                          'OutputUnits':['degree'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Resulting angles'],
                                                          'Purpose':'This function calculates the corresponding angle between 0 and 360 degrees given an angle of any size',
                                                          'Description':'No description',
                                                          'Category':'Mathematics',
                                                          'Source':'',
                                                          'References':'',
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


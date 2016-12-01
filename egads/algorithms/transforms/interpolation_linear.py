__author__ = "mfreer"
__date__ = "$Date:: 2012-06-22 17:19#$"
__version__ = "$Revision:: 140       $"
__all__ = ['InterpolationLinear']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata

class InterpolationLinear(egads_core.EgadsAlgorithm):
    """

    FILE        interpolation_linear.py

    VERSION     $Revision: 140 $

    CATEGORY    Transforms

    PURPOSE     Calculate linear interpolation of a variable.

    DESCRIPTION Calculates the one-dimensional piecewise linear interpolation 
                of a variable between two coordinate systems.

    INPUT       x            vector            _    x-coordinates of the data 
                                                    points (must be increasing)
                f            vector            _    data points to interpolate
                x_interp     vector            _    new set of coordinates to use in interpolation
                f_left       coeff, optional   _    value to return for x_interp < x[0]. 
                                                    default is f[0]
                f_right      coeff, optional   _    value to return when x_interp > x[-1]. 
                                                    default is f[-1]
                                                    
    OUTPUT      f_interp     vector            _    interpolated values of f

    SOURCE      sources

    REFERENCES

    """

    def __init__(self, return_Egads=True):

        egads_core.EgadsAlgorithm.__init__(self, return_Egads)

        self.output_metadata = egads_metadata.VariableMetadata({'units':'input0',
                                                               'long_name':'',
                                                               'standard_name':'',
                                                               'Category':['']})

        self.metadata = egads_metadata.AlgorithmMetadata({'Inputs':['x', 'f', 'x_interp', 'f_left', 'f_right'],
                                                          'InputUnits':[None, None, None, None, None],
                                                          'InputTypes':['vector','vector','vector','coeff_optional','coeff_optional'],
                                                          'InputDescription':['x-coordinates of the data points (must be increasing)','Data points to interpolate','New set of coordinates to use in interpolation','value to return for x_interp < x[0], default is f[0]','Value to return when x_interp > x[-1], default is f[-1]'],
                                                          'Outputs':['interpolated values of f'],
                                                          'OutputDescription':['Interpolated values of f'],
                                                          'Purpose':'Calculate linear interpolation of a variable',
                                                          'Description':'Calculates the one-dimensional piecewise linear interpolation of a variable between two coordinate systems',
                                                          'Processor':self.name,
                                                          'ProcessorDate':__date__,
                                                          'ProcessorVersion':__version__,
                                                          'DateProcessed':self.now()},
                                                          self.output_metadata)

    def run(self, x, f, x_interp, f_left=None, f_right=None):

        return egads_core.EgadsAlgorithm.run(self, x, f, x_interp, f_left, f_right)

    def _algorithm(self, x, f, x_interp, f_left, f_right):

        if not f_left:
            f_left = f[0]

        if not f_right:
            f_right = f[-1]

        f_interp = []

        for x_val in x_interp:
            if x_val < x[0]:
                f_interp.append(f_left)
            elif x_val > x[-1]:
                f_interp.append(f_right)
            else:
                lower_x = x[x <= x_val][0]
                lower_f = f[x <= x_val][0]

                upper_x = x[x >= x_val][0]
                upper_f = f[x >= x_val][0]

                f_val = lower_f + (x_val - lower_x) * (upper_f - lower_f) / (upper_x - lower_x)

                f_interp.append(f_val)



        return f_interp



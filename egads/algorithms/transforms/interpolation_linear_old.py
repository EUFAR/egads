__author__ = "mfreer,ohenry"
__date__ = "2016-01-04 09:39"
__version__ = "1.2"
__all__ = ['InterpolationLinearOld']

import egads.core.egads_core as egads_core
import egads.core.metadata as egads_metadata
import numpy as np

class InterpolationLinearOld(egads_core.EgadsAlgorithm):
    
    """
    FILE        interpolation_linear_old.py

    VERSION     1.2

    CATEGORY    Transforms

    PURPOSE     Calculate linear interpolation of a variable.

    DESCRIPTION Calculates the one-dimensional piecewise linear interpolation 
                of a variable between two coordinate systems. The algorithm will
                calculate an interpolated value at each coordinate even if it exists 
                in the new coordinate vector.

    INPUT       x            vector            _    x-coordinates of the data points (must be 
                                                    increasing and must be the same size as f)
                f            vector            _    data points to interpolate (nan can be used
                                                    where data are missing, must be the same size
                                                    as x)
                x_interp     vector            _    new set of coordinates to use in interpolation
                f_left       coeff, optional   _    value to return for x_interp < x[0], nan can be 
                                                    used if nans are present at the beginning of f 
                                                    and the user wants to keep them.
                                                    default is f[0], if nan are present at the beginning
                                                    of f, the algorithm will keep them.
                f_right      coeff, optional   _    value to return when x_interp > x[-1], nan can be 
                                                    used if nans are present at the end of f and the 
                                                    user wants to keep them.
                                                    default is f[-1], if nan are present at the end
                                                    of f, the algorithm will keep them.
                                                    
    OUTPUT      f_interp     vector            _    interpolated values of f, nans at the beginning 
                                                    and at the end are removed if f_right and f_left
                                                    are not set to nan.

    SOURCE

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
                                                          'InputDescription':['X-coordinates of the data points (must be increasing and must be the same size as f)',
                                                                              'Data points to interpolate (nan can be used where data are missing, must be the same size as x)',
                                                                              'New set of coordinates to use in interpolation',
                                                                              'Value to return for x_interp < x[0], nan can be used if nans are present at the beginning of f and the user wants to keep them. Default is f[0], if nan are present at the beginning of f, the algorithm will keep them.',
                                                                              'Value to return when x_interp > x[-1], nan can be used if nans are present at the end of f and the user wants to keep them. Default is f[-1], if nan are present at the end of f, the algorithm will keep them.'],
                                                          'Outputs':['f_interp'],
                                                          'OutputUnits':['input0'],
                                                          'OutputTypes':['vector'],
                                                          'OutputDescription':['Interpolated values of f, nans at the beginning and at the end are removed if f_right and f_left are not set to nan.'],
                                                          'Purpose':'Calculate linear interpolation of a variable',
                                                          'Description':'Calculates the one-dimensional piecewise linear interpolation of a variable between two coordinate systems',
                                                          'Category':'Transforms',
                                                          'Source':'',
                                                          'References':'',
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
        index = np.argwhere(~np.isnan(f))
        f = f[index]
        x = x[index]
        for x_val in x_interp:
            if x_val < x[0]:
                f_interp.append(f_left)
            elif x_val > x[-1]:
                f_interp.append(f_right)
            else:
                try:
                    lower_x = x[x < x_val][-1]
                except IndexError:
                    lower_x = x_val
                try:
                    lower_f = f[x < x_val][-1]
                except IndexError:
                    lower_f = f[0][0]
                try:
                    upper_x = x[x > x_val][0]
                except IndexError:
                    upper_x = x_val
                try:
                    upper_f = f[x > x_val][0]
                except IndexError:
                    upper_f = f[-1][0]
                f_interp.append(lower_f + (x_val - lower_x) * (upper_f - lower_f) / (upper_x - lower_x))
        return f_interp


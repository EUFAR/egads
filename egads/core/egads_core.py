__author__ = "mfreer"
__date__ = "$Date:: 2012-07-06 17:42#$"
__version__ = "$Revision:: 146       $"
__all__ = ["EgadsData", "EgadsAlgorithm"]


import weakref
import datetime
import re
import warnings
import numpy
import quantities as pq  # @UnresolvedImport
import metadata
from collections import defaultdict


class EgadsData(pq.Quantity):
    """
    This class is designed using the EUFAR Standards & Protocols data and metadata 
    recommendations. Its purpose is to store related data and metadata and allow them to be
    passed between functions and algorithms in a consistent manner.
    """

    __refs__ = defaultdict(list)
    

    def __new__(cls, value, units='', variable_metadata={}, dtype=None, **attrs):
        
        _add_new_units()
        
        if isinstance(units, metadata.VariableMetadata):
            if not variable_metadata:
                variable_metadata = units
            units = units.get('units', '')

        if variable_metadata and (not units):
            units = variable_metadata.get('units', '')
            if not units:
                units = variable_metadata.get('Units', '')


        units = _validate_units(units)

        if isinstance(value, pq.Quantity):
            ret = pq.Quantity.__new__(cls, value, value.units, dtype=dtype)
        else:
            try:
                ret = pq.Quantity.__new__(cls, value, units, dtype=dtype)
            except (LookupError, SyntaxError):
                ret = pq.Quantity.__new__(cls, value, units="", dtype=dtype)

        if isinstance(variable_metadata, metadata.VariableMetadata):
            ret.metadata = variable_metadata
        else:
            ret.metadata = metadata.VariableMetadata(variable_metadata)

        ret.metadata['units'] = units

        return ret


    def __init__(self, value, units='', variable_metadata=None, dtype='float64', **attrs):
        """
        Constructor Variables
    
        :param value:
            Scalar or array of values to initialize EgadsData object.
        :param string units:
            Optional - String representation of units to be used for current EgadsData instance, e.g.
            'm/s', 'kg', 'g/cm^3', etc.            
        :param VariableMetadata variable_metadata: 
            Optional - VariableMetadata dictionary object containing relevant metadata
            for the current EgadsData instance.
        :param **attrs:
            Optional - Keyword/value pairs of additional metadata which will be added into
            the existing variable_metadata object.
        """

        for key, val in attrs.iteritems():
            self.metadata[key] = val

        self.__refs__[self.__class__].append(weakref.ref(self))


    @property
    def value(self):
        return self.view(type=numpy.ndarray)
    @value.setter
    def value(self, value, indx=None):

        print value, indx

    @property
    def units(self):
        try:
            return super(EgadsData, self).units.dimensionality.string
        except KeyError:
            return ''
    @units.setter
    def units(self, units):
        pq.Quantity.units.fset(self, units)


#    def __len__(self):
#        return len(self.value)



    def __repr__(self):
        try:
            return repr(['EgadsData', self.value, self.dimensionality.string])
        except AttributeError:
            return repr(None)

    def __add__(self, other):
        return super(EgadsData, self).__add__(other).view(EgadsData)

    def __radd__(self, other):
        return super(EgadsData, self).__radd__(other).view(EgadsData)

    def __iadd__(self, other):
        return super(EgadsData, self).__iadd__(other).view(EgadsData)

    def __sub__(self, other):
        return super(EgadsData, self).__sub__(other).view(EgadsData)

    def __rsub__(self, other):
        return super(EgadsData, self).__rsub__(other).view(EgadsData)

    def __isub__(self, other):
        return super(EgadsData, self).__isub__(other).view(EgadsData)

    def __mod__(self, other):
        return super(EgadsData, self).__mod__(other).view(EgadsData)

    def __imod__(self, other):
        return super(EgadsData, self).__imod__(other).view(EgadsData)

    def __imul__(self, other):
        return super(EgadsData, self).__imul__(other).view(EgadsData)

    def __rmul__(self, other):
        return super(EgadsData, self).__rmul__(other).view(EgadsData)


    def copy(self):
        """
        Generate and return a copy of the current EgadsData instance.
        """

        var_copy = EgadsData(super(EgadsData, self).copy())
        var_copy.__dict__ = self.__dict__.copy()
        var_copy.metadata = self.metadata.copy()

        return var_copy


    def rescale(self, units):
        """
        Return a copy of the variable rescaled to the provided units.
        
        :param string units:
            String representation of desired units.
        """
        units = _validate_units(units)
        return super(EgadsData, self).rescale(units).view(EgadsData)

    def print_description(self):
        """
        Generate and return a description of current EgadsData instance.

        """

        outstr = self._get_description()

        print outstr


    def get_units(self):
        """
        Return units used in current EgadsData instance.

        """

        return self.units


    def print_shape(self):
        """
        Prints shape of current EgadsData instance
        """

        print self._get_shape()


    def _get_description(self):
        """
        Generate description of current EgadsData instance.

        """

        outstr = ('Current variable is %i with units of %s. \n' % (self.value.shape, self.units) +
                  'Its descriptive name is: %s and its CF name is: %s\n' % (self.long_name, self.standard_name))

        return outstr


    def _get_shape(self):
        """
        Get shape of current EgadsData instance.

        """

        return self.value.shape


    @classmethod
    def _get_instances(cls):
        """
        Generator which returns currently defined instances of EgadsData.

        """

        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst




class EgadsAlgorithm(object):
    """
    EGADS algorithm base class. All egads algorithms should inherit this class.

    The EgadsAlgorithm class provides base methods for algorithms in EGADS and
    initializes algorithm attributes.

    """

    def __init__(self, return_Egads=True):
        """
        Initializes EgadsAlgorithm instance with None values for all standard
        attributes.

        Constructor Variables
    
        :param bool return_Egads: Optional - 
            Flag used to configure which object type will be returned by the current
            EgadsAlgorithm. If ``true`` an :class: EgadsData instance with relevant
            metadata will be returned by the algorithm, otherwise an array or
            scalar will be returned.
        """
        self.name = self.__class__.__name__

        self.return_Egads = return_Egads

        self.metadata = None
        self.output_metadata = None

        self._output_fields = ['name', 'units', 'long_name', 'standard_name',
            'fill_value', 'valid_range', 'sampled_rate',
            'category', 'calibration_coeff', 'dependencies']

        self.output_properties = {}

        for key in self._output_fields:
            self.output_properties[key] = None

    def run(self, *args):
        """
        Basic run method. This method should be called from EgadsAlgorithm children,
        passing along the correct inputs to the _call_algorithm method.
        
        :param *args:
            Parameters to pass into algorithm in the order specified in algorithm metadata.

        """

        if not isinstance(self.output_metadata, list):
            output_metadata = self.output_metadata
            self.output_metadata = []
            self.output_metadata.append(output_metadata)

        for metadata in self.output_metadata:
            for key, value in metadata.iteritems():
                    try:
                        match = re.compile('input[0-9]+').search(value)
                        while match:
                            input = metadata.get(key)[match.start():match.end()]
                            input_index = int(input.strip('input'))

                            if isinstance(args[input_index], EgadsData):
                                metadata[key] = metadata[key].replace(input, args[input_index].metadata.get(key, ''))
                            else:
                                metadata[key] = metadata[key].replace(input, '')

                            match = re.compile('input[0-9]+').search(metadata[key ])
                    except TypeError:
                        match = None

        output = self._call_algorithm(*args)
        if len(self.metadata['Outputs']) > 1:
            result = []
            for i, value in enumerate(output):
                self.output_metadata[i].set_parent(self.metadata)
                result.append(self._return_result(value, self.output_metadata[i]))
            result = tuple(result)
        else:
            self.output_metadata[0].set_parent(self.metadata)
            result = self._return_result(output, self.output_metadata[0])


        return result

    def _none_units_check(self, *args):

        try:
            for i, value in enumerate(self.output_metadata):
                if self.output_metadata[i]['units'] is None:
                    self.output_metadata[i]['units'] = args[i].get('units', '')
        except TypeError:
            if self.output_metadata['units'] is None:
                self.output_metadata[i]['units'] = args.get('units', '')



    def _return_result(self, value, metadata):

        if self.return_Egads is True:
            result = EgadsData(value, metadata)
        else:
            result = value


        return result


    def _call_algorithm(self, *args):
        """
        Does check on arguments to pass to algorithm.

        If arguments are EgadsData instances, a check is done for expected units.
        Then the numeric value is passed to the algorithm. If argument is not
        EgadsData instance, units are assumed to be correct, and numeric value
        is passed to algorithm.

        """

        out_arg = []

        for i, arg in enumerate(args):
            if isinstance(arg, EgadsData):
                required_units = self.metadata['InputUnits'][i]
                if required_units is not None:
                    required_units = _validate_units(required_units)

                    to_dims = pq.quantity.validate_dimensionality(required_units)
                    to_temps = []
                    for to_unit in to_dims.iterkeys():
                        if isinstance(to_unit, pq.UnitTemperature):
                            to_temps.append(to_unit)

                    from_temps = []
                    for from_unit in arg._dimensionality.iterkeys():
                        if isinstance(from_unit, pq.UnitTemperature):
                            from_temps.append(from_unit)

                    for from_temp, to_temp in zip(from_temps, to_temps):
                        if from_temp._dimensionality != to_temp._dimensionality:
                            warnings.warn("Unsupported conversion between temperature types." +
                                             "'%s' given, '%s' expected."
                                             % (from_temp._dimensionality.string, to_temp._dimensionality.string),
                                             UserWarning)
    #                        raise ValueError("Unsupported conversion between temperature types." +
    #                                         "'%s' given, '%s' expected."
    #                                         % (from_temp._dimensionality.string, to_temp._dimensionality.string)
    #                                         ) #TODO Define error for temperature mismatch

                    arg_corr = arg.rescale(required_units)


                    out_arg.append(arg_corr.value)
                else:
                    out_arg.append(arg.value)
            else:
                out_arg.append(numpy.array(arg))

        result = self._algorithm(*out_arg)



        self.time_stamp()

        return result

    def _algorithm(self):
        """
        Skeleton algorithm method. Must be defined in EgadsAlgorithm children.

        """

        raise AssertionError('Algorithm not implemented')


    def get_info(self):
        """
        Print docstring of algorithm to standard output. 
        
        """

        print self.__doc__

    def time_stamp(self):
        """
        Calculate and set date processed for all output variables.
        """

        for output in self.output_metadata:
                output['DateProcessed'] = self.now()

    def now(self):
        """
        Calculate and return current date/time in ISO 8601 format.
        """

        return datetime.datetime.isoformat(datetime.datetime.today())

    def _populate_data_object(self, value, metadata):
        """
        Method for automatically populating new EgadsData instance 
        with calculated value and algorithm/variable metadata.
        
        
        """

        result = EgadsData(value, metadata)

        for key, val in self.output_properties.iteritems():
            result.__setattr__(key, val)


        return result

def _validate_units(units):
    """
    Function to pre-validate units to be passed into Quantities for comprehension.
    
    Corrects string units which are written without carets or multiplication symbols:
    'kg m-3' becomes 'kg*m^-3'
    
    In quantities 0.10.1, the '%' symbol is not correctly recognized. Thus corrects
    the '%' symbol to 'percent'.
    
    In quantities, the time unit 'time since ...' is not correctly recognized. Thus
    corrects the 'time since ...' to 'time'.
    """
    
    # few patches have been introduced for compatibility"
    if "degree_" in units or "decimal degree" in units:
        units = "degree"
    if units == "-":
        units = ""
    if " since " in units:
        units = units[:units.index(" since ")]
        
    if " / " in units:
        units = units[:units.index(" / ")] + "/" + units[units.index(" / ")+3:]
    if isinstance(units, str) or isinstance(units, unicode):
        
        regex = re.compile('(?<=[A-Za-z])[0-9-]')
        match = regex.search(units)
        while match is not None:
            units = units[:match.start()] + "^" + units[match.start():]
            match = regex.search(units)
        regex_space = re.compile('[ ]+')
        units = regex_space.sub('*', units)
        if '%' in units:
            units = units.replace('%', 'percent')
    
    return units


def _add_new_units():
    """
    Function to add units which are not natively present in Quantities but are
    important for airborne research.
    """

    pq.UnitQuantity('microgram', pq.milligram/1e6, symbol='ug', aliases=['micrograms'])


__author__ = "mfreer"
__date__ = "2012-07-06 17:42"
__version__ = "1.6"
__all__ = ["EgadsData", "EgadsAlgorithm"]

import logging
import weakref
import datetime
import re
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
        logging.debug('egads - egads_core.py - EgadsData - __new__')
        if isinstance(units, metadata.VariableMetadata):
            if not variable_metadata:
                variable_metadata = units
            units = units.get('units', '')
        if variable_metadata and (not units):
            units = variable_metadata.get('units', '')
            if not units:
                units = variable_metadata.get('Units', '')
        
        # quantities can't handle the CF time unit 'time since epoch'
        # to allow a proper operation of EGADS, a new attribute has been added,
        # transparent to the user, if the epoch is needed.
        true_units = None
        if ' since ' in units or 'after' in units:
            true_units = units
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
        if true_units:
            ret.metadata['units'] = true_units
        else:
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
        
        try:
            logging.debug('egads - egads_core.py - EgadsData __init__ - value [' + str(value[0]) + ' ... ' + 
                          str(value[-1]) + '], units ' + str(units) + ', variale_metadata ' + 
                          str(variable_metadata) + ', dtype' + str(dtype))
        except (IndexError, TypeError):
            logging.exception('egads - egads_core.py - EgadsData - __init__ - value [' + str(value) + '], units ' +
                           str(units) + ', variale_metadata ' + str(variable_metadata) + ', dtype' + 
                           str(dtype))
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

    def __getitem__(self, other):
        metadata = None
        try:
            metadata = self.metadata.copy()
        except AttributeError:
            pass
        out = super(EgadsData, self).__getitem__(other).view(EgadsData)
        if metadata:
            out.metadata = metadata
        return out

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

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
        
        logging.debug('egads - egads_core.py - EgadsData - copy - metadata %s', self.metadata)
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
        
        logging.debug('egads - egads_core.py - EgadsData - rescale - units %s to %s', self.units, units)
        units = _validate_units(units)
        metadata = None
        try:
            metadata = self.metadata.copy()
        except AttributeError:
            pass
        out = super(EgadsData, self).rescale(units).view(EgadsData)
        if metadata:
            out.metadata = metadata
        try:
            long_units = max(getattr(pq, out.units)._aliases, key=len)
            if ' since ' in out.metadata['units']:
                true_units = str(long_units) + out.metadata['units'][out.metadata['units'].index(' since '):]
                out.metadata['units'] = true_units
            else:
                out.metadata['units'] = long_units
        except (AttributeError, KeyError, ValueError):
            pass
        return out

    def print_description(self):
        """
        Generate and return a description of current EgadsData instance.
        """
        
        logging.debug('egads - egads_core.py - EgadsData - print_description - ' +  self._get_description())
        outstr = self._get_description()
        print outstr

    def get_units(self):
        """
        Return units used in current EgadsData instance.
        """

        logging.debug('egads - egads_core.py - EgadsData - get_units - ' +  self.units)
        return self.units

    def print_shape(self):
        """
        Prints shape of current EgadsData instance
        """

        logging.debug('egads - egads_core.py - EgadsData - print_shape - ' +  str(self._get_shape()))
        print self._get_shape()

    def _get_description(self):
        """
        Generate description of current EgadsData instance.
        """

        shape = str(self.value.shape)
        units = str(self.units)
        try:
            long_name = self.metadata['long_name']
        except KeyError:
            long_name = 'no_long_name'
        try:
            standard_name = self.metadata['standard_name']
        except KeyError:
            standard_name = 'no_standard_name'

        outstr = ('Current variable is %s with units of %s. \n' % (shape, units) +
                  'Its descriptive name is: %s and its CF name is: %s\n' % (long_name, standard_name))
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


    logging.info('egads - egads_core.py - EgadsData has been loaded')


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
        
        logging.debug('egads - egads_core.py - EgadsAlgorithm - __init__ - return_egads ' +  str(return_Egads))
        self.name = self.__class__.__name__
        self.return_Egads = return_Egads
        self.metadata = None
        self.output_metadata = None
        self._output_fields = ['name', 'units', 'long_name', 'standard_name', 'fill_value',
                               'valid_range', 'sampled_rate', 'category', 'calibration_coeff',
                               'dependencies']
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
        
        logging.debug('egads - egads_core.py - EgadsAlgorithm - run - name ' + self.name + ', args ' + str(args)) 
        if not isinstance(self.output_metadata, list):
            output_metadata = self.output_metadata
            self.output_metadata = []
            self.output_metadata.append(output_metadata)
        for metadata in self.output_metadata:
            for key, value in metadata.iteritems():
                try:
                    match = re.compile('input[0-9]+').search(value)
                    while match:
                        input_seq = metadata.get(key)[match.start():match.end()]
                        input_index = int(input_seq.strip('input'))
                        
                        if isinstance(args[input_index], EgadsData):
                            metadata[key] = metadata[key].replace(input_seq, args[input_index].metadata.get(key, ''))
                        else:
                            metadata[key] = metadata[key].replace(input_seq, '')
                        match = re.compile('input[0-9]+').search(metadata[key])
                except TypeError:
                    match = None
                try:
                    if key == 'Category':
                        if value == ['']:
                            out_category = []
                            for arg in args:
                                if isinstance(arg, EgadsData):
                                    out_category.append(arg.metadata[key])
                            metadata[key] = out_category
                except KeyError:
                    pass
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
            for i, _ in enumerate(self.output_metadata):
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

        logging.debug('egads - egads_core.py - EgadsAlgorithm - _call_algorithm')
        out_arg = []
        for i, arg in enumerate(args):
            if isinstance(arg, EgadsData):
                required_units = self.metadata['InputUnits'][i]
                if required_units is not None:
                    arg_corr = arg
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
                            if 'degC' in str(from_temp) and 'K' in str(to_temp):
                                arg_corr = arg_corr + EgadsData(value=273.15, units=from_temp)
                            elif 'K' in str(from_temp) and 'degC' in str(to_temp):
                                arg_corr = arg_corr - EgadsData(value=273.15, units=from_temp)
                            else:
                                pass
                    arg_corr = arg_corr.rescale(required_units)
                    out_arg.append(arg_corr.value)
                else:
                    out_arg.append(arg.value)
            else:
                out_arg.append(numpy.array(arg))
        result = self._algorithm(*out_arg)
        self.time_stamp()
        self.processor()
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
        
        logging.debug('egads - egads_core.py - EgadsAlgorithm - get_info')
        print self.__doc__

    def time_stamp(self):
        """
        Calculate and set date processed for all output variables.
        """
        
        logging.debug('egads - egads_core.py - EgadsAlgorithm - time_stamp.')
        for output in self.output_metadata:
                output['DateProcessed'] = self.now()

    def now(self):
        """
        Calculate and return current date/time in ISO 8601 format.
        """
        
        logging.debug('egads - egads_core.py - EgadsAlgorithm - now - time_stamp ' + datetime.datetime.isoformat(datetime.datetime.today()))
        return datetime.datetime.isoformat(datetime.datetime.today())
    
    def processor(self):
        """
        Indicate the algorithm used to produce the output variable
        """
        logging.debug('egads - egads_core.py - EgadsAlgorithm - processor')
        for output in self.output_metadata:
                output['Processor'] = self.metadata['Processor']

    def _populate_data_object(self, value, metadata):
        """
        Method for automatically populating new EgadsData instance 
        with calculated value and algorithm/variable metadata.
        """

        result = EgadsData(value, metadata)
        for key, val in self.output_properties.iteritems():
            result.__setattr__(key, val)
        return result
    
    logging.info('egads - egads_core.py - EgadsAlgorithm has been loaded')


def _validate_units(units):
    """
    Function to pre-validate units to be passed into Quantities for comprehension.
    
    Corrects string units which are written without carets or multiplication symbols:
    'kg m-3' becomes 'kg*m^-3'
    
    In quantities 0.10.1+, the '%' symbol is not correctly recognized. Thus corrects
    the '%' symbol to 'percent'.
    
    In few atmospheric measurement dataset, '0.01' can be used to represent '%'. Thus
    corrects the '0.01' symbol to 'percent'.
    
    In few atmospheric measurement dataset, dimensionless data based on event have their
    units equal to '1'. Thus corrects the '1' to 'dimensionless'.
    
    In quantities, the time unit 'time since ...' is not correctly recognized. Thus
    corrects the 'time since ...' to 'time'.
    """

    logging.debug('egads - egads_core.py - _validate_units - units ' + str(units))
    
    # few patches have been introduced for compatibility"
    if "degree_" in units or "decimal degree" in units:
        units = "degree"
    if units == "-":
        units = ""
    if " since " in units:
        units = units[:units.index(" since ")]
    if " after " in units:
        units = units[:units.index(" after ")]
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
        if units == '1':
            units = 'dimensionless'
        if units == '0.01':
            units = 'percent'
    return units


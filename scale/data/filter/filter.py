"""Defines the class for filtering data"""
from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from data.filter.exceptions import InvalidDataFilter
from storage.models import ScaleFile

logger = logging.getLogger(__name__)

FILE_TYPES = {'filename', 'media-type'}

STRING_TYPES = {'string', 'filename', 'media-type'}

STRING_CONDITIONS = {'==', '!=', 'in', 'not in', 'contains'}

NUMBER_TYPES = {'integer', 'number'}

NUMBER_CONDITIONS = {'<', '<=', '>','>=', '==', '!=', 'between', 'in', 'not in'}

BOOL_TYPES = {'boolean'}

BOOL_CONDITIONS = {'==', '!='}


def _less_than(input, values):
    """Checks if the given input is < the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input < values[0]
    except IndexError:
        return False

def _less_than_equal(input, values):
    """Checks if the given input is <= the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input <= values[0]
    except IndexError:
        return False

def _greater_than(input, values):
    """Checks if the given input is > the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input > values[0]
    except IndexError:
        return False

def _greater_than_equal(input, values):
    """Checks if the given input is >= the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input >= values[0]
    except IndexError:
        return False

def _equal(input, values):
    """Checks if the given input is equal to the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input == values[0]
    except IndexError:
        return False

def _not_equal(input, values):
    """Checks if the given input is not equal to the first value in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input != values[0]
    except IndexError:
        return False

def _between(input, values):
    """Checks if the given input is between the first two values in the list

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    try:
        return input >= values[0] and input <= values[1]
    except IndexError:
        return False

def _in(input, values):
    """Checks if the given input is in the list of values, or is a subset of a value

    :param input: The input to check
    :type input: int/float
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    if input in values:
        return True
    for value in values:
        if input in value:
            return True
    return False
    
def _not_in(input, values):
    """Checks if the given input is not in the list of values and is not a subset of a value

    :param input: The input to check
    :type input: int/float/string
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    if input in values:
        return False
    for value in values:
        if input in value:
            return False
    return True

def _contains(input, values):
    """Checks if the given input contains a value from the given list

    :param input: The input to check
    :type input: string/list
    :param values: The values to check
    :type values: list
    :returns: True if the condition check passes, False otherwise
    :rtype: bool
    """

    for value in values:
        if value in input:
            return True
    return False


ALL_CONDITIONS = {'<': _less_than, '<=': _less_than_equal, '>': _greater_than,'>=': _greater_than_equal,
                  '==': _equal, '!=': _not_equal, 'between': _between, 'in': _in, 'not in': _not_in, 'contains': _contains}

class DataFilter(object):
    """Represents a filter that either accepts or denies a set of data values
    """

    def __init__(self, filters, all=True):
        """Constructor

        :param filters: Filters to determine whether to accept or deny data
        :type filters: dict
        :param all: Whether all filters need to pass to accept data
        :type filters: boolean
        """

        # TODO: there are a number of unit tests that will need to have real DataFilters created instead of
        # DataFilter(True) or DataFilter(False)

        # TODO: after implementing this class, implement recipe.definition.node.ConditionNodeDefinition.__init__
        self.filters = filters
        self.all = all

    def add_filter(self, name, type, condition, values):
        """Adds a condition node to the recipe graph

        :param name: Name of the data value to compare against
        :type name: string
        :param type: The type of the data value being compared
        :type type: string
        :param condition: The condition to test (<, >, ==, between, contains, etc)
        :type condition: string
        :param values: The values to compare for the condition
        :type values: list

        :raises :class:`recipe.definition.exceptions.InvalidDefinition`: If the node is duplicated
        """

        if not name:
            raise InvalidDataFilter('MISSING_NAME', 'Missing name for filter')

        if not type:
            raise InvalidDataFilter('MISSING_TYPE', 'Missing type for \'%s\'' % name)

        if not condition:
            raise InvalidDataFilter('MISSING_CONDITION', 'Missing condition for \'%s\'' % name)

        if condition not in ALL_CONDITIONS:
            raise InvalidDataFilter('INVALID_CONDITION', 'Invalid condition \'%s\' for \'%s\'. Valid conditions are: %s'
                                    % (condition, name, ALL_CONDITIONS))

        if type in STRING_TYPES and condition not in STRING_CONDITIONS:
            raise InvalidDataFilter('INVALID_CONDITION', 'Invalid condition \'%s\' for \'%s\'. Valid conditions are: %s'
                                    % (condition, name, STRING_CONDITIONS))

        if type in NUMBER_TYPES and condition not in NUMBER_CONDITIONS:
            raise InvalidDataFilter('INVALID_CONDITION', 'Invalid condition \'%s\' for \'%s\'. Valid conditions are: %s'
                                    % (condition, name, NUMBER_CONDITIONS))

        if type in BOOL_TYPES and condition not in BOOL_CONDITIONS:
            raise InvalidDataFilter('INVALID_CONDITION', 'Invalid condition \'%s\' for \'%s\'. Valid conditions are: %s'
                                    % (condition, name, BOOL_CONDITIONS))
        if not values:
            raise InvalidDataFilter('MISSING_VALUES', 'Missing values for \'%s\'' % name)

        filter_values = []
        if type == 'number':
            for value in values:
                try:
                    filter_values.append(float(value))
                except ValueError:
                    raise InvalidDataFilter('VALUE_ERROR', 'Expected float for \'%s\', found %s' % (name, value))
        elif type == 'integer':
            for value in values:
                try:
                    filter_values.append(int(value))
                except ValueError:
                    raise InvalidDataFilter('VALUE_ERROR', 'Expected int for \'%s\', found %s' % (name, value))
        else:
            filter_values.extend(values)

        self.filters.append({'name': name, 'type': type, 'condition': condition, 'values': filter_values})

    def is_data_accepted(self, data):
        """Indicates whether the given data passes the filter or not

        :param data: The data to check against the filter
        :type data: :class:`data.data.data.Data`
        :returns: True if the data is accepted, False if the data is denied
        :rtype: bool
        """

        success = True
        for filter in self.filters:
            name = filter['name']
            type = filter['type']
            cond = filter['condition']
            values = filter['values']
            filter_success = True
            if name in data.values:
                param = data.values[name]
                try:
                    if type == 'filename':
                        filenames = [scale_file.file_name for scale_file in ScaleFile.objects.filter(id__in=param.file_ids)]
                        for filename in filenames:
                            filter_success |= ALL_CONDITIONS[cond](filename, values)
                    if type == 'media-type':
                        media_types = [scale_file.media_type for scale_file in ScaleFile.objects.filter(id__in=param.file_ids)]
                        filter_success &= ALL_CONDITIONS[cond](media_types, values)
                except AttributeError:
                    logger.error('Attempting to run file filter on json parameter or vice versa')
                    success = False
                except KeyError:
                    logger.error('Condition %s does not exist' % cond)
                    success = False
                except ScaleFile.DoesNotExist:
                    logger.error('Attempting to run file filter on non-existant file(s): %d' % param.file_ids)
                    success = False
            if success and not self.all:
                return True # One filter passed, so return True
        return success

    def is_filter_equal(self, data_filter):
        """Indicates whether the given data filter is equal to this filter or not

        :param data_filter: The data filter
        :type data_filter: :class:`data.filter.filter.DataFilter`
        :returns: True if the data filter is equal to this one, False otherwise
        :rtype: bool
        """

        equal = self.all == data_filter.all
        equal &= self.filters == data_filter.filters
        
        return equal

    def validate(self, interface):
        """Validates this data filter against the given interface

        :param interface: The interface describing the data that will be passed to the filter
        :type interface: :class:`data.interface.interface.Interface`
        :returns: A list of warnings discovered during validation
        :rtype: list

        :raises :class:`data.filter.exceptions.InvalidDataFilter`: If the data filter is invalid
        """

        warnings = []

        # TODO: implement

        return warnings

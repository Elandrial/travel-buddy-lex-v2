from datetime import datetime, date
import dateutil.parser

import lex_v2
import utility

"""
The core methods for validating data, often these are passed by reference for intent slots
"""


def isvalid_number(value):
    if isinstance(value, int) or isinstance(value, float):
        return True
    elif isinstance(value, str):
        return value.isnumeric()
    else:
        return False


def isvalid_num_range(value, min_value, max_value):
    if isvalid_number(value) and isvalid_number(min_value) and isvalid_number(max_value):
        num_value = utility.safe_int(value)
        return min_value <= num_value <= max_value
    return False


def isvalid_in_array(value, array):
    if value and array:
        if isinstance(value, str):
            return value.lower() in array
        else:
            return value in array
    return False


def isvalid_boolean(value):
    return isvalid_in_array(value, ['yes', 'no', 'sure', 'nope', 'never', 'positive', 'negative', 'nay', 'true', 'false'])


def isvalid_date(date_value):
    val_date = utility.convert_to_date(date_value)
    if val_date:
        return True
    else:
        return False


def isvalid_date_beyond(value, date_value):
    beyond_date = utility.convert_to_date(value)
    compare_date = utility.convert_to_date(date_value)

    if beyond_date and compare_date:
        return beyond_date > compare_date
    else:
        return False

"""
Dynamic validation performance, takes a function reference and determines what values it needs to pass it, 
to validate a value
"""
def do_validate(validation_fn, value, dynamic_values):
    if 'val1' in dynamic_values:
        slot1_value = dynamic_values['val1']
    elif 'val1' in validation_fn:
        slot1_value = validation_fn['val1']

    if 'val2' in dynamic_values:
        slot2_value = dynamic_values['val2']
    elif 'val2' in validation_fn:
        slot2_value = validation_fn['val2']

    if 'val1' in validation_fn and 'val2' in validation_fn:
        return validation_fn['fn'](value, slot1_value, slot2_value)
    elif 'val1' in validation_fn:
        return validation_fn['fn'](value, slot1_value)
    else:
        return validation_fn['fn'](value)


# maps slot values from Lex to keywords, used when one slot field depends on the value of another
def map_validation(slots, validation_fn):
    dynamic_values = {}

    # handle dynamically populated values that depend on other slots
    if 'val1' in validation_fn and isinstance(validation_fn['val1'], str):
        if 'slot:' in validation_fn['val1']:
            dynamic_values['val1'] = lex_v2.get_slot_value(lex_v2.get_slot_from_slots(slots, validation_fn['val1'][5:]))
    if 'val2' in validation_fn and isinstance(validation_fn['val2'], str):
        if 'slot:' in validation_fn['val2']:
            dynamic_values['val2'] = lex_v2.get_slot_value(lex_v2.get_slot_from_slots(slots, validation_fn['val2'][5:]))

    return dynamic_values

import datetime

from context import validation
import validation


def test_validation():
    # isvalid_number
    assert validation.isvalid_number(123)
    assert validation.isvalid_number("1")
    assert not validation.isvalid_number("asd")

    # isvalid_num_range(value, min_value, max_value)
    assert validation.isvalid_num_range(5, 1, 10)
    assert validation.isvalid_num_range(5, 5, 10)
    assert validation.isvalid_num_range(5, 1, 5)
    assert not validation.isvalid_num_range(50, 5, 10)
    assert validation.isvalid_num_range(5, 1, 10)
    assert not validation.isvalid_num_range('a', 1, 10)

    # isvalid_in_array(value, array)
    assert validation.isvalid_in_array(1, [1, 2, 3, 4, 5])
    assert validation.isvalid_in_array('apple', ['fruit', 'apple', '3', '4', '5'])
    assert not validation.isvalid_in_array('aple', ['fruit', 'apple', '3', '4', '5'])

    # isvalid_boolean(value)
    assert validation.isvalid_boolean('yes')
    assert validation.isvalid_boolean('no')
    assert not validation.isvalid_boolean('aa')

    # isvalid_date(date)
    assert validation.isvalid_date(datetime.date.today())
    assert validation.isvalid_date('2023-01-01')
    assert not validation.isvalid_date('2023-02-30')
    assert not validation.isvalid_date('test')

    # isvalid_date_beyond(value, date)
    assert validation.isvalid_date_beyond(datetime.date(2023, 1, 2), datetime.date(2023, 1, 1))
    assert validation.isvalid_date_beyond('2023-01-02', datetime.date(2023, 1, 1))
    assert not validation.isvalid_date_beyond(datetime.date(2023, 1, 1), datetime.date(2023, 1, 2))
    assert not validation.isvalid_date_beyond('2023-01-01', datetime.date(2023, 1, 2))
    assert not validation.isvalid_date_beyond('test', datetime.date(2023, 1, 2))
    assert not validation.isvalid_date_beyond('2023-01-01', 'test')

    validation_fn2 = {'fn': validation.isvalid_date_beyond,
                      'val1': 'slot:PickUpDate',
                      'message': 'The return date needs to be after the pickup date.  Can '
                                 'you try a different date?'}
    # map_validation(slots, validation_fn)
    slots = {
        'ReturnDate': {
            'shape': 'Scalar',
            'value': {
                'originalValue': '1st june 2023',
                'resolvedValues': ['2023-06-01'],
                'interpretedValue': '2023-06-01'
            }
        },
        'PickUpDate': {
            'shape': 'Scalar',
            'value': {
                'originalValue': 'tomorrow',
                'resolvedValues': ['2023-04-09'],
                'interpretedValue': '2023-04-09'
            }
        },
        'DriverAge': None,
        'CarType': None,
        'PickUpCity': {
            'shape': 'Scalar',
            'value': {
                'originalValue': 'perth',
                'resolvedValues': ['perth'],
                'interpretedValue': 'perth'
            }
        }
    }
    assert validation.map_validation(slots, validation_fn2) == {'val1': '2023-04-09'}

    # do_validate(validation_fn, value, dynamic_values)
    validation_fn = {'fn': validation.isvalid_in_array,
                     'val1': ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix',
                              'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                              'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte',
                              'detroit', 'el paso', 'seattle', 'denver', 'washington dc', 'memphis', 'boston',
                              'nashville', 'baltimore', 'portland', 'melbourne', 'sydney', 'perth', 'albany',
                              'bunbury'],
                     'message': 'We currently do not support {} as a valid pickup location.  Can you try a '
                                'different city?'}
    assert validation.do_validate(validation_fn, 'perth', {})

    assert validation.do_validate(validation_fn2, '2023-06-01', {'val1': '2023-04-09'})
    assert not validation.do_validate(validation_fn2, '2023-01-01', {'val1': '2023-04-09'})

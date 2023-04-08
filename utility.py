import datetime
import dateutil.parser
from validation import isvalid_number

"""
Utility functions to support validation and data translation
"""

def safe_int(n):
    if n is not None and isvalid_number(n):
        return int(n)
    return None


def get_day_difference(later_date, earlier_date):
    later_datetime = convert_to_date(later_date)
    earlier_datetime = convert_to_date(earlier_date)

    if earlier_datetime and later_datetime:
        return abs(later_datetime - earlier_datetime).days
    else:
        return None


def convert_to_date(date_value):
    output_date = convert_to_datetime(date_value)
    if isinstance(output_date, datetime.datetime):
        output_date = output_date.date()

    return output_date


def convert_to_datetime(datetime_value):
    output_date = None
    if isinstance(datetime_value, str):
        try:
            output_date = dateutil.parser.parse(datetime_value)
        except dateutil.parser.ParserError:
            output_date = None
    elif isinstance(datetime_value, datetime.datetime):
        output_date = datetime_value
    elif isinstance(datetime_value, datetime.date):
        output_date = datetime.datetime.combine(datetime_value, datetime.datetime.min.time())
    return output_date


def add_days(date_value, number_of_days):
    new_date = convert_to_date(date_value)
    new_date += datetime.timedelta(days=number_of_days)
    return new_date.strftime('%Y-%m-%d')

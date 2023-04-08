from context import utility
import utility
import datetime


def test_utility():
    # safe_int(n)
    assert utility.safe_int('5') == 5
    assert utility.safe_int(5) == 5
    assert utility.safe_int('a') is None
    assert utility.safe_int(None) is None

    # get_day_difference(later_date, earlier_date)
    assert utility.get_day_difference(datetime.date.today(), datetime.date.today()) == 0
    assert utility.get_day_difference(datetime.date(2023, 1, 1), datetime.date(2023, 1, 2)) == 1
    assert utility.get_day_difference(datetime.date(2023, 1, 2), datetime.date(2023, 1, 1)) == 1
    assert utility.get_day_difference('2023-01-01', '2023-01-02') == 1
    assert utility.get_day_difference('test', '2023-01-02') is None
    assert utility.get_day_difference('2023-01-02', 'test') is None

    # convert_to_date(date_value)
    assert utility.convert_to_date('2023-01-01 12:00:00') == datetime.date(2023, 1, 1)
    assert utility.convert_to_date(datetime.datetime(2023, 1, 1, 12, 0, 0)) == datetime.date(2023, 1, 1)
    assert utility.convert_to_date('2023-01-01') == datetime.date(2023, 1, 1)
    assert utility.convert_to_date('test') is None

    # convert_to_datetime(datetime_value)
    assert utility.convert_to_datetime('2023-01-01 12:00:00') == datetime.datetime(2023, 1, 1, 12, 0, 0)
    assert utility.convert_to_datetime(datetime.datetime(2023, 1, 1, 12, 0, 0)) == datetime.datetime(2023, 1, 1, 12, 0, 0)
    assert utility.convert_to_datetime('2023-01-01') == datetime.datetime(2023, 1, 1, 0, 0, 0)
    assert utility.convert_to_datetime('test') is None

    # add_days(date_value, number_of_days)
    assert utility.add_days('2023-01-01', 2) == datetime.date(2023, 1, 3).strftime('%Y-%m-%d')
    assert not utility.add_days('2023-01-01', 2) == datetime.date(2023, 1, 2).strftime('%Y-%m-%d')

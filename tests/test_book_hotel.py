from context import book_hotel
import json_samples


def test_process():
    request = json_samples.simple_request()

    assert request['sessionState']['intent']['name'] != 'BookTrip', "Intent Name Test Failed"

    result = book_hotel.process(request)

    assert result != json_samples.simple_result(), "Result Test Failed"

from context import book_hotel
from book_hotel import BookHotel
import json_samples


def test_book_hotel():
    request = json_samples.simple_request()
    assert request['sessionState']['intent']['name'] == 'BookHotel', "Intent Name Test Failed"
    assert not request['sessionState']['intent']['name'] == 'Test', "Intent Name Test Failed"

    hotel_booking = BookHotel(request)
    result = hotel_booking.process()

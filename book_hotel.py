import datetime
import json
import utility
import lex_v2
import logging

import validation
from intent import Intent

# provides the configuration setup for validation of slots
hotel_slots = [{'slotName': 'Location',
                'name': 'Location',
                'validation': [{'fn': validation.isvalid_in_array,
                                'val1': ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix',
                                         'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                                         'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte',
                                         'detroit',
                                         'el paso', 'seattle', 'denver', 'washington dc', 'memphis', 'boston',
                                         'nashville',
                                         'baltimore', 'portland', 'melbourne', 'sydney', 'perth', 'albany', 'bunbury'],
                                'message': 'We currently do not support {} as a valid destination.  Can you try a '
                                           'different city?'}]
                },
               {
                   'slotName': 'CheckInDate',
                   'name': 'Check in date',
                   'validation': [{'fn': validation.isvalid_date,
                                   'message': 'I did not understand your check in date.  When would you like to check '
                                              'in?'},
                                  {'fn': validation.isvalid_date_beyond,
                                   'val1': datetime.date.today(),
                                   'message': 'Reservations must be scheduled at least one day in advance.  Can '
                                              'you try a different date?'}]
               },
               {
                   'slotName': 'Nights',
                   'name': 'Nights',
                   'validation': [{'fn': validation.isvalid_num_range,
                                   'val1': 1,
                                   'val2': 30,
                                   'message': 'You can make a reservations for from one to thirty nights.  How many '
                                              'nights would you like to stay for?'}]
               },
               {
                   'slotName': 'RoomType',
                   'name': 'Room Type',
                   'validation': [{'fn': validation.isvalid_in_array,
                                   'val1': ['queen', 'king', 'deluxe'],
                                   'message': 'I did not recognize that room type.  Would you like to stay in a '
                                              'queen, king, or deluxe room?'}]
               },
               {
                   'slotName': 'BreakfastIncluded',
                   'name': 'Breakfast Included',
                   'validation': [{'fn': validation.isvalid_boolean,
                                   'message': "Sorry I didn't understand your answer, did you want to include "
                                              "breakfast with your accommodation?"}]
               }
               ]


class BookHotel(Intent):
    """
    Handles the Lex Intent BookHotel, inherits from Intent which provides most of the logic
    """
    def __init__(self, intent_request):
        Intent.__init__(self, intent_request, hotel_slots, 'Hotel Booking')

    """
    Fires once all data has been entered and validated. Calculates a price based on the inputted values
    """
    def on_data_completed(self, reservation, session_attributes):
        location = reservation['Location']
        room_type = reservation['RoomType']
        checkin_date = reservation['CheckInDate']
        nights = reservation['Nights']
        breakfast_included = reservation['BreakfastIncluded']

        # The price of the hotel has yet to be confirmed.
        price = self.generate_hotel_price(location, nights, room_type, breakfast_included)
        session_attributes['currentReservationPrice'] = price
        message = 'OK, I have you down for a {} room with a {} night stay in {} starting {},  ' \
                  'Breakfast: {}. Total price: {}'.format(room_type, nights, location,
                                                          checkin_date, breakfast_included, price)
        # TODO: find out why this doesn't work? Wrong message to Lex v2?
        # return lex_v2.confirm_intent(intent_request, session_attributes,
        #                             intent_request['sessionState']['intent']['slots'], message)
        return message

    """
    Generates a number within a reasonable range that might be expected for a car.
    The price also takes into consideration being a young driver
    """
    def generate_hotel_price(self, location, nights, room_type, breakfast_included):
        """
        Generates a number within a reasonable range that might be expected for a hotel.
        The price is fixed for a pair of location and roomType.
        """

        room_types = ['queen', 'king', 'deluxe']
        cost_of_living = 0
        cost_of_breakfast = 0

        if breakfast_included.lower() == 'yes':
            cost_of_breakfast = 15

        for i in range(len(location)):
            cost_of_living += ord(location.lower()[i]) - 97

        return nights * (100 + cost_of_breakfast + cost_of_living + (100 + room_types.index(room_type.lower())))

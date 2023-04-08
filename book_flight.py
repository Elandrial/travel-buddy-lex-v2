import datetime
import json
import utility
import lex_v2
import logging

import validation
from intent import Intent

flight_slots = [{'slotName': 'LocationFrom',
                 'name': 'Departure City',
                 'validation': [{'fn': validation.isvalid_in_array,
                                 'val1': ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix',
                                          'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                                          'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte',
                                          'detroit', 'el paso', 'seattle', 'denver', 'washington dc', 'memphis',
                                          'boston',
                                          'nashville', 'baltimore', 'portland', 'melbourne', 'sydney', 'perth',
                                          'albany',
                                          'bunbury'],
                                 'message': 'We currently do not support {} as a valid departure location.  Can you '
                                            'try a different city?'}]
                 },
                {
                    'slotName': 'LocationTo',
                    'name': 'Arrival City',
                    'validation': [{'fn': validation.isvalid_in_array,
                                    'val1': ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix',
                                             'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                                             'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte',
                                             'detroit', 'el paso', 'seattle', 'denver', 'washington dc', 'memphis',
                                             'boston',
                                             'nashville', 'baltimore', 'portland', 'melbourne', 'sydney', 'perth',
                                             'albany',
                                             'bunbury'],
                                    'message': 'We currently do not support {} as a valid departure location.  Can you '
                                               'try a different city?'},
                                   {'fn': (lambda a, b: a != b),
                                    'val1': 'slot:LocationFrom',
                                    'message': 'You have entered the same departure and arrival location.  Can you '
                                               'try a different arrival city?'}
                                   ]
                },
                {
                    'slotName': 'DepartureDate',
                    'name': 'Departure date',
                    'validation': [{'fn': validation.isvalid_date,
                                    'message': 'I did not understand your departure date.  When would you like '
                                               'to fly out?'},
                                   {'fn': validation.isvalid_date_beyond,
                                    'val1': datetime.date.today(),
                                    'message': 'Reservations must be scheduled at least one day in advance.  Can '
                                               'you try a different date?'}]
                },
                {
                    'slotName': 'ReturnDate',
                    'name': 'Return date',
                    'validation': [{'fn': validation.isvalid_date,
                                    'message': 'I did not understand your return date.  When would you like to return?'},
                                   {'fn': validation.isvalid_date_beyond,
                                    'val1': 'slot:DepartureDate',
                                    'message': 'The return date needs to be after the departure date.  Can '
                                               'you try a different date?'}]
                },
                {
                    'slotName': 'CabinClass',
                    'name': 'Cabin Class',
                    'validation': [{'fn': validation.isvalid_in_array,
                                    'val1': ['economy', 'business', 'first class'],
                                    'message': "Sorry I didn't recognise that class. Would you like Economy, "
                                               "Business or First Class?"}]
                }]


class BookFlight(Intent):
    def __init__(self, intent_request):
        Intent.__init__(self, intent_request, flight_slots, 'Flight Booking')

    def on_data_completed(self, reservation, session_attributes):
        location_from = reservation['LocationFrom']
        location_to = reservation['LocationTo']
        departure_date = reservation['DepartureDate']
        return_date = reservation['ReturnDate']
        cabin_class = reservation['CabinClass']

        # The price of the hotel has yet to be confirmed.
        price = self.generate_flight_price(location_from, location_to, departure_date, return_date, cabin_class)
        session_attributes['currentReservationPrice'] = price
        message = 'OK, I have you down for a flight in {} from {} to {}, departing on the {} and returning on the {}. ' \
                  'Total price: {}'.format(cabin_class, location_from, location_to, departure_date,
                                           return_date, price)
        # TODO: find out why this doesn't work? Wrong response to Lex v2?
        # return lex_v2.confirm_intent(intent_request, session_attributes,
        #                             intent_request['sessionState']['intent']['slots'], message)
        return message

    def generate_flight_price(self, pickup_city, pickup_date, return_date, driver_age, car_type):
        """
        Generates a number within a reasonable range that might be expected for a flight.
        """

        class_types = ['economy', 'business', 'first class']
        cost_of_living = 0

        for i in range(len(pickup_city)):
            cost_of_living += ord(pickup_city.lower()[i]) - 97

        return 2 * (100 + cost_of_living + (100 * (1+ class_types.index(class_types.lower()))))

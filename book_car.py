import datetime
import json
import utility
import lex_v2
import logging

import validation
from intent import Intent

# provides the configuration setup for validation of slots
car_slots = [{'slotName': 'PickUpCity',
              'name': 'Pickup City',
              'validation': [{'fn': validation.isvalid_in_array,
                              'val1': ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix',
                                       'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                                       'san francisco', 'indianapolis', 'columbus', 'fort worth', 'charlotte',
                                       'detroit', 'el paso', 'seattle', 'denver', 'washington dc', 'memphis', 'boston',
                                       'nashville', 'baltimore', 'portland', 'melbourne', 'sydney', 'perth', 'albany',
                                       'bunbury'],
                              'message': 'We currently do not support {} as a valid pickup location.  Can you try a '
                                         'different city?'}]
              },
             {
                 'slotName': 'PickUpDate',
                 'name': 'Pick up date',
                 'validation': [{'fn': validation.isvalid_date,
                                 'message': 'I did not understand your pick up date.  When would you like to pick up '
                                            'the car?'},
                                {'fn': validation.isvalid_date_beyond,
                                 'val1': datetime.date.today(),
                                 'message': 'Reservations must be scheduled at least one day in advance.  Can '
                                            'you try a different date?'}]
             },
             {
                 'slotName': 'ReturnDate',
                 'name': 'Return date',
                 'validation': [{'fn': validation.isvalid_date,
                                 'message': 'I did not understand your return date.  When would you like to return '
                                            'the car?'},
                                {'fn': validation.isvalid_date_beyond,
                                 'val1': 'slot:PickUpDate',
                                 'message': 'The return date needs to be after the pickup date.  Can '
                                            'you try a different date?'}]
             },
             {
                 'slotName': 'DriverAge',
                 'name': 'Driver age',
                 'validation': [{'fn': validation.isvalid_num_range,
                                 'val1': 18,
                                 'val2': 110,
                                 'message': 'Sorry the driver must be at least 18 to hire a car. How old is another '
                                            'driver of the car?'}]
             },
             {
                 'slotName': 'CarType',
                 'name': 'Car Type',
                 'validation': [{'fn': validation.isvalid_in_array,
                                 'val1': ['hatchback', 'sedan', 'ute', 'luxury', 'sports', 'minivan'],
                                 'message': "Sorry I didn't recognise that type of car, we have hatchbacks, sedans, "
                                            "utes, luxury, sports and minivans. Which one would you like?"
                                 }
                                ]
             }]


class BookCar(Intent):
    """
    Handles the Lex Intent BookCar, inherits from Intent which provides most of the logic
    """

    def __init__(self, intent_request):
        Intent.__init__(self, intent_request, car_slots, 'Car Booking')

    """
    Fires once all data has been entered and validated. Calculates a price based on the inputted values
    """
    def on_data_completed(self, reservation, session_attributes):
        pickup_city = reservation['PickUpCity']
        pickup_date = reservation['PickUpDate']
        return_date = reservation['ReturnDate']
        driver_age = reservation['DriverAge']
        car_type = reservation['CarType']

        # The price of the hotel has yet to be confirmed.
        price = self.generate_car_price(pickup_city, pickup_date, return_date, driver_age, car_type)
        session_attributes['currentReservationPrice'] = price
        message = 'OK, I have you down for a {} to be picked up from {} on the {} to be returned on {},  ' \
                  'Driver Age: {}. Total price: {}'.format(car_type, pickup_city, pickup_date, return_date,
                                                           driver_age, price)
        # TODO: find out why this doesn't work? Wrong response to Lex v2?
        # return lex_v2.confirm_intent(intent_request, session_attributes,
        #                             intent_request['sessionState']['intent']['slots'], message)
        return message

    """
    Generates a number within a reasonable range that might be expected for a car.
    The price also takes into consideration being a young driver
    """
    def generate_car_price(self, pickup_city, pickup_date, return_date, driver_age, car_type):

        car_types = ['hatchback', 'sedan', 'ute', 'luxury', 'sports', 'minivan']
        cost_of_living = 0
        young_driver_fee = 0

        nights = utility.get_day_difference(pickup_date, return_date)

        if driver_age < 21:
            young_driver_fee = 15

        for i in range(len(pickup_city)):
            cost_of_living += ord(pickup_city.lower()[i]) - 97

        return nights * (100 + young_driver_fee + cost_of_living + (100 + car_types.index(car_types.lower())))

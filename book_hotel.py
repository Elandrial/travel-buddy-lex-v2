import datetime
import json
import utility
import lex_v2
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def process(intent_request):
    location = lex_v2.get_slot(intent_request, 'Location')
    checkin_date = lex_v2.get_slot(intent_request, 'CheckInDate')
    nights = utility.safe_int(lex_v2.get_slot(intent_request, 'Nights'))
    room_type = lex_v2.get_slot(intent_request, 'RoomType')
    breakfast_included = lex_v2.get_slot(intent_request, 'BreakfastIncluded')
    session_attributes = lex_v2.get_session_attributes(intent_request)

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'ReservationType': 'Hotel',
        'Location': location,
        'RoomType': room_type,
        'CheckInDate': checkin_date,
        'Nights': nights,
        'BreakfastIncluded': breakfast_included
    })

    session_attributes['currentReservation'] = reservation

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_hotel(intent_request)
        if not validation_result['isValid']:
            slots = lex_v2.get_slots(intent_request)
            slots[validation_result['violatedSlot']] = None

            return lex_v2.elicit_slot(
                intent_request,
                session_attributes,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        message = None
        # Otherwise, let native DM rules determine how to elicit for slots and prompt for confirmation.  Pass price
        # back in sessionAttributes once it can be calculated; otherwise clear any setting from sessionAttributes.
        if location and checkin_date and nights and room_type and breakfast_included:
            # The price of the hotel has yet to be confirmed.
            price = generate_hotel_price(location, nights, room_type, breakfast_included)
            session_attributes['currentReservationPrice'] = price
            message = 'OK, I have you down for a {} room with a {} night stay in {} starting {},  ' \
                      'Breakfast: {}. Total price: {}'.format(room_type, nights, location,
                                                              checkin_date, breakfast_included, price)
        else:
            lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')

        session_attributes['currentReservation'] = reservation
        return lex_v2.delegate(intent_request, session_attributes, intent_request['sessionState']['intent']['slots'],
                               lex_v2.create_message(message))

    # Booking the hotel.  In a real application, this would likely involve a call to a backend service.
    logger.debug('bookHotel under={}'.format(reservation))

    lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')
    lex_v2.remove_session_attribute(session_attributes, 'currentReservation')
    session_attributes['lastConfirmedReservation'] = reservation

    return lex_v2.close(intent_request,
                        session_attributes,
                        'Fulfilled',
                        lex_v2.create_message('Thanks, I have placed your reservation.')
                        )


def isvalid_city(city):
    valid_cities = ['new york', 'los angeles', 'chicago', 'houston', 'philadelphia', 'phoenix', 'san antonio',
                    'san diego', 'dallas', 'san jose', 'austin', 'jacksonville', 'san francisco', 'indianapolis',
                    'columbus', 'fort worth', 'charlotte', 'detroit', 'el paso', 'seattle', 'denver', 'washington dc',
                    'memphis', 'boston', 'nashville', 'baltimore', 'portland', 'melbourne', 'sydney', 'perth',
                    'albany', 'bunbury']
    return city.lower() in valid_cities


def generate_hotel_price(location, nights, room_type, breakfast_included):
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


# validation
def isvalid_room_type(room_type):
    room_types = ['queen', 'king', 'deluxe']
    return room_type.lower() in room_types


def isvalid_breakfast(breakfast_included):
    yes_no_options = ['yes', 'no', 'sure', 'nope', 'never', 'positive', 'negative', 'nay']
    return breakfast_included.lower() in yes_no_options


def validate_hotel(intent_request):
    location = lex_v2.get_slot(intent_request, 'Location')
    checkin_date = lex_v2.get_slot(intent_request, 'CheckInDate')
    nights = utility.safe_int(lex_v2.get_slot(intent_request, 'Nights'))
    room_type = lex_v2.get_slot(intent_request, 'RoomType')
    breakfast_included = lex_v2.get_slot(intent_request, 'BreakfastIncluded')

    if location and not isvalid_city(location):
        return lex_v2.build_validation_result(False, 'Location',
                                              'We currently do not support {} as a valid destination.  '
                                              'Can you try a different city?'.format(location))

    if checkin_date:
        if not utility.isvalid_date(checkin_date):
            return lex_v2.build_validation_result(False, 'CheckInDate',
                                                  'I did not understand your check in date.  When would you like to '
                                                  'check in?')
        if datetime.datetime.strptime(checkin_date, '%Y-%m-%d').date() <= datetime.date.today():
            return lex_v2.build_validation_result(False, 'CheckInDate',
                                                  'Reservations must be scheduled at least one day in advance.  Can '
                                                  'you try a different date?')

    if nights is not None and (nights < 1 or nights > 30):
        return lex_v2.build_validation_result(
            False,
            'Nights',
            'You can make a reservations for from one to thirty nights.  How many nights would you like to stay for?'
        )

    if room_type and not isvalid_room_type(room_type):
        return lex_v2.build_validation_result(False, 'RoomType',
                                              'I did not recognize that room type.  Would you like to stay in a '
                                              'queen, king, or deluxe room?')

    if breakfast_included and not isvalid_breakfast(breakfast_included):
        return lex_v2.build_validation_result(False, 'BreakfastIncluded',
                                              "Sorry I didn't understand your answer, did you want to include breakfast"
                                              " with your accommodation?")

    return {'isValid': True}

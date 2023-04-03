import datetime
import json
import utility
import lex_v2
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def process(intent_request):
    location = utility.try_ex(lambda: intent_request['currentIntent']['slots']['Location'])
    checkin_date = utility.try_ex(lambda: intent_request['currentIntent']['slots']['CheckInDate'])
    nights = utility.safe_int(utility.try_ex(lambda: intent_request['currentIntent']['slots']['Nights']))
    room_type = utility.try_ex(lambda: intent_request['currentIntent']['slots']['RoomType'])
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'ReservationType': 'Hotel',
        'Location': location,
        'RoomType': room_type,
        'CheckInDate': checkin_date,
        'Nights': nights
    })

    session_attributes['currentReservation'] = reservation

    if intent_request['invocationSource'] == 'DialogCodeHook':
        # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
        validation_result = validate_hotel(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return lex_v2.elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        # Otherwise, let native DM rules determine how to elicit for slots and prompt for confirmation.  Pass price
        # back in sessionAttributes once it can be calculated; otherwise clear any setting from sessionAttributes.
        if location and checkin_date and nights and room_type:
            # The price of the hotel has yet to be confirmed.
            price = generate_hotel_price(location, nights, room_type)
            session_attributes['currentReservationPrice'] = price
        else:
            utility.try_ex(lambda: session_attributes.pop('currentReservationPrice'))

        session_attributes['currentReservation'] = reservation
        return lex_v2.delegate(session_attributes, intent_request['currentIntent']['slots'])

    # Booking the hotel.  In a real application, this would likely involve a call to a backend service.
    logger.debug('bookHotel under={}'.format(reservation))

    utility.try_ex(lambda: session_attributes.pop('currentReservationPrice'))
    utility.try_ex(lambda: session_attributes.pop('currentReservation'))
    session_attributes['lastConfirmedReservation'] = reservation

    return lex_v2.close(
        session_attributes,
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': 'Thanks, I have placed your reservation.'
        }
    )


def generate_hotel_price(location, nights, room_type):
    """
    Generates a number within a reasonable range that might be expected for a hotel.
    The price is fixed for a pair of location and roomType.
    """

    room_types = ['queen', 'king', 'deluxe']
    cost_of_living = 0
    for i in range(len(location)):
        cost_of_living += ord(location.lower()[i]) - 97

    return nights * (100 + cost_of_living + (100 + room_types.index(room_type.lower())))


# validation
def isvalid_room_type(room_type):
    room_types = ['queen', 'king', 'deluxe']
    return room_type.lower() in room_types


def validate_hotel(slots):
    location = utility.try_ex(lambda: slots['Location'])
    checkin_date = utility.try_ex(lambda: slots['CheckInDate'])
    nights = utility.safe_int(utility.try_ex(lambda: slots['Nights']))
    room_type = utility.try_ex(lambda: slots['RoomType'])

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

    return {'isValid': True}

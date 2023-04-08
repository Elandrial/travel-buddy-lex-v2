def simple_request():
    return {
        'sessionId': '361143368210760',
        'bot': {
            'aliasId': 'TSTALIASID',
            'aliasName': 'TestBotAlias',
            'name': 'TravelBuddy',
            'version': 'DRAFT',
            'localeId': 'en_US',
            'id': 'U6FQYXVFLD'
        },
        'inputTranscript': 'book a hotel',
        'interpretations': [
            {
                'intent': {
                    'confirmationState': 'None',
                    'name': 'BookHotel',
                    'state': 'InProgress',
                    'slots': {
                        'RoomType': None,
                        'CheckInDate': None,
                        'Nights': None,
                        'BreakfastIncluded': None,
                        'Location': None
                    }
                },
                'nluConfidence': 1
            },
            {
                'intent': {
                    'confirmationState': 'None',
                    'name': 'BookFlight',
                    'state': 'InProgress',
                    'slots': {
                        'cabinClass': None,
                        'returnDate': None,
                        'locationTo': None,
                        'leaveDate': None,
                        'locationFrom': None
                    }
                },
                'nluConfidence': 0.56
            },
            {
                'intent': {
                    'confirmationState': 'None',
                    'name': 'BookCar',
                    'state': 'InProgress',
                    'slots': {
                        'ReturnDate': None,
                        'PickUpDate': None,
                        'DriverAge': None,
                        'CarType': None,
                        'PickUpCity': None
                    }
                },
                'nluConfidence': 0.51
            },
            {
                'intent': {
                    'confirmationState': 'None',
                    'name': 'FallbackIntent',
                    'state': 'InProgress',
                    'slots': {}
                }
            }
        ],
        'proposedNextState': {
            'intent': {
                'confirmationState': 'None',
                'name': 'BookHotel',
                'state': 'InProgress',
                'slots': {
                    'RoomType': None,
                    'CheckInDate': None,
                    'Nights': None,
                    'BreakfastIncluded': None,
                    'Location': None
                }
            },
            'dialogAction': {
                'slotToElicit': 'Location',
                'type': 'ElicitSlot'
            },
            'prompt': {
                'attempt': 'Initial'
            }
        },
        'responseContentType': 'text/plain; charset=utf-8',
        'messageVersion': '1.0',
        'invocationSource': 'DialogCodeHook',
        'transcriptions': [
            {
                'transcription': 'book a hotel',
                'resolvedSlots': {},
                'transcriptionConfidence': 1,
                'resolvedContext': {
                    'intent': 'BookHotel'
                }
            }
        ],
        'sessionState': sample_session_state_one(),
        'inputMode': 'Text',
        'messages': sample_messages_one(),
        'requestAttributes': None
    }


def sample_intent_one():
    return {
        'name': 'BookHotel',
        'state': 'InProgress',
        'confirmationState': 'None',
        'slots': sample_slots_one()
    }


def sample_session_state_one():
    return {
        'dialogAction': {
            'type': 'ElicitSlot',
            'slotToElicit': 'CheckInDate'
        },
        'sessionAttributes': sample_session_attributes_one(),
        'intent': sample_intent_one()
    }


def sample_slots_one():
    return {
        'RoomType': None,
        'CheckInDate': {
            'shape': 'Scalar',
            'value': {
                'originalValue': '1st june 2023',
                'resolvedValues': ['2023-06-01'],
                'interpretedValue': '2023-06-01'
            }
        },
        'Nights': None,
        'BreakfastIncluded': None,
        'Location': {
            'shape': 'Scalar',
            'value': {
                'originalValue': 'perth',
                'resolvedValues': ['perth'],
                'interpretedValue': 'perth'
            }
        }
    }


def sample_session_attributes_one():
    return {
        'currentReservation': '{"ReservationType": "Hotel Booking", "Location": "perth", '
                              '"Check in date": null, "Nights": null, "Room Type": null, '
                              '"Breakfast Included": null}'
    }


def sample_messages_one():
    return [{
        'contentType': 'PlainText',
        'content': 'Reservations must be scheduled at least one day in advance.  Can you try a different date?'
    }]

def elicit_slot(intent_request, session_attributes, slot_to_elicit, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        "slotToElicit": slot_to_elicit if slot_to_elicit is not None else None,
        'messages': [message] if message is not None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ConfirmIntent',
                'slots': slots
            },
            'intent': {
                'name': intent_name,
                'state': 'InProgress'
            },
            'messages': [message]
        }
    }


def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }


def delegate(intent_request, session_attributes, slots, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': slots
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message] if message is not None else None,
    }


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': create_message(message_content)
    }


def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']


def get_slot(intent_request, slot_name):
    slots = get_slots(intent_request)
    if slots is not None and slot_name in slots and slots[slot_name] is not None:
        return slots[slot_name]['value']['interpretedValue']
    else:
        return None


def get_session_attributes(intent_request):
    session_state = intent_request['sessionState']
    if 'sessionAttributes' in session_state:
        return session_state['sessionAttributes']

    return {}


def get_session_attribute(intent_request, name):
    session_attributes = get_session_attributes(intent_request)
    if name in session_attributes:
        return session_attributes[name]

    return None


def remove_session_attribute(session_attributes, name):
    if name in session_attributes:
        session_attributes.pop(name)


def create_message(text):
    if text is not None:
        return {
            'contentType': 'PlainText',
            'content': text
        }
    else:
        return None



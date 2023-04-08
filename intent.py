import json
import logging

import lex_v2
import utility
import validation

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Intent:
    """
    The Parent class for all Lex v2 intents, allows the easy setup and maintenance of intent handling
    """

    """
    Initialises the object
    intent_request: supplied by Lex on intent fire
    slots: user configured with the appropriate validation rules
    reservation_name: the output name to use for messages relating to this intent
    """
    def __init__(self, intent_request, slots, reservation_name):
        self.request = intent_request
        self.reservation_name = reservation_name
        self.slots = slots

    """
    Performs validation on the data that has been supplied using the defined slots rules
    """
    def validate(self):
        lex_slots = lex_v2.get_slots(self.request)
        # loop through the defined slots, running the relevant validation and returning the result
        for slot in self.slots:
            # always basic test first
            request_slot = lex_v2.get_slot_from_slots(lex_slots, slot['slotName'])

            # if we have a value set, lets validate it
            if request_slot:
                if not lex_v2.isvalid_slot_value(request_slot):
                    return lex_v2.build_validation_result(False, slot['slotName'],
                                                          "Sorry I didn't recognise that {}, could you please "
                                                          "try again?".format(slot['name']))

                # loop through the assign validation scripts
                for validation_fn in slot['validation']:
                    # map any dependencies with their values, should we require them for the current slot
                    dynamic_values = validation.map_validation(lex_slots, validation_fn)

                    # perform the dynamic function calling for valiation
                    if not validation.do_validate(validation_fn, lex_v2.get_slot_value(request_slot), dynamic_values):
                        return lex_v2.build_validation_result(False, slot['slotName'],
                                                              validation_fn['message'].format(
                                                                  lex_v2.get_slot_value(request_slot)))

        return {'isValid': True}

    """
    The main entry point to the program. This will fire everytime there is a user interaction from the lex bot
    """
    def process(self):
        session_attributes = lex_v2.get_session_attributes(self.request)
        reservation = self.generate_reservation()

        # if we've taken slot input, lets process it
        if self.request['invocationSource'] == 'DialogCodeHook':
            validation_result = self.validate()
            if not validation_result['isValid']:
                return lex_v2.elicit_slot(
                    self.request,
                    session_attributes,
                    validation_result['violatedSlot'],
                    validation_result['message']
                )

            message = None

            if self.are_all_slots_set(reservation):
                message = self.on_data_completed(reservation, session_attributes)
            else:
                lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')

            session_attributes['currentReservation'] = json.dumps(reservation)
            # inform lex to go to the next action
            return lex_v2.delegate(self.request, session_attributes, self.request['sessionState']['intent']['slots'],
                                   lex_v2.create_message(message))

        logger.debug('{} under={}'.format(self.reservation_name, reservation))
        lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')
        lex_v2.remove_session_attribute(session_attributes, 'currentReservation')
        session_attributes['lastConfirmedReservation'] = reservation

        # close the interaction and consider it fullfilled
        return lex_v2.close(self.request,
                            session_attributes,
                            'Fulfilled',
                            lex_v2.create_message('Thanks, I have placed your reservation.')
                            )

    """
    Generate a reservation object that can be used for data storage
    """
    def generate_reservation(self):
        reservation = {'ReservationType': self.reservation_name}
        for slot in self.slots:
            reservation[slot['name']] = lex_v2.get_slot_value(lex_v2.get_slot_from_intent(self.request, slot['name']))
        return reservation

    def on_data_completed(self, reservation, session_attributes):
        return

    def are_all_slots_set(self, reservation):
        for field in reservation:
            if field:
                return False
        return True

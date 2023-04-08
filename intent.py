import json
import logging

import lex_v2
import utility
import validation

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Intent:
    def __init__(self, intent_request, slots, reservation_name):
        self.request = intent_request
        self.reservation_name = reservation_name
        self.slots = slots

    def validate(self):
        print('validating')
        print(self.slots)
        lex_slots = lex_v2.get_slots(self.request)
        print(lex_slots)
        # loop through the defined slots, running the relevant validation and returning the result
        for slot in self.slots:
            # always basic test first
            request_slot = lex_v2.get_slot_from_slots(lex_slots, slot['slotName'])

            if request_slot:
                print('request_slot set: ', request_slot)
                if not lex_v2.isvalid_slot_value(request_slot):
                    print('value not valid')
                    return lex_v2.build_validation_result(False, slot['slotName'],
                                                          "Sorry I didn't recognise that {}, could you please "
                                                          "try again?".format(slot['name']))

                # loop through the assign validation scripts
                for validation_fn in slot['validation']:
                    dynamic_values = validation.map_validation(lex_slots, validation_fn)
                    print('validating with: ', validation_fn)
                    if not validation.do_validate(validation_fn, lex_v2.get_slot_value(request_slot), dynamic_values):
                        return lex_v2.build_validation_result(False, slot['slotName'],
                                                              validation_fn['message'].format(
                                                                  lex_v2.get_slot_value(request_slot)))
                print('finished validating: ', request_slot)
        print('is valid')
        return {'isValid': True}

    def process(self):
        session_attributes = lex_v2.get_session_attributes(self.request)
        reservation = self.generate_reservation()

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
                print('all set')
                message = self.on_data_completed(reservation, session_attributes)
            else:
                print('more to go')
                lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')

            session_attributes['currentReservation'] = json.dumps(reservation)
            return lex_v2.delegate(self.request, session_attributes, self.request['sessionState']['intent']['slots'],
                                   lex_v2.create_message(message))

        logger.debug('{} under={}'.format(self.reservation_name, reservation))
        lex_v2.remove_session_attribute(session_attributes, 'currentReservationPrice')
        lex_v2.remove_session_attribute(session_attributes, 'currentReservation')
        session_attributes['lastConfirmedReservation'] = reservation

        return lex_v2.close(self.request,
                            session_attributes,
                            'Fulfilled',
                            lex_v2.create_message('Thanks, I have placed your reservation.')
                            )

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

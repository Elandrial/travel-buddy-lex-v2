from context import lex_v2
import lex_v2
from tests import json_samples


def test_lex_v2():
    sample_intent = json_samples.simple_request()
    session_attributes = json_samples.sample_session_attributes_one()
    messages = json_samples.sample_messages_one()
    session_state = json_samples.sample_session_state_one()

    # TODO: Implement testing for individual json generators
    # elicit_slot(intent_request, session_attributes, slot_to_elicit, message)
    # assert lex_v2.elicit_slot(sample_intent, session_attributes, 'CheckInDate', messages) == session_state

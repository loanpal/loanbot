from dateutil import parser
# dt = parser.parse("Aug 28 1999 12:00AM")
from utils import next_prompt, send_text_message, check_error_threshold, increment_error_counts
from application import db

def initial(user, message):
    message_text = 'When were you born?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        check_error_threshold(user)
        increment_error_counts(user)
        follow_up(user, message)

def parse(user, message):
    response = message.get('text')
    dob = parser.parse(response, fuzzy=True)
    if dob:
        user.dob = dob
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, please type your birth date.'
    send_text_message(user.id, message_text)

dob = {
    'initial': initial,
    'action': action
}

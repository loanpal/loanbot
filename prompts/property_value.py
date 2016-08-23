from utils import next_prompt, send_text_message
from application import db
import re

def initial(user, message):
    message_text = ' Please estimate the value of the property.'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    text = message.get('text')
    numbers_only = re.sub("[^0-9]", "", text)
    if len(numbers_only) > 4:  # Houses worth less than $9,999 aren't interesting to us
        user.property_value = numbers_only
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, what is the value of the property?'
    send_text_message(user.id, message_text)

property_value = {
    'initial': initial,
    'action': action
}

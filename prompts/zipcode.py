from utils import next_prompt, send_text_message
from application import db
import re

def initial(user, message):
    message_text = 'What is your zipcode?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    text = message.get('text')
    numbers_only = re.sub("[^0-9]", "", text)
    if len(numbers_only) == 5:
        user.zipcode = numbers_only
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, can you enter your zipcode?'
    send_text_message(user.id, message_text)

zipcode = {
    'initial': initial,
    'action': action
}

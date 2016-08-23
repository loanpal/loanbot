from nameparser import HumanName
from utils import next_prompt, send_text_message
from application import db

def initial(user, message):
    message_text = 'What is your full name?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    name = message.get('text')
    parsed_name = HumanName(name)
    if (parsed_name.first and parsed_name.last):
        user.first_name = parsed_name.first
        user.last_name = parsed_name.last
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, can you enter your name?'
    send_text_message(user.id, message_text)

name = {
    'initial': initial,
    'action': action
}

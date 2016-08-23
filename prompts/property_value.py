from utils import next_prompt, send_text_message
from application import db

def initial(user, message):
    message_text = ' Please estimate the value of the property.'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    user.property_value = message.get('text')
    db.session.commit()

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, what is the value of the property?'
    send_text_message(user.id, message_text)

property_value = {
    'initial': initial,
    'action': action
}

from utils import next_prompt, send_text_message
from application import db

def new_scope(user, message):
    user.current_scope = 'new_lead'
    user.current_prompt = 'zipcode'
    db.session.commit()
    next_prompt(user, message)

def send_question(user):
    message_text = 'Welcome to Loanpal!'
    send_text_message(user.id, message_text)
    return

welcome = {
    'action': send_question,
}

from utils import next_prompt, send_text_message
from application import db

def initial(user, message):
    message_text = 'What is your zipcode?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    user.zipcode = message.get('text')
    db.session.commit()

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, can you enter your zipcode?'
    send_text_message(user.id, message_text)

zipcode = {
    'initial': initial,
    'action': action
}

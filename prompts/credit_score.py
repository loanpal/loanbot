from utils import next_prompt, send_text_message
from application import db

def initial(user, message):
    message_text = 'Estimate your credit score.'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    user.credit_score = message.get('text')
    db.session.commit()

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, estimate your credit score'
    send_text_message(user.id, message_text)

credit_score = {
    'initial': initial,
    'action': action
}

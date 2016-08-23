from utils import next_prompt, send_text_message
from application import db

def initial(user, message):
    message_text = 'Thank you!'
    send_text_message(user.id, message_text)

def action(user, message):
    initial(user, message)
    next_prompt(user, message)

def parse(user, message):
    pass

# def follow_up(user, message):
#     # TODO: Customize response based on error count here
#     message_text = 'I didn\'t get that, can you enter your zipcode?'
#     send_text_message(user.id, message_text)
thank_you = {
    'initial': initial,
    'action': action
}

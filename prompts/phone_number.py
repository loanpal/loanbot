import phonenumbers
from utils import next_prompt, send_text_message
from application import db
import re

def initial(user, message):
    message_text = 'Great, your rates are ready. What is your mobile or home phone number?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    phone_number = message.get('text')
    cleaned_phone_number = re.sub("[^0-9]", "", phone_number)
    number = phonenumbers.parse(cleaned_phone_number, 'US')
    formated_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
    if formated_number:
        user.phone_number = formated_number
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, can you enter your phone_number?'
    send_text_message(user.id, message_text)

phone_number = {
    'initial': initial,
    'action': action
}

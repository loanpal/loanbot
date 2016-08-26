from utils import next_prompt, send_text_message, check_error_threshold, increment_error_counts
from application import db
import re

def initial(user, message):
    message_text = 'What is the remaining 1st mortgage balance?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        check_error_threshold(user)
        increment_error_counts(user)
        follow_up(user, message)

def parse(user, message):
    text = message.get('text')
    numbers_only = re.sub("[^0-9]", "", text)
    pattern = 'zero|none|paid off|paid|don\'t'
    if numbers_only:
        user.mortgage_balance = numbers_only
        db.session.commit()
        return True
    if re.match(pattern, text.lower(), flags=0):
        user.mortgage_balance = numbers_only
        db.session.commit()
        return True
    return False

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, what is the remaining 1st mortgage balance?'
    send_text_message(user.id, message_text)

mortgage_balance = {
    'initial': initial,
    'action': action
}

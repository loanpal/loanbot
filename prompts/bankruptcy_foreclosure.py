from utils import next_prompt, send_quick_reply, send_text_message, increment_error_counts, check_error_threshold
from application import db
from configuration import default_thresholds

def initial(user, message):
    message_text = 'Have you had a bankruptcy or foreclosure in the last 7 years?'
    options = [
        {
            "content_type": "text",
            "title": "No",
            "payload": "No"
        },
        {
            "content_type": "text",
            "title": "Bankruptcy",
            "payload": "Bankruptcy"
        },
        {
            "content_type": "text",
            "title": "Foreclosure",
            "payload": "Foreclosure"
        },
        {
            "content_type": "text",
            "title": "Both",
            "payload": "Both"
        }
    ]
    send_quick_reply(user.id, message_text, options)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        check_error_threshold(user, default_thresholds)
        increment_error_counts(user)
        follow_up(user, message)

def parse(user, message):
    user.is_recent_bankruptcy = False
    user.is_recent_foreclosure = False
    db.session.commit()
    return True

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, let\'s try again?'
    send_text_message(user.id, message_text)
    initial(user, message)

bankruptcy_foreclosure = {
    'initial': initial,
    'action': action
}

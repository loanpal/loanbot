import os
import sys
import json

import requests
from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import *
from outline import *

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must
    # return the 'hub.challenge' value in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webook():
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] != "page":
        return "ok", 200

    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:
            if messaging_event.get('message'):
                # Handle message
                received_message(messaging_event)
            # elif messaging_event.get('optin'):
            #   receivedAuthentication(messaging_event)
            # elif messaging_event.get('delivery'):
            #   receivedDeliveryConfirmation(messaging_event)
            # elif messaging_event.get('postback'):
            #   receivedPostback(messaging_event)
            # elif messaging_event.get('read'):
            #   receivedMessageRead(messaging_event)
            # elif messaging_event.get('account_linking'):
            #   receivedAccountLink(messaging_event)
            else:
              log("Webhook received unknown messaging_event: " + json.dumps(messaging_event))

    return "ok", 200


#
# Message Event
#
# This event is called when a message is sent to your page. The 'message'
# object format can vary depending on the kind of message that was received.
# Read more at https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-received
#
# For this example, we're going to echo any text that we get. If we get some
# special keywords ('button', 'generic', 'receipt'), then we'll send back
# examples of those bubbles to illustrate the special message bubbles we've
# created. If we receive a message with an attachment (image, video, audio),
# then we'll simply confirm that we've received the attachment.
#
def received_message(event):
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    time_of_message = event['timestamp']
    message = event['message']

    # Find or Create User
    try:
        user = User.get(id)
    except:
        user = User(id=sender_id)
        db.session.add(user)

    is_echo = message.get('is_echo')
    message_id = message.get('mid')
    sequence_id = message.get('seq')
    sticker_id = message.get('sticker_id')
    app_id = message.get('app_id')
    metadata = message.get('metadata')

    if is_echo:
        # Just logging message echoes to console
        log("Received echo for message %s and app %s with metadata %s" %
                (message_id, app_id, metadata));
        return

    # You may get a text or attachment but not both
    message_text = message.get('text')
    message_attachments = message.get('attachments')
    quick_reply = message.get('quick_reply')


    # elif quick_reply:
    #     quick_reply_payload = quick_reply['payload'];
    #     log("Quick reply for message %s with payload %s" %
    #             (message_id, quick_reply_payload))
    #     send_text_message(senderID, "Quick reply tapped");
    #     return

    if message_text:
        parse_text_message(user, message_text)
    elif message_attachments:
        send_text_message(sender_id, "Message with attachment received")
    else:
        log("Invalid message")

def parse_text_message(user, message_text):
    current_step = get_current_step(user)
    valid_input = validate_and_save(user, current_step, message_text)
    if valid_input:
        next_step = get_next_step(current_step)
        next_message = details[next_step]['questions'][0]  # Randomize?
        send_text_message(user.id, next_message)
    else:
        repeat_message = details[current_step]['repeat_questions'][0]  # Randomize?
        send_text_message(user.id, repeat_message)

def get_current_step(user):
    # look through steps in order
    for step_name in order:
        step = details[step_name]
        validation = step['data_to_collect']  # an array of strings that are User model attibutes

        # for each check to see if there is a value saved in the applicable fields
        for attribute in validation:
            current = getattr(user, attribute)
            if not current:
                # If not, return that step
                return step_name

def get_next_step(current_step):
    index = order.index(current_step)
    next_index = index + 1
    return order[next_index]


def validate_and_save(user, current_step, message_text):
    # add validation logic
    step_details = details[current_step]
    data = step_details['parser'](user, message_text)  # False if isn't valid



def send_text_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}"
            .format(recipient=recipient_id, text=message_text))

    send_message({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
        }
    })


def send_message(data):
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps(data)

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)

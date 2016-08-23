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
from utils import next_prompt
from prompts import prompts
from utils import send_text_message

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
    print(data)  # you may not want to print every incoming message in production, but it's good for testing

    if data["object"] != "page":
        return "ok", 200

    for entry in data["entry"]:
        for messaging_event in entry["messaging"]:
            if messaging_event.get('message') or messaging_event.get('postback'):
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
              print("Webhook received unknown messaging_event: " + json.dumps(messaging_event))

    return "ok", 200


#
# Message Event
#

def received_message(event):
    sender_id = event['sender']['id']
    message = event.get('message')
    postback = event.get('postback')
    if postback and not message:
        message = {'text': postback['payload']}

    # Find or Create User
    user = User.query.get(sender_id)
    if not user:
        # First visit
        user = User(id=sender_id)
        db.session.add(user)
        db.session.commit()
        send_text_message(user.id, 'Welcome to LoanPal!')

    # Hack to see info REMOVE BEFORE PUBLISHING
    if message['text'] == 'myData':
        return printUserData(user)

    # Find current prompt
    current_prompt_name = user.current_prompt
    if not user.current_prompt:
        # Defualt action ('welcome')
        next_prompt(user, message)
    else:
        # Trigger action
        current_prompt = prompts[current_prompt_name]
        current_action = current_prompt['action']
        current_action(user, message or postback)
    return

def printUserData(user):
    string = ''
    string += 'first_name: ' + str(user.first_name) +'\n'
    string += 'last_name: ' + str(user.last_name) +'\n'
    string += 'phone_number: ' + str(user.phone_number) +'\n'
    string += 'property_value: ' + str(user.property_value) +'\n'
    string += 'mortgage_balance: ' + str(user.mortgage_balance) +'\n'
    string += 'credit_score: ' + str(user.credit_score) +'\n'
    string += 'dob: ' + str(user.dob) +'\n'
    string += 'is_recent_bankruptcy: ' + str(user.is_recent_bankruptcy) +'\n'
    string += 'is_recent_foreclosure: ' + str(user.is_recent_foreclosure) +'\n'
    string += 'street_address: ' + str(user.street_address) +'\n'
    string += 'city: ' + str(user.city) +'\n'
    string += 'state: ' + str(user.state) +'\n'
    string += 'zipcode: ' + str(user.zipcode) +'\n'
    # string += 'messages: ' + str(user.messages) +'\n'
    # string += 'total_error_count: ' + str(user.total_error_count) +'\n'
    # string += 'current_scope: ' + str(user.current_scope) +'\n'
    # string += 'current_scope_eror_count: ' + str(user.current_scope_eror_count) +'\n'
    # string += 'current_prompt: ' + str(user.current_prompt) +'\n'
    # string += 'current_prompt_eror_count: ' + str(user.current_prompt_eror_count) +'\n'
    # string += 'sent_to_velocify: ' + str(user.sent_to_velocify) +'\n'

    send_text_message(user.id, string)
    return

if __name__ == '__main__':
    app.run(debug=True)

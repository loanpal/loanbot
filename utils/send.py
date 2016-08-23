import os
import json
import requests

def send_text_message(recipient_id, message_text):
    send_message({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
        }
    })

# More than ~3 elements creates horizontal scroll
def send_quick_reply(recipient_id, message_text, options):
    send_message({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies": options
        }
    })

# Max is 3 buttons
def send_button_template(recipient_id, message_text, buttons):
    send_message({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": buttons
                }
            }
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

    r = requests.post(
        "https://graph.facebook.com/v2.6/me/messages",
        params=params,
        headers=headers,
        data=data
    )
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)

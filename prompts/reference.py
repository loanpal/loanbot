# button temlate
buttons = [
    {
        "type": "web_url",
        "url": "https://petersapparel.parseapp.com",
        "title": "Show Website"
    },
    {
        "type": "postback",
        "title": "Start Chatting",
        "payload": "USER_DEFINED_PAYLOAD"
    }
]

# generic temlate
elements = [
    {
        "title": "Welcome to Peter\'s Hats",
        "image_url": "http://petersapparel.parseapp.com/img/item100-thumb.png",
        "subtitle": "We\'ve got the right hat for everyone.",
        "buttons": [
            {
                "type": "web_url",
                "url": "https://petersapparel.parseapp.com/view_item?item_id=100",
                "title": "View Website"
            },
            {
                "type": "postback",
                "title": "Start Chatting",
                "payload": "USER_DEFINED_PAYLOAD"
            }
        ]
    }
]

# quick_reply
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
    },
]

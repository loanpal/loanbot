# Loanpal Messenger Bot

### Basic elements
* `Prompt`
    - Question asked of the user that anticipate a specific response
    - Include function for parsing response and saving to DB
    - Includes an action that directs what should be done after a successful response. Actions should always return a prompt. Possibilities inclue:
        * Proceed to next `Prompt` in `Scope`
        * Jump to new `Scope`
        * Increment Error counts and repeat question

* `Scope`
    - Represents a chain of `Prompt`s asked to a user leading to a specific goal
    - When a user enters a scope, they will continue in the context of this scope until:
        * They send a cancel command (default: cancel)
        * They complete the current scope
        * The current scope hooks them into a different scope

* `Message`
    - Text: Standard text message
    - Button: Uses a template to send clickable buttons that can lead to an external URL or send a `postback` request
    - Quick_reply: Similar to button, but can only be text and send back a quick_reply response
    - Attachment: Send a picture, video, etc
    - General Template: Send a template that can have several elements and/or buttons. Sending several elements gives you the swipeable option interface.

* Errors
    - Tallied whenever the bot is unable to intelligently interpret a message
    - Tallied at each level of the app: Overall, current `Scope`, and current `Prompt`
    - Designed to allow custom responses when error count reaches threshold

### Types of callbacks received
* Text message
* Attachment
* quick_reply
* postback
* (additional available, but not yet implemented)

from application import db
from .send import send_button_template
from configuration import default_thresholds

def next_prompt(user, message):
    from prompts import prompts
    from scopes import scopes

    current_scope_name = user.current_scope
    current_prompt_name = user.current_prompt
    if not current_scope_name:
        user.current_scope = 'welcome'
        current_scope_name = 'welcome'
        user.current_prompt = 'welcome'
        current_prompt_name = 'welcome'
        db.session.commit()

    current_scope = scopes[current_scope_name]
    next_index = current_scope.index(current_prompt_name) + 1

    if next_index >= len(current_scope):
        user.current_scope = 'new_lead'
        user.current_prompt = 'zipcode'
        new_current_prompt_name = 'zipcode'
        db.session.commit()
    else:
        # Advance to next prompt in scope
        new_current_prompt_name = current_scope[next_index]
        user.current_prompt = new_current_prompt_name
        db.session.commit()

    new_current_prompt = prompts[new_current_prompt_name]
    # Send initiate next prompt
    initial = new_current_prompt['initial']
    initial(user, message)
    return

def increment_error_counts(user):
    user.total_error_count += 1
    user.current_scope_eror_count += 1
    user.current_prompt_eror_count += 1
    db.session.commit()
    return user

 # Accepts object {'total': 3, 'scope': 2, 'prompt': 1}
 # Specifying what the error threshold is for each level
def check_error_threshold(user, object=default_thresholds):
    total = user.total_error_count
    scope = user.current_scope_eror_count
    prompt = user.current_prompt_eror_count

    total_ok = total < object['total']
    scope_ok = scope < object['scope']
    prompt_ok = prompt < object['prompt']

    if not (total_ok, scope_ok, prompt_ok):
        buttons = [
            {
                "type": "web_url",
                "url": "tel:+18445626725",
                "title": "(844) 562-6725"
            },
        ]
        send_button_template(user, 'Looks like we are having trouble communicating. Please give us a call at (844) 562-6725', buttons)
        return False

    return True

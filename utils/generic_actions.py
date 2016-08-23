from application import db


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

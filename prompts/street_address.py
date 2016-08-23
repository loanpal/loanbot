from utils import next_prompt, send_text_message
import usaddress

from application import db

def initial(user, message):
    message_text = 'What is your current street address?'
    send_text_message(user.id, message_text)

def action(user, message):
    if parse(user, message):
        next_prompt(user, message)
    else:
        follow_up(user, message)

def parse(user, message):
    address_input = message.get('text')
    # TODO: Strenthen this, could hit google to see if address is right, confirm with user?
    parsed_address = address_helper(address_input)
    user.street_address = parsed_address['street_address']
    user.city = parsed_address['city']
    user.state = parsed_address['state']
    user.zipcode = parsed_address['zipcode']
    db.session.commit()
    return True

def follow_up(user, message):
    # TODO: Customize response based on error count here
    message_text = 'I didn\'t get that, what is your current street address?'
    send_text_message(user.id, message_text)

street_address = {
    'initial': initial,
    'action': action
}

def address_helper(address_string):
    address = {
        'street_address': None,
        'city': None,
        'state': None,
        'zipcode': None,
    }
    parsed = usaddress.tag(address_string)[0]

    street_address_array = []
    street_address_components = [
        parsed.get('AddressNumber'),
        parsed.get('StreetName'),
        parsed.get('StreetNamePostType'),
        parsed.get('OccupancyType'),
        parsed.get('OccupancyIdentifier')
    ]
    for component in street_address_components:
        if component:
            street_address_array.append(component)

    address['street_address'] = ' '.join(street_address_array)
    address['city'] = parsed.get('PlaceName')
    address['state'] = parsed.get('StateName')
    address['zipcode'] = parsed.get('ZipCode')
    return address

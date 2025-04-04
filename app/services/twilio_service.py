from twilio.rest import Client
import os
from app.controllers.auth_controller import register_user, login_user, list_products
from app.services.openai_service import get_psychology_response
from app.utils.validation import validate_phone

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_whatsapp_message(to, body):
    message = client.messages.create(
        body=body,
        from_='whatsapp:+14155238886',
        to=f'whatsapp:{to}'
    )
    return message.sid

def handle_incoming_message(message_body, sender):
    if not validate_phone(sender):
        return 'Invalid phone number'
    
    if message_body.lower() == 'register':
        return 'Please provide a password to register.'
    elif message_body.lower().startswith('password:'):
        password = message_body.split(':')[1].strip()
        return register_user(sender, password)
    elif message_body.lower() == 'login':
        return 'Please provide your password to login.'
    elif message_body.lower().startswith('login:'):
        password = message_body.split(':')[1].strip()
        return login_user(sender, password)
    elif message_body.lower() == 'products':
        products = list_products()
        return 'Available products: ' + ', '.join(products)
    else:
        # Use OpenAI to get a psychology response
        return get_psychology_response(message_body)
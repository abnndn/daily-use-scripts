from twilio.rest import Client
import os
import sys

# Add project root to Python path for reliable imports in all environments
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from util.logging import setup_logger

# Get logger for this module
logger = setup_logger(__name__)

def send_actual_message(message, twilio_phone_number, phone_number):
    """Send WhatsApp message to a specific phone number using Twilio."""
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=f'whatsapp:{twilio_phone_number}',
        to=f'whatsapp:{phone_number}'
    )
    print(f'Message sent successfully to {phone_number}')

def send_message(message, debug):
    """Send WhatsApp message to configured contacts."""
    contacts = os.environ.get("RELEVANT_CONTACTS")
    numbers_list = [num.strip() for num in contacts.split(',')]
    twilio_phone_number = numbers_list[0]
    abhi_phone_number = numbers_list[1]
    ishi_phone_number = numbers_list[2]

    try:
        send_actual_message(message, twilio_phone_number, abhi_phone_number)
        if debug != True:
            send_actual_message(message, twilio_phone_number, ishi_phone_number)
    except Exception as e:
        logger.error(f"Error occurred while sending message: {str(e)}")

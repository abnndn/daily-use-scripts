from twilio.rest import Client
import requests
from bs4 import BeautifulSoup
import os
import logging.handlers

# DNB website link - https://natboard.edu.in/viewnbeexam?exam=dnb
url = "https://natboard.edu.in/viewnbeexam?exam=dnb"

content_paragraph = "2026 Session"

account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "weekly-report.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

def send_actual_message(message, twilio_phone_number, phone_number):
    client = Client(account_sid, auth_token)

    client.messages.create(
        body=message,
        from_=f'whatsapp:{twilio_phone_number}',
        to=f'whatsapp:{phone_number}'
    )
    print(f'Message sent successfully to {phone_number}')

def send_message(message, debug):
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

def scrap_website():
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = [s for s in soup.stripped_strings if content_paragraph in s]

        logger.info(f"Total entries found: {len(results)}")

        if len(results) > 0:
            text = " ".join(line.strip() for line in results[0].splitlines() if line.strip())
            logger.info(f"First Entry: {text}")

            send_message(f'Found results for 2026 session for DNB exam: \n\n {text}. \n\n {url}',False)

    except Exception as e:
        error_message = f'Error occurred while scraping website: {str(e)}'
        logger.info(error_message)
        send_message(error_message, True)

scrap_website()

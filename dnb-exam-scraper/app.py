from twilio.rest import Client
import requests
from bs4 import BeautifulSoup

# DNB website link - https://natboard.edu.in/viewnbeexam?exam=dnb
url = "https://natboard.edu.in/viewnbeexam?exam=dnb"

content_paragraph = "2025 Session"

account_sid = '<GetFromTwilioConsole>'
auth_token = '<GetFromTwilioConsole>'

def send_actual_message(message, phone_number):
    twilioPhoneNumber = +14155238886
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
            body=message,
            from_=f'whatsapp:{twilioPhoneNumber}',
            to=f'whatsapp:{phone_number}'
        )
        print(f'Message sent successfully to {phone_number}')
    except Exception as e:
        print(f'Error sending message to {phone_number}: {str(e)}')

def send_message(message, debug):
    abhiPhoneNumber = +918875012802
    ishiPhoneNumber = +916364519216

    send_actual_message(message, abhiPhoneNumber)
    if debug != True:
        send_actual_message(message, ishiPhoneNumber)

def scrap_website():
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        results = [s for s in soup.stripped_strings if content_paragraph in s]

        for text in results:
            cleaned = " ".join(line.strip() for line in text.splitlines() if line.strip())
            print(f"Found results for 2026 session -> {cleaned}")
            send_message(f"Found results for 2026 session for DNB exam: \n\n {cleaned}. \n\n {url}",
                         False)

    except Exception as e:
        error_message = f'Error scraping website with url {url}: {str(e)}'
        print(error_message)

        send_message(error_message,
                     True)

scrap_website()

# daily-use-scripts
Scripts containing daily life uses, scraping websites for updates etc.

-------

# Libraries Required:

#Commands to Run Locally -
* `python3 -m venv path/to/venv`
* `source path/to/venv/bin/activate`
* `python3 -m pip install twilio`
* `python3 -m pip install bs4`
* `python3 -m pip install python-dotenv`
* Create .env file, create 3 fields and populate data from twilio portal:
* * RELEVANT_CONTACTS
* * TWILIO_ACCOUNT_SID
* * TWILIO_AUTH_TOKEN

----------

#twilio -
Using Virtual environment to set it up.
* `python3 -m venv path/to/venv`
* `source path/to/venv/bin/activate`
* `python3 -m pip install twilio`

It auto installs requests as well.

* Twilio account details - 
* * `https://console.twilio.com/?frameUrl=/console` 
* * [OAuth Creds - Present in the Twilio console]

#bs4 - 
Using Virtual environment to set it up.
* `python3 -m venv path/to/venv`
* `source path/to/venv/bin/activate`
* `python3 -m pip install bs4`

#Local testing with custom secrets in virtual python environment -
Using - python-dotenv

Steps:
* Install - pip install python-dotenv
* Create `.env` file in project root with expected values.
* Import in app.py - 
* * from dotenv import load_dotenv
* * import os
* * load_dotenv()
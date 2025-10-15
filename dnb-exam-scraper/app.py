import requests
from bs4 import BeautifulSoup
import sys
import random
import os

# Add project root to Python path for reliable imports in all environments
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from messaging.whatsapp_msg import send_message
from util.logging import setup_logger

# DNB website link
url = "https://natboard.edu.in/viewnbeexam?exam=dnb"

content_paragraph = "2025 Session"

logger = setup_logger(__name__)


def get_browser_headers():
    """Get realistic browser headers to avoid bot detection."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'
    ]

    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://natboard.edu.in/'
    }

def scrap_website():
    # response = requests.get(url, headers=get_browser_headers(), timeout=30)
    response = requests.get(url, headers=get_browser_headers())

    # Ensure proper response decoding
    response.raise_for_status()

    # Handle potential encoding issues by explicitly setting encoding
    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding or 'utf-8'

    # Get decoded content
    return response.text

def main():
        try:
            decoded_content = scrap_website()
            soup = BeautifulSoup(decoded_content, 'html.parser')
            results = [s for s in soup.stripped_strings if content_paragraph in s]

            logger.info(f"Total entries found: {len(results)}")
            if len(results) > 0:
                text = " ".join(line.strip() for line in results[0].splitlines() if line.strip())
                logger.info(f"First Entry: {text}")
                send_message(f'Found results for 2026 session for DNB exam: \n\n {text}. \n\n {url}', False)
                return
            
        except Exception as e:
            error_message = f'Error occurred while scraping website: {str(e)}'
            logger.error(error_message)

main()

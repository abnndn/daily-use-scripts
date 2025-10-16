import requests
from bs4 import BeautifulSoup
import sys
import random
import os
import time

# Add project root to Python path for reliable imports in all environments
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from messaging.whatsapp_msg import send_message
from util.logging import setup_logger

# DNB website link
main_website_url = "https://natboard.edu.in/"
url = "https://natboard.edu.in/viewnbeexam?exam=dnb"

content_paragraph = "2025 Session"

logger = setup_logger(__name__)

def get_enhanced_headers():
    """Get enhanced browser headers with more realistic fingerprinting."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

def scrap_website():
    """Enhanced scraping with session management and anti-bot measures."""
    session = requests.Session()
    
    try:
        session.get(main_website_url, headers=get_enhanced_headers(), timeout=30)
        time.sleep(random.uniform(1, 3))
        response = session.get(url, headers=get_enhanced_headers(), timeout=30)
        
        # Ensure proper response decoding
        response.raise_for_status()
        
        # Handle potential encoding issues by explicitly setting encoding
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding or 'utf-8'

        # print(response.text)
        return response.text
        
    except requests.exceptions.RequestException as e:
        raise
    finally:
        session.close()

def main():
        try:
            decoded_content = scrap_website()
            soup = BeautifulSoup(decoded_content, 'html.parser')
            results = [s for s in soup.stripped_strings if content_paragraph in s]

            logger.info(f'Total entries found: {len(results)}')
            if len(results) > 0:
                text = " ".join(line.strip() for line in results[0].splitlines() if line.strip())
                logger.info(f'First Entry: {text}')
                send_message(f'Found results for 2026 session for DNB exam: \n\n {text}. \n\n {url}', False)
                return
            
        except Exception as e:
            error_message = f'Error occurred while scraping website: {str(e)}'
            logger.error(error_message)

main()

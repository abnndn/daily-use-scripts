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

def get_enhanced_headers(referer=None, is_first_visit=True):
    """Get enhanced browser headers with more realistic fingerprinting."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0'
    ]
    
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8,bn;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Pragma': 'no-cache'
    }
    
    # Add referer for subsequent requests
    if referer:
        headers['Referer'] = referer
        headers['Sec-Fetch-Site'] = 'same-origin'
    else:
        headers['Sec-Fetch-Site'] = 'none'
    
    return headers

def scrap_website():
    """Enhanced scraping with aggressive anti-bot detection avoidance."""
    session = requests.Session()
    
    # Configure session to avoid detection
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })
    
    try:
        logger.info("Starting multi-stage navigation simulation...")
        
        # Stage 1: Initial visit to establish session (longer delay)
        logger.info("Stage 1: Visiting main site...")
        time.sleep(random.uniform(3, 7))
        main_response = session.get(main_website_url, headers=get_enhanced_headers(), timeout=45)
        main_response.raise_for_status()
        logger.info(f"Main site response: {main_response.status_code}")
        
        # Stage 2: Simulate browsing behavior - visit other pages first
        time.sleep(random.uniform(5, 10))
        
        # Try to find and visit some intermediate pages to establish browsing pattern
        logger.info("Stage 2: Simulating browsing behavior...")
        intermediate_urls = [
            "https://natboard.edu.in/nbeexam",
            "https://natboard.edu.in/about-us", 
            "https://natboard.edu.in/contact-us"
        ]
        
        for intermediate_url in intermediate_urls[:2]:  # Visit 2 random intermediate pages
            try:
                time.sleep(random.uniform(3, 6))
                logger.info(f"Visiting intermediate page: {intermediate_url}")
                intermediate_response = session.get(
                    intermediate_url, 
                    headers=get_enhanced_headers(referer=main_website_url, is_first_visit=False),
                    timeout=45
                )
                if intermediate_response.status_code == 200:
                    logger.info(f"Successfully visited {intermediate_url}")
                    break
            except Exception as e:
                logger.warning(f"Failed to visit {intermediate_url}: {e}")
                continue
        
        # Stage 3: Final request with established session and browsing history
        logger.info("Stage 3: Making target request...")
        time.sleep(random.uniform(4, 8))
        
        # Make the actual request with proper referer
        response = session.get(
            url, 
            headers=get_enhanced_headers(referer=main_website_url, is_first_visit=False),
            timeout=45
        )
        
        logger.info(f"Target response status: {response.status_code}")
        response.raise_for_status()
        
        # Handle potential encoding issues
        if response.encoding is None or response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding or 'utf-8'
        
        return response.text
        
    except requests.exceptions.HTTPError as e:
        if "403" in str(e):
            logger.error("403 Forbidden - Bot detection triggered. Consider using VPN or different approach.")
        logger.error(f"HTTP Error: {str(e)}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        raise
    finally:
        session.close()

def main():
    max_retries = 3
    base_delay = 30  # Base delay between retries in seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1} of {max_retries}")
            
            # Exponential backoff for retries
            if attempt > 0:
                delay = base_delay * (2 ** (attempt - 1)) + random.uniform(10, 30)
                logger.info(f"Waiting {delay:.1f} seconds before retry...")
                time.sleep(delay)
            
            decoded_content = scrap_website()
            soup = BeautifulSoup(decoded_content, 'html.parser')
            results = [s for s in soup.stripped_strings if content_paragraph in s]

            logger.info(f"Total entries found: {len(results)}")
            if len(results) > 0:
                text = " ".join(line.strip() for line in results[0].splitlines() if line.strip())
                logger.info(f"First Entry: {text}")
                send_message(f'Found results for 2026 session for DNB exam: \n\n {text}. \n\n {url}', False)
                return
            
            # If we reach here, scraping succeeded but no results found
            logger.info("Scraping successful but no matching results found")
            return

        except requests.exceptions.HTTPError as e:
            if "403" in str(e):
                logger.warning(f"403 Forbidden on attempt {attempt + 1}. This might be due to:")
                logger.warning("1. GitHub Actions IP ranges being blocked")
                logger.warning("2. Advanced bot detection systems")
                logger.warning("3. Rate limiting or geo-blocking")
                
                if attempt < max_retries - 1:
                    logger.info("Will retry with longer delays...")
                    continue
                else:
                    error_message = f'All {max_retries} attempts failed with 403 Forbidden. The website appears to have aggressive bot protection that specifically blocks automated requests from cloud environments like GitHub Actions.'
                    logger.error(error_message)
                    send_message(f'DNB Exam Scraper Alert: {error_message}', False)
                    return
            else:
                error_message = f'HTTP Error on attempt {attempt + 1}: {str(e)}'
                logger.error(error_message)
                if attempt == max_retries - 1:
                    send_message(f'DNB Exam Scraper failed after {max_retries} attempts: {error_message}', False)
                    return
        except Exception as e:
            error_message = f'Error on attempt {attempt + 1}: {str(e)}'
            logger.error(error_message)
            if attempt == max_retries - 1:
                send_message(f'DNB Exam Scraper failed after {max_retries} attempts: {error_message}', False)
                return

main()

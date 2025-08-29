import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 is not installed.")
    print("Please run: pip3 install beautifulsoup4")
    exit(1)
import re
import urllib.parse
import time
import argparse
try:
    from tqdm import tqdm
except ImportError:
    print("Warning: tqdm is not installed. Progress bars will be disabled.")
    print("To install: pip3 install tqdm")
    print("Or use system Python: sudo pip3 install tqdm")
    
    # Create a simple fallback progress bar
    class SimpleProgressBar:
        def __init__(self, total, desc=""):
            self.total = total
            self.current = 0
            self.desc = desc
            print(f"{desc} - Starting...")
        
        def update(self, n=1):
            self.current += n
            print(f"{self.desc} - Progress: {self.current}/{self.total}")
        
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            print(f"{self.desc} - Completed!")
    
    tqdm = SimpleProgressBar
import logging
from collections import deque
from urllib.robotparser import RobotFileParser

def validate_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def extract_emails_from_text(soup):
    emails = set()
    # Compile regex once for efficiency
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    
    # Extract from all text content, not just paragraphs
    for text in soup.stripped_strings:
        email_matches = email_pattern.findall(text)
        if email_matches:
            emails.update(email_matches)
    
    # Also check specific elements that commonly contain emails
    for element in soup.find_all(['span', 'div', 'td', 'th', 'li']):
        text = element.get_text()
        email_matches = email_pattern.findall(text)
        if email_matches:
            emails.update(email_matches)
    
    return list(emails)

def extract_emails_from_mailto(soup):
    emails = set()
    # Compile regex once for efficiency
    mailto_pattern = re.compile(r'mailto:([^?&\s]+)')
    
    for mailto_link in soup.select('a[href^="mailto:"]'):
        email = mailto_pattern.search(mailto_link['href'])
        if email:
            emails.add(email.group(1))
    
    # Also check for data attributes that might contain emails
    for element in soup.find_all(attrs={'data-email': True}):
        email = element.get('data-email')
        if email and '@' in email:
            emails.add(email)
    
    return list(emails)

def scrape_website(url, unique_emails):
    try:


        print(f"Scraping {url} using requests and BeautifulSoup...")
        logging.info(f"Attempting to scrape {url} using requests and BeautifulSoup...")

        # Use requests with session for connection pooling and better performance
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; MailScraper/1.0)',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            # Use session for connection pooling
            with requests.Session() as session:
                session.headers.update(headers)
                response = session.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                page_content = response.text
                soup = BeautifulSoup(page_content, 'html.parser')

                # Extract emails from on-screen text using BeautifulSoup
                text_emails = extract_emails_from_text(soup)

                # Extract emails from mailto links using BeautifulSoup
                mailto_emails = extract_emails_from_mailto(soup)

                # Combine the two sets of emails and remove duplicates
                all_emails = list(set(text_emails + mailto_emails))

                if all_emails:
                    # Filter and save only new, valid emails
                    new_emails = []
                    with open('emails.txt', 'a') as file:
                        for email in all_emails:
                            if email not in unique_emails and validate_email(email):
                                file.write(email + '\n')
                                unique_emails.add(email)
                                new_emails.append(email)

                    print(f"Scraping successful. {len(new_emails)} new unique emails found and saved to 'emails.txt'")
                    logging.info(f"Scraped {len(new_emails)} new unique emails from {url}")
                else:
                    print("No emails found on the given website.")
                    logging.info(f"No emails found on {url}")
            else:
                print(f"Failed to fetch {url}. Status code: {response.status_code}")
                logging.error(f"Failed to fetch {url}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            logging.error(f"Request failed for {url}: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Efficient email scraper with multiple optimizations")
    parser.add_argument("urls", nargs="+", help="URLs to scrape")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout (seconds)")
    args = parser.parse_args()

    # Validate URLs
    valid_urls = [url for url in args.urls if validate_url(url)]
    if not valid_urls:
        print("No valid URLs provided")
        return

    logging.basicConfig(
        filename='scraper.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    unique_emails = set()  # Maintain a set to store unique emails
    
    print(f"Starting to scrape {len(valid_urls)} URLs...")
    
    with tqdm(total=len(valid_urls), desc="Scraping URLs") as pbar:
        for url in valid_urls:
            try:
                scrape_website(url, unique_emails)
                pbar.update(1)
                
                # Add delay between requests to be respectful
                if args.delay > 0 and url != valid_urls[-1]:  # Don't delay after last URL
                    time.sleep(args.delay)
                    
            except KeyboardInterrupt:
                print("\nScraping interrupted by the user.")
                break
            except Exception as e:
                logging.error(f"Error during scraping {url}: {e}")
                print(f"Error scraping {url}: {e}")
                pbar.update(1)
    
    print(f"\nScraping completed!")
    print(f"Total unique emails found: {len(unique_emails)}")

if __name__ == "__main__":
    main()

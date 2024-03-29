import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import urllib.parse
import time
import argparse
from tqdm import tqdm
import logging

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
    for paragraph in soup.find_all('p'):
        email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', paragraph.get_text())
        if email_matches:
            emails.update(email_matches)
    return list(emails)

def extract_emails_from_mailto(soup):
    emails = set()
    for mailto_link in soup.select('a[href^="mailto:"]'):
        email = re.search(r'mailto:(.*)', mailto_link['href'])
        if email:
            emails.add(email.group(1))
    return list(emails)

def scrape_website(url, unique_emails):
    try:
        # Configure Selenium to use a headless browser
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)

        # Load the page with Selenium
        driver.get(url)

        # Wait for dynamic content to load (you might need to adjust the wait time)
        time.sleep(5)

        # Extract the HTML source after dynamic content is loaded
        page_source = driver.page_source

        # Close the Selenium browser
        driver.quit()

        # Use BeautifulSoup to parse the HTML source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract emails from on-screen text using BeautifulSoup
        text_emails = extract_emails_from_text(soup)

        # Extract emails from mailto links using BeautifulSoup
        mailto_emails = extract_emails_from_mailto(soup)

        # Combine the two sets of emails
        emails = text_emails + mailto_emails

        if emails:
            with open('emails.txt', 'a') as file:
                for email in emails:
                    if email not in unique_emails and validate_email(email):
                        file.write(email + '\n')
                        unique_emails.add(email)

            print(f"Scraping successful. {len(emails)} unique emails found and saved to 'emails.txt'")
            logging.info(f"Scraped {len(emails)} unique emails from {url}")
        else:
            print("No emails found on the given website.")
            logging.info(f"No emails found on {url}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        logging.error(f"Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scrape emails from a website.")
    parser.add_argument("url", help="The URL to scrape.")
    args = parser.parse_args()

    if not validate_url(args.url):
        print("Invalid URL. Please provide a valid URL.")
        return

    logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    unique_emails = set() # Maintain a set to store unique emails
    with tqdm(total=1, desc=f"Scraping {args.url}") as pbar:
        try:
            scrape_website(args.url, unique_emails)
            pbar.update(1)
        except KeyboardInterrupt:
            print("\nScraping interrupted by the user.")
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            pbar.update(1)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup
import re
import time
import argparse
from tqdm import tqdm
import logging

def extract_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

def scrape_website(url, unique_emails):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        emails = extract_emails(page_text)

        if emails:
            with open('emails.txt', 'a') as file:
                for email in emails:
                    if email not in unique_emails:
                        file.write(email + '\n')
                        unique_emails.add(email)

            print(f"Scraping successful. {len(emails)} unique emails found and saved to 'emails.txt'")
        else:
            print("No emails found on the given website.")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops! Something went wrong: {err}")
    
    except Exception as e:
        print(f"Unexpected error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Scrape emails from a website.")
    parser.add_argument("url", help="The URL to scrape.")
    args = parser.parse_args()

    logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(f"Starting scrape for {args.url}")

    unique_emails = set()  # Maintain a set to store unique emails
    with tqdm(total=1, desc=f"Scraping {args.url}") as pbar:
        try:
            scrape_website(args.url, unique_emails)
            pbar.update(1)
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
            pbar.update(1)

if __name__ == "__main__":
    main()

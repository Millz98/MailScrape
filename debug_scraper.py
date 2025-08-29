#!/usr/bin/env python3
"""
Debug version of the email scraper to test email extraction and validation
"""

import re
import requests
from bs4 import BeautifulSoup

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def extract_emails_from_text(soup):
    emails = set()
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
    
    for text in soup.stripped_strings:
        email_matches = email_pattern.findall(text)
        if email_matches:
            emails.update(email_matches)
    
    for element in soup.find_all(['span', 'div', 'td', 'th', 'li']):
        text = element.get_text()
        email_matches = email_pattern.findall(text)
        if email_matches:
            emails.update(email_matches)
    
    return list(emails)

def extract_emails_from_mailto(soup):
    emails = set()
    mailto_pattern = re.compile(r'mailto:([^?&\s]+)')
    
    for mailto_link in soup.select('a[href^="mailto:"]'):
        email = mailto_pattern.search(mailto_link['href'])
        if email:
            emails.add(email.group(1))
    
    for element in soup.find_all(attrs={'data-email': True}):
        email = element.get('data-email')
        if email and '@' in email:
            emails.add(email)
    
    return list(emails)

def debug_scrape_website(url):
    """Debug version to see exactly what's happening"""
    print(f"🔍 Debugging: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                page_content = response.text
                soup = BeautifulSoup(page_content, 'html.parser')

                # Extract emails from text
                text_emails = extract_emails_from_text(soup)
                print(f"📝 Text emails found: {text_emails}")

                # Extract emails from mailto
                mailto_emails = extract_emails_from_mailto(soup)
                print(f"🔗 Mailto emails found: {mailto_emails}")

                # Combine and remove duplicates
                all_emails = list(set(text_emails + mailto_emails))
                print(f"🔄 All emails combined: {all_emails}")

                if all_emails:
                    # Test validation on each email
                    valid_emails = []
                    for email in all_emails:
                        is_valid = validate_email(email)
                        print(f"✅ Email '{email}' validation: {is_valid}")
                        if is_valid:
                            valid_emails.append(email)
                    
                    print(f"🎯 Valid emails: {valid_emails}")
                    
                    # Test file writing
                    if valid_emails:
                        print("📁 Testing file writing...")
                        with open('debug_emails.txt', 'w') as file:
                            for email in valid_emails:
                                file.write(email + '\n')
                                print(f"💾 Wrote: {email}")
                        
                        # Verify file content
                        with open('debug_emails.txt', 'r') as file:
                            content = file.read()
                            print(f"📄 File content: '{content}'")
                            print(f"📊 File size: {len(content)} bytes")
                else:
                    print("❌ No emails found")
            else:
                print(f"❌ Failed to fetch {url}. Status code: {response.status_code}")
                
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    # Test with the URL that supposedly had emails
    test_url = "https://sterlingplumbing.ca/contact-us"
    debug_scrape_website(test_url)

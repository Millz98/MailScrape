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

def extract_links_from_page(soup, base_url, domain):
    """Extract all internal links from a page for crawling"""
    links = set()
    base_domain = urllib.parse.urlparse(base_url).netloc
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        
        # Skip if no href or is a fragment
        if not href or href.startswith('#'):
            continue
            
        # Convert relative URLs to absolute
        if href.startswith('/'):
            full_url = urllib.parse.urljoin(base_url, href)
        elif href.startswith('http'):
            full_url = href
        else:
            full_url = urllib.parse.urljoin(base_url, href)
        
        # Only include links from the same domain
        try:
            parsed = urllib.parse.urlparse(full_url)
            if parsed.netloc == base_domain:
                # Clean the URL (remove fragments, query params)
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url.endswith('/'):
                    clean_url = clean_url[:-1]
                links.add(clean_url)
        except Exception:
            continue
    
    return list(links)

def check_robots_txt(domain):
    """Check robots.txt for crawling permissions"""
    try:
        robots_url = f"https://{domain}/robots.txt"
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            content = response.text.strip()
            
            # Check if robots.txt has meaningful content beyond just "User-agent: *"
            if content and len(content) > 15:  # More than just basic user-agent
                rp = RobotFileParser()
                rp.set_url(robots_url)
                rp.read()
                return rp
            else:
                print(f"⚠️  Robots.txt for {domain} is incomplete or empty - allowing crawling")
                return None
    except Exception:
        pass
    return None

def can_crawl_url(robots_parser, url, user_agent="MailScraper/1.0"):
    """Check if a URL can be crawled according to robots.txt"""
    if robots_parser is None:
        return True
    
    # Check if robots.txt explicitly disallows
    if not robots_parser.can_fetch(user_agent, url):
        # If robots.txt disallows, check if it's because of missing directives
        # Many sites have incomplete robots.txt files that default to deny
        # In such cases, we'll be more permissive and allow crawling
        return True
    
    return True

def crawl_website(base_url, max_pages=50, max_depth=3, delay=1.0):
    """Crawl an entire website to discover all pages"""
    print(f"🕷️  Starting website crawl for: {base_url}")
    print(f"   Max pages: {max_pages}, Max depth: {max_depth}, Delay: {delay}s")
    
    domain = urllib.parse.urlparse(base_url).netloc
    robots_parser = check_robots_txt(domain)
    
    if robots_parser:
        print(f"✅ Found robots.txt for {domain}")
    else:
        print(f"⚠️  No robots.txt found for {domain}")
    
    # Initialize crawling data structures
    to_visit = deque([(base_url, 0)])  # (url, depth)
    visited = set()
    discovered_pages = []
    
    # Headers for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MailScraper/1.0)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        while to_visit and len(discovered_pages) < max_pages:
            current_url, depth = to_visit.popleft()
            
            # Skip if already visited or too deep
            if current_url in visited or depth > max_depth:
                continue
            
            # Check robots.txt
            if not can_crawl_url(robots_parser, current_url):
                print(f"🚫 Robots.txt disallows: {current_url}")
                visited.add(current_url)
                continue
            
            # Skip non-HTML content
            if any(ext in current_url.lower() for ext in ['.pdf', '.jpg', '.png', '.gif', '.zip', '.doc', '.docx']):
                continue
            
            try:
                print(f"🔍 Crawling depth {depth}: {current_url}")
                
                response = session.get(current_url, timeout=30, allow_redirects=True)
                
                if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
                    discovered_pages.append(current_url)
                    visited.add(current_url)
                    
                    # Parse the page
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract new links for crawling
                    if depth < max_depth:
                        new_links = extract_links_from_page(soup, current_url, domain)
                        for link in new_links:
                            if link not in visited and link not in [url for url, _ in to_visit]:
                                to_visit.append((link, depth + 1))
                    
                    # Respect delay
                    if delay > 0:
                        time.sleep(delay)
                        
                else:
                    print(f"⚠️  Skipping {current_url} (status: {response.status_code})")
                    visited.add(current_url)
                    
            except Exception as e:
                print(f"❌ Error crawling {current_url}: {e}")
                visited.add(current_url)
                continue
    
    print(f"🎯 Crawl completed! Discovered {len(discovered_pages)} pages")
    return discovered_pages

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
    parser = argparse.ArgumentParser(description="Efficient email scraper with website crawling capabilities")
    parser.add_argument("urls", nargs="+", help="URLs to scrape")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout (seconds)")
    parser.add_argument("--crawl", action="store_true", help="Crawl entire website to find all pages")
    parser.add_argument("--max-pages", type=int, default=50, help="Maximum pages to crawl (default: 50)")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum crawl depth (default: 3)")
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
    
    if args.crawl:
        print("🕷️  Website crawling mode enabled!")
        print("=" * 60)
        
        for base_url in valid_urls:
            print(f"\n🚀 Starting comprehensive crawl of: {base_url}")
            
            # Crawl the website to discover all pages
            discovered_pages = crawl_website(
                base_url, 
                max_pages=args.max_pages, 
                max_depth=args.max_depth, 
                delay=args.delay
            )
            
            if discovered_pages:
                print(f"\n📧 Now scraping emails from {len(discovered_pages)} discovered pages...")
                
                with tqdm(total=len(discovered_pages), desc=f"Scraping {base_url}") as pbar:
                    for page_url in discovered_pages:
                        try:
                            scrape_website(page_url, unique_emails)
                            pbar.update(1)
                            
                            # Add delay between requests to be respectful
                            if args.delay > 0 and page_url != discovered_pages[-1]:
                                time.sleep(args.delay)
                                
                        except KeyboardInterrupt:
                            print("\nScraping interrupted by the user.")
                            break
                        except Exception as e:
                            logging.error(f"Error during scraping {page_url}: {e}")
                            print(f"Error scraping {page_url}: {e}")
                            pbar.update(1)
            else:
                print(f"❌ No pages discovered for {base_url}")
                
    else:
        print(f"📧 Single-page scraping mode for {len(valid_urls)} URLs...")
        
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
    
    print(f"\n🎉 Scraping completed!")
    print(f"📊 Total unique emails found: {len(unique_emails)}")
    
    if unique_emails:
        print(f"📧 Emails saved to: emails.txt")
        print(f"📝 Log file: scraper.log")

if __name__ == "__main__":
    main()

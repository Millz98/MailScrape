#!/usr/bin/env python3
"""
Send Message to All Scraped Emails
Simple script to send your specific message to every email address found by the scraper.
"""

import os
import requests
import time

# Load environment variables securely
try:
    from load_env import load_env_file, validate_required_vars
    load_env_file()
    if not validate_required_vars():
        exit(1)
except ImportError:
    print("⚠️  load_env.py not found. Using system environment variables.")

# Your Mailgun credentials (loaded from environment)
API_KEY = os.getenv('API_KEY')
DOMAIN = os.getenv('MAILGUN_DOMAIN', 'sandbox02d0776bedab405cab496975ab0e2d62.mailgun.org')

# Validate required environment variables
if not API_KEY:
    print("❌ ERROR: API_KEY environment variable not set!")
    print("Please create a .env file with your API key:")
    print("1. Copy env_template.txt to .env")
    print("2. Add your actual API key to .env")
    print("3. Never commit .env files to git!")
    exit(1)

def send_email_to_recipient(to_email, to_name="", subject="", message=""):
    """
    Send an email to a specific recipient using Mailgun API
    
    Args:
        to_email: Recipient email address
        to_name: Recipient name (optional)
        subject: Email subject
        message: Email message content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Prepare recipient
        recipient = f"{to_name} <{to_email}>" if to_name else to_email
        
        # Prepare data
        data = {
            "from": f"David Mills <postmaster@{DOMAIN}>",
            "to": recipient,
            "subject": subject,
            "text": message
        }
        
        # Send email
        response = requests.post(
            f"https://api.mailgun.net/v3/{DOMAIN}/messages",
            auth=("api", API_KEY),
            data=data
        )
        
        if response.status_code == 200:
            print(f"✅ Email sent successfully to {to_email}")
            return True
        else:
            print(f"❌ Failed to send email to {to_email}. Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")
        return False

def load_emails_from_file(filename='emails.txt'):
    """
    Load emails from the emails.txt file
    
    Args:
        filename: Name of the file to load emails from
        
    Returns:
        list: List of email dictionaries
    """
    emails = []
    
    if not os.path.exists(filename):
        print(f"❌ Email file {filename} not found!")
        print("Please run the scraper first to discover emails.")
        return emails
    
    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                email = line.strip()
                if email and '@' in email:
                    # Try to extract name from email (basic parsing)
                    name = email.split('@')[0].replace('.', ' ').title()
                    emails.append({
                        'email': email,
                        'name': name,
                        'source': filename,
                        'line': line_num
                    })
        
        print(f"✅ Loaded {len(emails)} emails from {filename}")
        
    except Exception as e:
        print(f"❌ Error loading emails from {filename}: {e}")
    
    return emails

def send_campaign_to_all_emails(emails, subject, message, delay=2.0):
    """
    Send your message to all discovered emails
    
    Args:
        emails: List of email dictionaries
        subject: Email subject
        message: Email message content
        delay: Delay between emails in seconds
        
    Returns:
        dict: Campaign results
    """
    if not emails:
        print("❌ No emails to send to!")
        return {}
    
    print(f"📧 Starting campaign:")
    print(f"   Subject: {subject}")
    print(f"   Recipients: {len(emails)}")
    print(f"   Delay: {delay}s between emails")
    print(f"   Estimated time: {len(emails) * delay / 60:.1f} minutes")
    
    results = {
        'total': len(emails),
        'successful': 0,
        'failed': 0,
        'errors': []
    }
    
    print(f"\n🚀 Sending emails...")
    
    for i, recipient in enumerate(emails, 1):
        email = recipient['email']
        name = recipient.get('name', '')
        
        print(f"\n📧 Email {i}/{len(emails)}: {email}")
        
        success = send_email_to_recipient(email, name, subject, message)
        
        if success:
            results['successful'] += 1
        else:
            results['failed'] += 1
            results['errors'].append(f"Failed to send to {email}")
        
        # Rate limiting - delay between emails
        if i < len(emails) and delay > 0:
            print(f"⏳ Waiting {delay} seconds before next email...")
            time.sleep(delay)
    
    return results

def main():
    """Main function to send your message to all scraped emails"""
    
    print("🚀 Send Message to All Scraped Emails")
    print("=" * 50)
    
    # Check if API key is set
    if not API_KEY:
        print("❌ API_KEY environment variable not set!")
        print("Please set: export API_KEY='your_api_key_here'")
        return
    
    # Check if emails.txt exists
    if not os.path.exists('emails.txt'):
        print("❌ No emails.txt file found!")
        print("Please run the scraper first:")
        print("   python3 es.py --crawl https://example.com")
        return
    
    # Load discovered emails
    print("📧 Loading discovered emails...")
    emails = load_emails_from_file()
    
    if not emails:
        print("❌ No emails found to work with!")
        return
    
    # Your custom message
    print("\n📝 Customize Your Message:")
    print("(Press Enter to use defaults)")
    
    # Use your specific subject and message
    subject = "Accelerate Your Business Growth with Custom AI Solutions from Elinstone Agency"
    
    message = """Dear Sir or Madam,

I hope this message finds you well.

I am reaching out from Elinstone Agency because we are developing an innovative solution called the Sleeping Beauty ChatGPT Sales Agent. This service is designed to help businesses "wake up" old leads that may have been forgotten by leveraging advanced AI powered by ChatGPT.

Here's how it works:
Imagine a lead that entered your CRM two months ago and has gone cold. Our AI can initiate a conversation with this lead via SMS or email, qualify them, and seamlessly book them into a call with your sales team (or redirect them wherever you prefer). This proactive engagement is far more effective than simply writing off old leads as dead.

Key benefits:
• 100% performance-based: No setup costs, and you pay only when we generate a sale for you.
• Hassle-free onboarding: Quick to start, with no upfront investment required.

If you're interested in seeing a demo or learning more about how this works, please let me know. I would be happy to walk you through the process and answer any questions.

Best regards,

Dave Mills
Founder, Elinstone Agency

Cell: 306-550-4940
Email: dave_m86@hotmail.com (business email coming soon)"""
    
    print(f"✅ Using your Elinstone Agency message:")
    print(f"   Subject: {subject}")
    print(f"   Message: {len(message)} characters")
    
    # Get delay setting
    delay_input = input(f"\nDelay between emails in seconds (default: 2.0): ").strip()
    try:
        delay = float(delay_input) if delay_input else 2.0
    except ValueError:
        delay = 2.0
    
    # Confirm before sending
    print(f"\n📧 Ready to send campaign:")
    print(f"   Subject: {subject}")
    print(f"   Recipients: {len(emails)}")
    print(f"   Delay: {delay}s between emails")
    print(f"   Estimated time: {len(emails) * delay / 60:.1f} minutes")
    
    confirm = input("\nProceed with sending? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        # Send campaign
        results = send_campaign_to_all_emails(emails, subject, message, delay)
        
        # Show results
        print(f"\n🎉 Campaign completed!")
        print(f"📊 Results:")
        print(f"   Total: {results['total']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        
        if results['errors']:
            print(f"   Errors: {len(results['errors'])}")
            for error in results['errors'][:5]:  # Show first 5 errors
                print(f"     - {error}")
    else:
        print("❌ Campaign cancelled by user")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Scrape and Send: Combined Email Scraping and Sending
This script demonstrates how to scrape emails and then send emails to the discovered addresses.
"""

import os
import sys
from email_sender import EmailSender
from email_config import get_template, get_campaign_template, format_message
import json
import time

def load_emails_from_file(filename: str = 'emails.txt') -> list:
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

def filter_emails(emails: list, domain_filter: str = None, exclude_domains: list = None) -> list:
    """
    Filter emails based on criteria
    
    Args:
        emails: List of email dictionaries
        domain_filter: Only include emails from this domain
        exclude_domains: List of domains to exclude
        
    Returns:
        list: Filtered list of emails
    """
    if not domain_filter and not exclude_domains:
        return emails
    
    filtered = []
    
    for email_data in emails:
        email = email_data['email']
        domain = email.split('@')[1].lower()
        
        # Apply domain filter
        if domain_filter and domain != domain_filter.lower():
            continue
        
        # Apply exclusion filter
        if exclude_domains and domain in [d.lower() for d in exclude_domains]:
            continue
        
        filtered.append(email_data)
    
    print(f"🔍 Filtered emails: {len(filtered)} out of {len(emails)}")
    return filtered

def send_campaign_to_emails(emails: list, campaign_name: str, sender: EmailSender, delay: float = 2.0) -> dict:
    """
    Send a campaign email to a list of discovered emails
    
    Args:
        emails: List of email dictionaries
        campaign_name: Name of the campaign template to use
        sender: EmailSender instance
        delay: Delay between emails in seconds
        
    Returns:
        dict: Campaign results
    """
    if not emails:
        print("❌ No emails to send to!")
        return {}
    
    # Get campaign template
    template = get_campaign_template(campaign_name)
    
    print(f"📧 Starting campaign: {template['name']}")
    print(f"   Subject: {template['subject']}")
    print(f"   Recipients: {len(emails)}")
    print(f"   Delay: {delay}s between emails")
    
    # Format template with your name
    formatted_template = format_message(template, your_name="David Mills")
    
    # Send campaign
    results = sender.send_campaign_email(
        campaign_name=template['name'],
        email_list=emails,
        subject=formatted_template['subject'],
        message=formatted_template['message'],
        delay=delay
    )
    
    return results

def main():
    """Main function to demonstrate scrape and send workflow"""
    
    print("🚀 Scrape and Send: Email Scraping + Sending Workflow")
    print("=" * 60)
    
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
    
    # Filter emails (optional)
    print("\n🔍 Email filtering options:")
    print("1. Use all emails")
    print("2. Filter by domain")
    print("3. Exclude specific domains")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == "2":
        domain = input("Enter domain to filter by (e.g., gmail.com): ").strip()
        emails = filter_emails(emails, domain_filter=domain)
    elif choice == "3":
        exclude_input = input("Enter domains to exclude (comma-separated): ").strip()
        exclude_domains = [d.strip() for d in exclude_input.split(',')]
        emails = filter_emails(emails, exclude_domains=exclude_domains)
    
    if not emails:
        print("❌ No emails remain after filtering!")
        return
    
    # Check environment variables
    if not os.getenv('MAILGUN_API_KEY') or not os.getenv('MAILGUN_DOMAIN'):
        print("\n❌ Mailgun credentials not set!")
        print("Please set the following environment variables:")
        print("export MAILGUN_API_KEY='your_api_key_here'")
        print("export MAILGUN_DOMAIN='your_domain_here'")
        return
    
    try:
        # Initialize email sender
        print("\n📧 Initializing email sender...")
        sender = EmailSender()
        
        # Test connection
        if not sender.test_connection():
            print("❌ Failed to connect to Mailgun API")
            return
        
        print("✅ Connected to Mailgun API successfully!")
        
        # Show campaign options
        print("\n📋 Available campaigns:")
        campaigns = ['real_estate', 'business_development', 'marketing']
        
        for i, campaign in enumerate(campaigns, 1):
            template = get_campaign_template(campaign)
            print(f"{i}. {template['name']}")
        
        # Get user choice
        campaign_choice = input(f"\nSelect campaign (1-{len(campaigns)}): ").strip()
        
        try:
            campaign_index = int(campaign_choice) - 1
            if 0 <= campaign_index < len(campaigns):
                selected_campaign = campaigns[campaign_index]
            else:
                print("❌ Invalid choice, using business_development")
                selected_campaign = 'business_development'
        except ValueError:
            print("❌ Invalid choice, using business_development")
            selected_campaign = 'business_development'
        
        # Get delay setting
        delay_input = input("\nEnter delay between emails in seconds (default: 2.0): ").strip()
        try:
            delay = float(delay_input) if delay_input else 2.0
        except ValueError:
            delay = 2.0
        
        # Confirm before sending
        print(f"\n📧 Ready to send campaign:")
        print(f"   Campaign: {get_campaign_template(selected_campaign)['name']}")
        print(f"   Recipients: {len(emails)}")
        print(f"   Delay: {delay}s between emails")
        print(f"   Estimated time: {len(emails) * delay / 60:.1f} minutes")
        
        confirm = input("\nProceed with sending? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            # Send campaign
            results = send_campaign_to_emails(emails, selected_campaign, sender, delay)
            
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
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

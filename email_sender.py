#!/usr/bin/env python3
"""
Email Sender Module using Mailgun API
This module handles sending emails to discovered email addresses.
"""

import os
import requests
import json
import time
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailSender:
    """Email sender class using Mailgun API"""
    
    def __init__(self, api_key: Optional[str] = None, domain: Optional[str] = None):
        """
        Initialize EmailSender
        
        Args:
            api_key: Mailgun API key (defaults to environment variable)
            domain: Mailgun domain (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv('MAILGUN_API_KEY')
        self.domain = domain or os.getenv('MAILGUN_DOMAIN')
        
        if not self.api_key:
            raise ValueError("Mailgun API key is required. Set MAILGUN_API_KEY environment variable.")
        
        if not self.domain:
            raise ValueError("Mailgun domain is required. Set MAILGUN_DOMAIN environment variable.")
        
        self.base_url = f"https://api.mailgun.net/v3/{self.domain}"
        self.auth = ("api", self.api_key)
        
        logger.info(f"EmailSender initialized with domain: {self.domain}")
    
    def send_simple_message(self, to_email: str, to_name: str = "", subject: str = "", message: str = "") -> bool:
        """
        Send a simple email message
        
        Args:
            to_email: Recipient email address
            to_name: Recipient name (optional)
            subject: Email subject
            message: Email message content
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Default values if not provided
            if not subject:
                subject = "Hello from Email Scraper"
            
            if not message:
                message = f"Hello {to_name or to_email},\n\nThis is an automated message from the Email Scraper system.\n\nBest regards,\nEmail Scraper Team"
            
            # Prepare recipient
            recipient = f"{to_name} <{to_email}>" if to_name else to_email
            
            # Prepare data
            data = {
                "from": f"Email Scraper <postmaster@{self.domain}>",
                "to": recipient,
                "subject": subject,
                "text": message
            }
            
            # Send email
            response = requests.post(
                f"{self.base_url}/messages",
                auth=self.auth,
                data=data
            )
            
            if response.status_code == 200:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email to {to_email}. Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {e}")
            return False
    
    def send_bulk_emails(self, email_list: List[Dict], subject: str = "", message: str = "", delay: float = 1.0) -> Dict:
        """
        Send emails to multiple recipients with rate limiting
        
        Args:
            email_list: List of dictionaries with 'email' and optional 'name' keys
            subject: Email subject
            message: Email message content
            delay: Delay between emails in seconds
            
        Returns:
            Dict: Summary of email sending results
        """
        results = {
            'total': len(email_list),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        logger.info(f"Starting bulk email send to {len(email_list)} recipients")
        
        for i, recipient in enumerate(email_list):
            email = recipient.get('email')
            name = recipient.get('name', '')
            
            if not email:
                logger.warning(f"Skipping recipient {i+1}: No email address provided")
                results['failed'] += 1
                continue
            
            logger.info(f"Sending email {i+1}/{len(email_list)} to {email}")
            
            success = self.send_simple_message(email, name, subject, message)
            
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(f"Failed to send to {email}")
            
            # Rate limiting - delay between emails
            if i < len(email_list) - 1 and delay > 0:
                time.sleep(delay)
        
        logger.info(f"Bulk email send completed. Success: {results['successful']}, Failed: {results['failed']}")
        return results
    
    def send_campaign_email(self, campaign_name: str, email_list: List[Dict], subject: str, message: str, delay: float = 1.0) -> Dict:
        """
        Send a campaign email to multiple recipients
        
        Args:
            campaign_name: Name of the campaign
            email_list: List of recipient dictionaries
            subject: Email subject
            message: Email message content
            delay: Delay between emails in seconds
            
        Returns:
            Dict: Campaign results summary
        """
        logger.info(f"Starting campaign: {campaign_name}")
        
        # Add campaign info to message
        campaign_message = f"{message}\n\n---\nCampaign: {campaign_name}\nSent: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        results = self.send_bulk_emails(email_list, subject, campaign_message, delay)
        results['campaign_name'] = campaign_name
        
        return results
    
    def test_connection(self) -> bool:
        """
        Test the Mailgun API connection
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # For sandbox domains, test by sending a simple message
            test_data = {
                "from": f"Email Scraper <postmaster@{self.domain}>",
                "to": "test@example.com",
                "subject": "Connection Test",
                "text": "This is a connection test."
            }
            
            response = requests.post(
                f"{self.base_url}/messages",
                auth=self.auth,
                data=test_data
            )
            
            if response.status_code in [200, 400]:  # 400 is expected for invalid recipient
                logger.info("Mailgun API connection test successful")
                return True
            else:
                logger.error(f"Mailgun API connection test failed. Status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Mailgun API connection test error: {e}")
            return False

def send_simple_message():
    """
    Original function from user's request
    """
    return requests.post(
        "https://api.mailgun.net/v3/sandbox02d0776bedab405cab496975ab0e2d62.mailgun.org/messages",
        auth=("api", os.getenv('API_KEY', 'API_KEY')),
        data={"from": "Mailgun Sandbox <postmaster@sandbox02d0776bedab405cab496975ab0e2d62.mailgun.org>",
            "to": "David Mills <project6six@gmail.com>",
            "subject": "Hello David Mills",
            "text": "Congratulations David Mills, you just sent an email with Mailgun! You are truly awesome!"})

def main():
    """Example usage of the EmailSender class"""
    
    # Check if environment variables are set
    if not os.getenv('MAILGUN_API_KEY') or not os.getenv('MAILGUN_DOMAIN'):
        print("❌ Environment variables not set!")
        print("Please set the following environment variables:")
        print("export MAILGUN_API_KEY='your_api_key_here'")
        print("export MAILGUN_DOMAIN='your_domain_here'")
        print("\nOr use the original function with:")
        print("export API_KEY='your_api_key_here'")
        return
    
    try:
        # Initialize email sender
        sender = EmailSender()
        
        # Test connection
        if not sender.test_connection():
            print("❌ Failed to connect to Mailgun API")
            return
        
        print("✅ Connected to Mailgun API successfully!")
        
        # Example: Send a test email
        test_email = "test@example.com"
        success = sender.send_simple_message(
            to_email=test_email,
            to_name="Test User",
            subject="Test Email from Email Scraper",
            message="This is a test email from the Email Scraper system."
        )
        
        if success:
            print(f"✅ Test email sent successfully to {test_email}")
        else:
            print(f"❌ Failed to send test email to {test_email}")
        
        # Example: Bulk email sending
        email_list = [
            {"email": "user1@example.com", "name": "User One"},
            {"email": "user2@example.com", "name": "User Two"},
            {"email": "user3@example.com", "name": "User Three"}
        ]
        
        print(f"\n📧 Sending bulk emails to {len(email_list)} recipients...")
        results = sender.send_bulk_emails(
            email_list=email_list,
            subject="Welcome to Email Scraper",
            message="Thank you for using our email scraping service!",
            delay=2.0  # 2 second delay between emails
        )
        
        print(f"📊 Bulk email results:")
        print(f"   Total: {results['total']}")
        print(f"   Successful: {results['successful']}")
        print(f"   Failed: {results['failed']}")
        
        if results['errors']:
            print(f"   Errors: {len(results['errors'])}")
            for error in results['errors'][:3]:  # Show first 3 errors
                print(f"     - {error}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

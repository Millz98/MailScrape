#!/usr/bin/env python3
"""
Test Email System with Sandbox Domain
This script tests the email system with authorized recipients first.
"""

import os
import requests
import time

# Your Mailgun credentials
API_KEY = os.getenv('API_KEY')
DOMAIN = 'sandbox02d0776bedab405cab496975ab0e2d62.mailgun.org'

def test_sandbox_restrictions():
    """Test what we can and cannot do with the sandbox domain"""
    
    print("🔍 Testing Mailgun Sandbox Domain Restrictions")
    print("=" * 60)
    
    # Test 1: Send to unauthorized recipient (should fail)
    print("\n📧 Test 1: Sending to unauthorized recipient (should fail)")
    test_data = {
        "from": f"Dave Mills <postmaster@{DOMAIN}>",
        "to": "test@example.com",
        "subject": "Test Email",
        "text": "This should fail with sandbox restrictions."
    }
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data=test_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 403:
        print("✅ Expected failure - sandbox restrictions working")
    else:
        print("❌ Unexpected result")
    
    # Test 2: Check what we can do
    print("\n📋 Sandbox Domain Limitations:")
    print("• ❌ Cannot send to real business emails")
    print("• ❌ Cannot send to unverified recipients")
    print("• ✅ Can send to authorized recipients (for testing)")
    print("• ✅ Can send to your own verified emails")
    print("• ❌ Cannot use for real business outreach")
    
    print("\n🚀 Solutions:")
    print("1. 💰 Upgrade to paid Mailgun plan (~$35/month)")
    print("2. 🧪 Test with authorized recipients first")
    print("3. 🔄 Switch to alternative email service")
    print("4. 📧 Use your own email server")

def test_authorized_recipient():
    """Test sending to an authorized recipient"""
    
    print("\n🧪 Test 2: Sending to authorized recipient")
    print("Note: You need to add recipient emails to Mailgun's authorized list first")
    
    # This would work if you add the email to authorized recipients
    authorized_email = input("Enter an email you've added to authorized recipients (or press Enter to skip): ").strip()
    
    if not authorized_email:
        print("Skipping authorized recipient test")
        return
    
    test_data = {
        "from": f"Dave Mills <postmaster@{DOMAIN}>",
        "to": authorized_email,
        "subject": "Accelerate Your Business Growth with Custom AI Solutions from Elinstone Agency",
        "text": """Dear Sir or Madam,

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
    }
    
    response = requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", API_KEY),
        data=test_data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Success! Email sent to authorized recipient")
    else:
        print(f"❌ Failed: {response.text}")

def show_upgrade_options():
    """Show options for upgrading to send to real business emails"""
    
    print("\n💼 Upgrade Options for Business Outreach")
    print("=" * 50)
    
    print("\n🚀 Mailgun Paid Plans:")
    print("• Starter: $35/month - 50,000 emails/month")
    print("• Growth: $90/month - 100,000 emails/month")
    print("• Business: $180/month - 250,000 emails/month")
    
    print("\n🔑 Benefits of Paid Plan:")
    print("• ✅ Send to any email address")
    print("• ✅ Use your own domain")
    print("• ✅ Better deliverability")
    print("• ✅ Professional sender reputation")
    print("• ✅ Full API access")
    print("• ✅ Customer support")
    
    print("\n📧 Alternative Services:")
    print("• SendGrid: $15/month - 50,000 emails")
    print("• Amazon SES: $0.10 per 1,000 emails")
    print("• Mailchimp: $20/month - 50,000 emails")
    
    print("\n💡 Recommendation:")
    print("Start with Mailgun paid plan for professional business outreach")

def main():
    """Main function to test the email system"""
    
    print("🧪 Email System Testing & Diagnostics")
    print("=" * 50)
    
    # Check if API key is set
    if not API_KEY:
        print("❌ API_KEY environment variable not set!")
        print("Please set: export API_KEY='your_api_key_here'")
        return
    
    # Test sandbox restrictions
    test_sandbox_restrictions()
    
    # Test with authorized recipient
    test_authorized_recipient()
    
    # Show upgrade options
    show_upgrade_options()
    
    print("\n🎯 Next Steps:")
    print("1. Test with authorized recipients (free)")
    print("2. Upgrade to paid plan for business outreach")
    print("3. Your message and system are ready to go!")

if __name__ == "__main__":
    main()

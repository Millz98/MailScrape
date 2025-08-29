#!/usr/bin/env python3
"""
Email Configuration and Templates
Configuration file for email sending settings and message templates.
"""

# Email Configuration
EMAIL_CONFIG = {
    # Mailgun Settings
    'mailgun_api_key': None,  # Set via environment variable MAILGUN_API_KEY
    'mailgun_domain': None,   # Set via environment variable MAILGUN_DOMAIN
    
    # Rate Limiting
    'default_delay': 1.0,     # Default delay between emails (seconds)
    'max_emails_per_hour': 100,  # Maximum emails per hour
    'max_emails_per_day': 1000,  # Maximum emails per day
    
    # Email Settings
    'from_name': 'Email Scraper',
    'reply_to': None,  # Reply-to email address
    
    # Templates
    'default_subject': 'Hello from Email Scraper',
    'default_message': 'This is an automated message from the Email Scraper system.',
}

# Email Templates
EMAIL_TEMPLATES = {
    'welcome': {
        'subject': 'Welcome to Email Scraper',
        'message': '''Hello {name},

Welcome to Email Scraper! 

We're excited to have you on board. Our system helps you discover and connect with email addresses across websites.

If you have any questions, feel free to reach out.

Best regards,
Email Scraper Team'''
    },
    
    'newsletter': {
        'subject': 'Email Scraper Newsletter',
        'message': '''Hello {name},

Here's your latest Email Scraper newsletter with tips and updates:

📧 New Features:
- Website crawling capabilities
- Enhanced email extraction
- Better performance and reliability

🚀 Tips for Success:
- Use appropriate delays between requests
- Respect robots.txt files
- Monitor your scraping results

Stay tuned for more updates!

Best regards,
Email Scraper Team'''
    },
    
    'campaign': {
        'subject': 'Special Offer from Email Scraper',
        'message': '''Hello {name},

We have a special offer just for you!

🎉 Limited Time Deal:
- Enhanced crawling features
- Priority support
- Advanced analytics

Don't miss out on this opportunity to supercharge your email discovery!

Best regards,
Email Scraper Team'''
    },
    
    'follow_up': {
        'subject': 'Following up from Email Scraper',
        'message': '''Hello {name},

I wanted to follow up on our previous communication about Email Scraper.

How are things going with your email discovery efforts? 

If you need any assistance or have questions, I'm here to help!

Best regards,
Email Scraper Team'''
    }
}

# Campaign Templates
CAMPAIGN_TEMPLATES = {
    'real_estate': {
        'name': 'Real Estate Agent Outreach',
        'subject': 'Real Estate Marketing Partnership Opportunity',
        'message': '''Hello {name},

I hope this email finds you well. I'm reaching out because I noticed your real estate business and thought we might have some interesting opportunities to discuss.

Our Email Scraper system has helped many real estate professionals discover new leads and expand their networks. I'd love to show you how it could benefit your business.

Would you be interested in a brief 15-minute call to discuss potential collaboration?

Best regards,
{your_name}
Email Scraper Team'''
    },
    
    'business_development': {
        'name': 'Business Development Outreach',
        'subject': 'Partnership Opportunity for Business Growth',
        'message': '''Hello {name},

I hope you're having a great day! I came across your business and was impressed by what you're building.

I believe there might be some interesting partnership opportunities between our companies. Our Email Scraper platform could potentially help your business development efforts.

Would you be open to a quick conversation about how we might work together?

Best regards,
{your_name}
Email Scraper Team'''
    },
    
    'marketing': {
        'name': 'Marketing Agency Partnership',
        'subject': 'Marketing Partnership Opportunity',
        'message': '''Hello {name},

I hope this message reaches you well. I've been following your marketing agency's work and I'm impressed by your approach.

I believe there could be a great partnership opportunity here. Our Email Scraper platform could be a valuable tool for your clients' lead generation efforts.

Would you be interested in discussing potential collaboration?

Best regards,
{your_name}
Email Scraper Team'''
    }
}

# Email Validation Rules
EMAIL_VALIDATION = {
    'min_length': 5,
    'max_length': 254,
    'required_chars': ['@', '.'],
    'forbidden_chars': [' ', '<', '>', '"', "'"],
    'allowed_domains': [],  # Empty list means all domains allowed
    'blocked_domains': ['example.com', 'test.com', 'spam.com']
}

# Rate Limiting Rules
RATE_LIMITING = {
    'emails_per_minute': 10,
    'emails_per_hour': 100,
    'emails_per_day': 1000,
    'delay_between_emails': 1.0,  # seconds
    'delay_between_batches': 60.0,  # seconds
    'batch_size': 50
}

# Logging Configuration
EMAIL_LOGGING = {
    'log_success': True,
    'log_failures': True,
    'log_rates': True,
    'log_file': 'email_sender.log',
    'log_level': 'INFO'
}

def get_template(template_name: str) -> dict:
    """
    Get an email template by name
    
    Args:
        template_name: Name of the template
        
    Returns:
        dict: Template with subject and message
    """
    return EMAIL_TEMPLATES.get(template_name, EMAIL_TEMPLATES['welcome'])

def get_campaign_template(campaign_name: str) -> dict:
    """
    Get a campaign template by name
    
    Args:
        campaign_name: Name of the campaign
        
    Returns:
        dict: Campaign template
    """
    return CAMPAIGN_TEMPLATES.get(campaign_name, CAMPAIGN_TEMPLATES['business_development'])

def format_message(template: dict, **kwargs) -> dict:
    """
    Format a message template with provided variables
    
    Args:
        template: Template dictionary
        **kwargs: Variables to format in the message
        
    Returns:
        dict: Formatted template
    """
    formatted = template.copy()
    
    # Format subject
    if 'subject' in formatted:
        formatted['subject'] = formatted['subject'].format(**kwargs)
    
    # Format message
    if 'message' in formatted:
        formatted['message'] = formatted['message'].format(**kwargs)
    
    return formatted

# 📧 Email Sending Module

## Overview

This module adds **email sending capabilities** to your email scraper, allowing you to send emails to discovered addresses using the Mailgun API. Perfect for outreach campaigns, lead generation, and automated follow-ups!

## 🚀 Features

### **Core Email Sending**
- ✅ **Individual Emails**: Send single emails with custom content
- ✅ **Bulk Emails**: Send to multiple recipients with rate limiting
- ✅ **Campaign Emails**: Pre-built templates for different use cases
- ✅ **Rate Limiting**: Respectful delays to avoid spam filters

### **Professional Templates**
- 🏠 **Real Estate**: Agent outreach and partnership opportunities
- 💼 **Business Development**: Partnership and collaboration requests
- 📢 **Marketing**: Agency partnerships and service offerings
- 📧 **Custom Templates**: Easy to create and modify

### **Smart Features**
- 🔍 **Email Filtering**: Filter by domain or exclude specific domains
- 📊 **Detailed Logging**: Track success rates and failures
- 🛡️ **Error Handling**: Graceful handling of API failures
- ⚡ **Performance**: Efficient bulk sending with progress tracking

## 📦 Installation

### **1. Install Dependencies**
```bash
pip3 install requests
```

### **2. Set Up Mailgun**
1. **Create Mailgun Account**: [Sign up at Mailgun](https://www.mailgun.com/)
2. **Get API Key**: From your Mailgun dashboard
3. **Set Environment Variables**:
```bash
export MAILGUN_API_KEY='your_api_key_here'
export MAILGUN_DOMAIN='your_domain_here'
```

### **3. Test Connection**
```bash
python3 email_sender.py
```

## 🎯 Usage Examples

### **Basic Email Sending**
```python
from email_sender import EmailSender

# Initialize sender
sender = EmailSender()

# Send single email
success = sender.send_simple_message(
    to_email="recipient@example.com",
    to_name="John Doe",
    subject="Hello from Email Scraper",
    message="This is a test message!"
)
```

### **Bulk Email Sending**
```python
# Prepare email list
email_list = [
    {"email": "user1@example.com", "name": "User One"},
    {"email": "user2@example.com", "name": "User Two"},
    {"email": "user3@example.com", "name": "User Three"}
]

# Send bulk emails
results = sender.send_bulk_emails(
    email_list=email_list,
    subject="Welcome to Email Scraper",
    message="Thank you for using our service!",
    delay=2.0  # 2 second delay between emails
)
```

### **Campaign Emails**
```python
# Send campaign email
results = sender.send_campaign_email(
    campaign_name="business_development",
    email_list=email_list,
    subject="Partnership Opportunity",
    message="Let's discuss collaboration!",
    delay=3.0
)
```

## 🕷️ **Complete Workflow: Scrape + Send**

### **Step 1: Scrape Emails**
```bash
# Crawl website to discover emails
python3 es.py --crawl --max-pages 50 --max-depth 3 https://example.com
```

### **Step 2: Send Campaign**
```bash
# Send emails to discovered addresses
python3 scrape_and_send.py
```

## 📋 **Available Campaign Templates**

### **1. Real Estate Agent Outreach**
- **Purpose**: Connect with real estate professionals
- **Subject**: "Real Estate Marketing Partnership Opportunity"
- **Content**: Partnership discussion for lead generation

### **2. Business Development**
- **Purpose**: General business partnership outreach
- **Subject**: "Partnership Opportunity for Business Growth"
- **Content**: Collaboration and growth opportunities

### **3. Marketing Agency Partnership**
- **Purpose**: Connect with marketing agencies
- **Subject**: "Marketing Partnership Opportunity"
- **Content**: Service integration and client referrals

## ⚙️ **Configuration**

### **Environment Variables**
```bash
# Required
export MAILGUN_API_KEY='your_api_key_here'
export MAILGUN_DOMAIN='your_domain_here'

# Optional
export MAILGUN_FROM_NAME='Your Company Name'
export MAILGUN_REPLY_TO='reply@yourcompany.com'
```

### **Rate Limiting Settings**
```python
# In email_config.py
RATE_LIMITING = {
    'emails_per_minute': 10,
    'emails_per_hour': 100,
    'emails_per_day': 1000,
    'delay_between_emails': 1.0,  # seconds
    'delay_between_batches': 60.0,  # seconds
    'batch_size': 50
}
```

## 🔍 **Email Filtering**

### **Domain Filtering**
```python
# Only send to specific domains
filtered_emails = filter_emails(emails, domain_filter="gmail.com")
```

### **Exclusion Filtering**
```python
# Exclude specific domains
filtered_emails = filter_emails(emails, exclude_domains=["spam.com", "test.com"])
```

## 📊 **Monitoring and Logging**

### **Log Files**
- **`email_sender.log`**: Detailed email sending logs
- **`scraper.log`**: Email discovery and scraping logs

### **Success Tracking**
```python
# Check campaign results
print(f"Campaign Results:")
print(f"  Total: {results['total']}")
print(f"  Successful: {results['successful']}")
print(f"  Failed: {results['failed']}")
```

## 🚨 **Best Practices**

### **Rate Limiting**
- **Start Conservative**: Begin with 2-3 second delays
- **Respect Limits**: Don't exceed Mailgun's rate limits
- **Monitor Bounces**: Track delivery failures

### **Content Quality**
- **Personalize**: Use recipient names when possible
- **Clear Subject**: Avoid spam trigger words
- **Professional Tone**: Maintain business-appropriate language

### **Compliance**
- **CAN-SPAM**: Include unsubscribe options
- **GDPR**: Respect data protection regulations
- **Opt-out**: Honor unsubscribe requests

## 🔧 **Customization**

### **Adding New Templates**
```python
# In email_config.py
EMAIL_TEMPLATES['custom'] = {
    'subject': 'Custom Subject',
    'message': '''Hello {name},

Your custom message here.

Best regards,
{your_name}'''
}
```

### **Modifying Campaigns**
```python
# In email_config.py
CAMPAIGN_TEMPLATES['custom_campaign'] = {
    'name': 'Custom Campaign Name',
    'subject': 'Custom Campaign Subject',
    'message': 'Your custom campaign message...'
}
```

## 🚀 **Advanced Features**

### **A/B Testing**
```python
# Send different versions to test groups
version_a = format_message(template, your_name="David Mills")
version_b = format_message(template, your_name="Dave Mills")

# Send to different groups
sender.send_bulk_emails(group_a, **version_a)
sender.send_bulk_emails(group_b, **version_b)
```

### **Scheduled Sending**
```python
import schedule
import time

# Schedule campaign for specific time
schedule.every().day.at("09:00").do(send_campaign)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🔍 **Troubleshooting**

### **Common Issues**

#### **API Connection Failed**
- Check API key and domain
- Verify Mailgun account status
- Test with `sender.test_connection()`

#### **Emails Not Sending**
- Check rate limits
- Verify recipient email format
- Review Mailgun dashboard for errors

#### **High Bounce Rate**
- Clean email list
- Improve content quality
- Check sender reputation

### **Debug Commands**
```bash
# Test email sender
python3 email_sender.py

# Test with specific credentials
MAILGUN_API_KEY='your_key' MAILGUN_DOMAIN='your_domain' python3 email_sender.py

# Check logs
tail -f email_sender.log
```

## 📈 **Performance Metrics**

### **Expected Results**
- **Small Campaigns (10-50 emails)**: 90-95% success rate
- **Medium Campaigns (50-500 emails)**: 85-90% success rate
- **Large Campaigns (500+ emails)**: 80-85% success rate

### **Optimization Tips**
- **Batch Processing**: Send in smaller batches
- **Time Zones**: Send during recipient business hours
- **Content Testing**: A/B test subject lines and content

## 🔮 **Future Enhancements**

- **Email Analytics**: Open rates, click tracking
- **Template Builder**: Visual template editor
- **Automation Rules**: Trigger-based sending
- **Integration**: CRM and marketing tool connections
- **AI Content**: Smart content generation

---

**🎯 Your email scraper now has professional email sending capabilities!**

**Perfect for:**
- 🏠 Real estate lead generation
- 💼 Business development outreach
- 📢 Marketing campaigns
- 🔗 Partnership building
- 📧 Automated follow-ups

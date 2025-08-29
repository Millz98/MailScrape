#!/usr/bin/env python3
"""
Test email validation logic
"""

import re

def validate_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Test some common email formats
test_emails = [
    "test@example.com",
    "user.name@domain.co.uk",
    "user+tag@example.org",
    "user@subdomain.example.com",
    "invalid-email",
    "user@",
    "@domain.com",
    "user@domain",
    "user name@example.com",
    "user@domain..com"
]

print("🧪 Testing email validation:")
for email in test_emails:
    is_valid = validate_email(email)
    status = "✅" if is_valid else "❌"
    print(f"{status} {email}: {is_valid}")

# Test the regex pattern directly
print("\n🔍 Testing regex pattern:")
pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
test_text = "Contact us at info@sterlingplumbing.ca or sales@sterlingplumbing.ca for more information."
matches = re.findall(pattern, test_text)
print(f"Text: {test_text}")
print(f"Matches: {matches}")

# Test the broader pattern used in extraction
print("\n🔍 Testing broader extraction pattern:")
broad_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
broad_matches = re.findall(broad_pattern, test_text)
print(f"Broad pattern matches: {broad_matches}")

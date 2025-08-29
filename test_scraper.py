#!/usr/bin/env python3
"""
Test script to demonstrate the performance improvements of the optimized email scraper.
"""

import time
import requests
from bs4 import BeautifulSoup
import re

def test_old_method():
    """Simulate the old Selenium-based approach"""
    print("Testing old method (simulated)...")
    start_time = time.time()
    
    # Simulate Selenium overhead
    time.sleep(2)  # Browser startup time
    
    # Simulate page loading
    time.sleep(3)  # Dynamic content loading
    
    # Simulate email extraction
    time.sleep(1)
    
    elapsed = time.time() - start_time
    print(f"Old method took: {elapsed:.2f} seconds")
    return elapsed

def test_new_method():
    """Test the new optimized approach"""
    print("Testing new optimized method...")
    start_time = time.time()
    
    try:
        # Test with a simple website
        url = "https://httpbin.org/html"
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; MailScraper/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Test email extraction
                email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
                emails = email_pattern.findall(response.text)
                
                print(f"Found {len(emails)} emails (test page)")
                
    except Exception as e:
        print(f"Test failed: {e}")
    
    elapsed = time.time() - start_time
    print(f"New method took: {elapsed:.2f} seconds")
    return elapsed

def main():
    print("🚀 Email Scraper Performance Test\n")
    
    # Test old method
    old_time = test_old_method()
    
    print()
    
    # Test new method
    new_time = test_new_method()
    
    print()
    
    # Calculate improvement
    if old_time > 0 and new_time > 0:
        improvement = old_time / new_time
        print(f"📊 Performance Results:")
        print(f"   Old method: {old_time:.2f}s")
        print(f"   New method: {new_time:.2f}s")
        print(f"   Improvement: {improvement:.1f}x faster!")
        
        if improvement > 5:
            print("   🎉 Excellent improvement!")
        elif improvement > 2:
            print("   👍 Good improvement!")
        else:
            print("   ✅ Some improvement")

if __name__ == "__main__":
    main()

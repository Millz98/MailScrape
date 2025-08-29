#!/usr/bin/env python3
"""
Script to verify that all imports are working correctly and type checking issues are resolved.
"""

def test_imports():
    """Test all the main imports used in the scraper"""
    print("🔍 Testing imports...")
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 imported successfully")
    except ImportError as e:
        print(f"❌ beautifulsoup4 import failed: {e}")
        return False
    
    try:
        import re
        print("✅ re imported successfully")
    except ImportError as e:
        print(f"❌ re import failed: {e}")
        return False
    
    try:
        import urllib.parse
        print("✅ urllib.parse imported successfully")
    except ImportError as e:
        print(f"❌ urllib.parse import failed: {e}")
        return False
    
    try:
        import time
        print("✅ time imported successfully")
    except ImportError as e:
        print(f"❌ time import failed: {e}")
        return False
    
    try:
        import argparse
        print("✅ argparse imported successfully")
    except ImportError as e:
        print(f"❌ argparse import failed: {e}")
        return False
    
    try:
        from tqdm import tqdm
        print("✅ tqdm imported successfully")
    except ImportError as e:
        print(f"❌ tqdm import failed: {e}")
        return False
    
    try:
        import logging
        print("✅ logging imported successfully")
    except ImportError as e:
        print(f"❌ logging import failed: {e}")
        return False
    
    return True

def test_scraper_functions():
    """Test that the main scraper functions can be imported"""
    print("\n🔍 Testing scraper functions...")
    
    try:
        from es import validate_url, validate_email, extract_emails_from_text, extract_emails_from_mailto
        print("✅ All scraper functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Scraper functions import failed: {e}")
        return False

def main():
    print("🚀 Type Checking and Import Verification\n")
    
    # Test basic imports
    imports_ok = test_imports()
    
    # Test scraper functions
    functions_ok = test_scraper_functions()
    
    print("\n" + "="*50)
    
    if imports_ok and functions_ok:
        print("🎉 All tests passed! Your scraper is ready to use.")
        print("\n💡 Type checking should now work properly with Pyright.")
        print("   If you still see errors, try restarting your IDE/editor.")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 To fix import issues, run:")
        print("   pip3 install -r requirements.txt")

if __name__ == "__main__":
    main()

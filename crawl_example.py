#!/usr/bin/env python3
"""
Example script demonstrating the website crawling capabilities of the email scraper.
This shows different crawling scenarios and best practices.
"""

import subprocess
import sys
import time

def run_crawler_command(command, description):
    """Run a crawler command and display results"""
    print(f"\n{'='*60}")
    print(f"🕷️  {description}")
    print(f"{'='*60}")
    print(f"Command: {command}")
    print(f"Starting at: {time.strftime('%H:%M:%S')}")
    
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Crawling completed successfully!")
            print("\n📊 Output:")
            print(result.stdout)
        else:
            print("❌ Crawling failed!")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Crawling timed out after 5 minutes")
    except Exception as e:
        print(f"❌ Error running command: {e}")

def main():
    print("🕷️  Website Crawling Examples")
    print("This script demonstrates different crawling scenarios")
    print("Make sure you have the required dependencies installed!")
    
    # Example 1: Basic website crawling
    print("\n📚 Example 1: Basic Website Crawling")
    print("Crawls a simple website with default settings")
    
    command1 = "python3 es.py --crawl --max-pages 10 --max-depth 2 --delay 1.0 https://httpbin.org/html"
    run_crawler_command(command1, "Basic Website Crawling")
    
    # Example 2: Aggressive crawling (be respectful!)
    print("\n📚 Example 2: Aggressive Crawling (Respectful)")
    print("Crawls more pages with faster rate - use responsibly!")
    
    command2 = "python3 es.py --crawl --max-pages 20 --max-depth 3 --delay 0.5 https://httpbin.org/html"
    run_crawler_command(command2, "Aggressive Crawling")
    
    # Example 3: Deep crawling
    print("\n📚 Example 3: Deep Crawling")
    print("Crawls deeper into the website structure")
    
    command3 = "python3 es.py --crawl --max-pages 30 --max-depth 4 --delay 1.5 https://httpbin.org/html"
    run_crawler_command(command3, "Deep Crawling")
    
    print(f"\n{'='*60}")
    print("🎉 All examples completed!")
    print("💡 Check emails.txt for discovered email addresses")
    print("📝 Check scraper.log for detailed crawling information")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()

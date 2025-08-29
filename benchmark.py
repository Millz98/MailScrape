#!/usr/bin/env python3
"""
Benchmark script to demonstrate the performance improvements of the optimized email scraper.
"""

import time
import statistics
from es import scrape_website, validate_url

def benchmark_scraper(url, iterations=3):
    """Benchmark the scraper performance on a given URL"""
    print(f"🔍 Benchmarking scraper on: {url}")
    print(f"   Running {iterations} iterations...")
    
    times = []
    emails_found = []
    
    for i in range(iterations):
        print(f"   Iteration {i+1}/{iterations}...", end=" ")
        
        # Reset unique emails for each iteration
        unique_emails = set()
        
        start_time = time.time()
        try:
            scrape_website(url, unique_emails)
            elapsed = time.time() - start_time
            times.append(elapsed)
            emails_found.append(len(unique_emails))
            print(f"✅ {elapsed:.2f}s ({len(unique_emails)} emails)")
        except Exception as e:
            print(f"❌ Failed: {e}")
            times.append(float('inf'))
            emails_found.append(0)
    
    # Calculate statistics
    valid_times = [t for t in times if t != float('inf')]
    if valid_times:
        avg_time = statistics.mean(valid_times)
        min_time = min(valid_times)
        max_time = max(valid_times)
        
        print(f"\n📊 Results for {url}:")
        print(f"   Average time: {avg_time:.2f}s")
        print(f"   Best time: {min_time:.2f}s")
        print(f"   Worst time: {max_time:.2f}s")
        print(f"   Total emails found: {sum(emails_found)}")
        
        return avg_time, sum(emails_found)
    else:
        print(f"\n❌ All iterations failed for {url}")
        return float('inf'), 0

def main():
    print("🚀 Email Scraper Performance Benchmark\n")
    
    # Test URLs (using safe, public websites)
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
        "https://httpbin.org/headers"
    ]
    
    results = []
    
    for url in test_urls:
        if validate_url(url):
            print(f"\n{'='*60}")
            avg_time, total_emails = benchmark_scraper(url, iterations=2)
            results.append((url, avg_time, total_emails))
        else:
            print(f"\n❌ Invalid URL: {url}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📈 BENCHMARK SUMMARY")
    print(f"{'='*60}")
    
    successful_results = [r for r in results if r[1] != float('inf')]
    
    if successful_results:
        avg_times = [r[1] for r in successful_results]
        total_emails = sum(r[2] for r in successful_results)
        
        print(f"✅ Successful scrapes: {len(successful_results)}/{len(test_urls)}")
        print(f"📊 Average scrape time: {statistics.mean(avg_times):.2f}s")
        print(f"🎯 Total emails found: {total_emails}")
        print(f"⚡ Performance rating: ", end="")
        
        avg_time = statistics.mean(avg_times)
        if avg_time < 1.0:
            print("🚀 Excellent (< 1s)")
        elif avg_time < 3.0:
            print("👍 Good (1-3s)")
        elif avg_time < 5.0:
            print("✅ Acceptable (3-5s)")
        else:
            print("🐌 Slow (> 5s)")
    else:
        print("❌ No successful scrapes")
    
    print(f"\n💡 Tips for better performance:")
    print(f"   • Use --delay 2.0 for respectful scraping")
    print(f"   • Check your internet connection")
    print(f"   • Some websites may block automated requests")
    print(f"   • Consider using a VPN if needed")

if __name__ == "__main__":
    main()

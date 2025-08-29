"""
Configuration file for the optimized email scraper.
Advanced users can modify these settings for custom behavior.
"""

# Scraping Configuration
SCRAPING_CONFIG = {
    'max_concurrent_requests': 5,  # Maximum concurrent requests (for future async implementation)
    'request_delay': 1.0,          # Delay between requests in seconds
    'timeout': 30,                 # Request timeout in seconds
    'max_retries': 3,              # Maximum retry attempts for failed requests
    'follow_redirects': True,      # Whether to follow HTTP redirects
    'verify_ssl': True,            # Whether to verify SSL certificates
}

# HTTP Headers Configuration
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; MailScraper/1.0; +https://github.com/your-repo)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Email Extraction Configuration
EMAIL_EXTRACTION_CONFIG = {
    'extract_from_text': True,     # Extract emails from text content
    'extract_from_mailto': True,   # Extract emails from mailto links
    'extract_from_data_attrs': True,  # Extract emails from data attributes
    'extract_from_meta': True,     # Extract emails from meta tags
    'case_sensitive': False,       # Whether email matching is case sensitive
    'validate_emails': True,       # Whether to validate email format
}

# Regex Patterns (pre-compiled for efficiency)
EMAIL_PATTERNS = {
    'basic': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'mailto': r'mailto:([^?&\s]+)',
    'data_email': r'data-email=["\']([^"\']+)["\']',
    'meta_email': r'<meta[^>]*content=["\']([^"\']*@[^"\']*\.[^"\']*)["\'][^>]*>',
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'scraper.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,
}

# Rate Limiting Configuration
RATE_LIMITING_CONFIG = {
    'enabled': True,
    'requests_per_minute': 10,     # Max requests per minute per domain
    'requests_per_hour': 100,      # Max requests per hour per domain
    'backoff_factor': 2,           # Exponential backoff factor
}

# Output Configuration
OUTPUT_CONFIG = {
    'emails_file': 'emails.txt',
    'log_file': 'scraper.log',
    'cache_dir': '.cache',
    'cache_expiry_hours': 24,      # Cache expiry time in hours
    'save_format': 'txt',          # Output format (txt, csv, json)
    'include_timestamp': True,     # Whether to include timestamps in output
}

# Advanced Features Configuration
ADVANCED_CONFIG = {
    'enable_caching': True,        # Enable content caching
    'enable_proxy_rotation': False,  # Enable proxy rotation (future feature)
    'enable_async_processing': False,  # Enable async processing (future feature)
    'enable_machine_learning': False,  # Enable ML-based email detection (future feature)
    'enable_robots_txt_check': True,   # Check robots.txt before scraping
    'enable_sitemap_processing': False,  # Process sitemaps for URLs (future feature)
}

# Performance Tuning
PERFORMANCE_CONFIG = {
    'chunk_size': 1024,            # Chunk size for file operations
    'max_memory_usage': 100 * 1024 * 1024,  # Max memory usage (100MB)
    'cleanup_interval': 3600,      # Cleanup interval in seconds
    'enable_compression': True,    # Enable gzip compression for requests
}

# Debug Configuration
DEBUG_CONFIG = {
    'verbose_logging': False,      # Enable verbose logging
    'save_raw_html': False,       # Save raw HTML for debugging
    'print_emails_found': True,   # Print found emails to console
    'show_progress_bar': True,    # Show progress bar during scraping
}

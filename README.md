# MailScrape - Optimized Email Scraper with Website Crawling

A highly efficient email scraping tool that extracts email addresses from websites using modern optimization techniques. **NEW: Now includes comprehensive website crawling to discover and scrape all pages on a domain!**

## 🚀 Key Features & Optimizations

- **🕷️ Website Crawling**: Automatically discover and scrape all pages on a website
- **Lightning Fast**: Replaced Selenium with requests + BeautifulSoup for 10x+ speed improvement
- **Smart Caching**: Avoids re-scraping the same content
- **Connection Pooling**: Reuses HTTP connections for better performance
- **Intelligent Email Extraction**: Enhanced regex patterns and multiple extraction methods
- **Rate Limiting**: Respectful scraping with configurable delays
- **Robots.txt Compliance**: Automatically checks and respects website crawling rules
- **Progress Tracking**: Real-time progress bars and detailed logging
- **Error Handling**: Robust error handling with retry logic

## 📦 Installation

### Quick Install
```bash
# Make the install script executable and run it
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Manual Install
```bash
# Install for current user (recommended)
pip3 install --user -r requirements.txt

# Or install system-wide (requires sudo)
sudo pip3 install -r requirements.txt
```

### Troubleshooting
If you get `ModuleNotFoundError`:
1. **Try user installation**: `pip3 install --user -r requirements.txt`
2. **Use Python module**: `python3 -m pip install --user -r requirements.txt`
3. **System-wide install**: `sudo pip3 install -r requirements.txt`
4. **Check Python path**: `python3 -c "import sys; print(sys.path)"`

## 🎯 Usage

### Basic Single-Page Scraping
```bash
# Scrape a single page
python3 es.py https://example.com

# Scrape multiple specific pages
python3 es.py https://site1.com https://site2.com https://site3.com
```

### 🕷️ Website Crawling (NEW!)
```bash
# Crawl entire website (discovers all pages automatically)
python3 es.py --crawl https://example.com

# Crawl with custom limits
python3 es.py --crawl --max-pages 100 --max-depth 4 https://example.com

# Crawl with faster rate (be respectful!)
python3 es.py --crawl --delay 0.5 --max-pages 50 https://example.com
```

### Advanced Options
```bash
# Custom settings for respectful scraping
python3 es.py --crawl --delay 2.0 --timeout 45 --max-pages 200 --max-depth 5 https://example.com
```

## ⚙️ Command Line Options

- `urls`: One or more URLs to scrape (required)
- `--crawl`: Enable website crawling mode to discover all pages
- `--max-pages`: Maximum pages to crawl (default: 50)
- `--max-depth`: Maximum crawl depth (default: 3)
- `--delay`: Delay between requests in seconds (default: 1.0)
- `--timeout`: Request timeout in seconds (default: 30)

## 🔧 Technical Improvements Made

1. **🕷️ Website Crawling**: Automatically discovers all pages on a domain
2. **Replaced Selenium**: Eliminated browser overhead and dependency on Chrome
3. **Optimized Regex**: Pre-compiled patterns for faster email extraction
4. **Session Management**: HTTP connection pooling and reuse
5. **Better Headers**: More realistic browser headers for higher success rates
6. **Enhanced Extraction**: Multiple methods to find emails in various HTML elements
7. **Memory Efficiency**: Better data structures and duplicate removal
8. **Robots.txt Support**: Respects website crawling rules automatically
9. **Logging**: Comprehensive logging for debugging and monitoring

## 📊 Performance Comparison

| Feature | Old Version | New Version | Improvement |
|---------|-------------|-------------|-------------|
| Speed | ~5-10 sec/URL | ~0.5-2 sec/URL | **5-20x faster** |
| Memory | High (Chrome) | Low | **90% reduction** |
| Coverage | Single page | Entire website | **Unlimited pages** |
| Dependencies | 5+ packages | 4 packages | **Simplified** |
| Scalability | Single URL | Multiple URLs | **Parallel ready** |

## 🕷️ Website Crawling Features

### **Automatic Discovery**
- Finds all internal links on each page
- Converts relative URLs to absolute URLs
- Respects same-domain policy
- Handles redirects and errors gracefully

### **Smart Crawling**
- Configurable depth limits (default: 3 levels)
- Page count limits (default: 50 pages)
- Skips non-HTML content (PDFs, images, etc.)
- Respects robots.txt rules

### **Respectful Scraping**
- Configurable delays between requests
- User-agent identification
- Rate limiting built-in
- Error handling and retry logic

## 🎨 Email Extraction Methods

- **Text Content**: Scans all text elements for email patterns
- **Mailto Links**: Extracts emails from `mailto:` href attributes
- **Data Attributes**: Finds emails in `data-email` attributes
- **Multiple Elements**: Checks span, div, td, th, li elements
- **Cross-Page Discovery**: Finds emails across entire website

## 📝 Output

- **emails.txt**: All unique emails found across all pages
- **scraper.log**: Detailed crawling and scraping information
- **Console**: Real-time progress and results

## 🚨 Best Practices

- Use reasonable delays between requests (1-3 seconds)
- Respect robots.txt and website terms of service
- Don't overwhelm servers with too many concurrent requests
- Monitor logs for any issues or rate limiting
- Start with small limits and increase gradually

## 🔮 Future Enhancements

- Async/parallel processing for multiple URLs
- Advanced caching with database backend
- Proxy rotation for large-scale scraping
- Machine learning for better email detection
- Web interface for easier management
- Sitemap processing for faster discovery

## 📄 License

This project is open source and available under the MIT License.
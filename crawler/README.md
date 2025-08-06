# Web Crawler Module

## Overview
Single-threaded web crawler that extracts content from websites using a breadth-first search approach with configurable rate limiting.

## Architecture

### Core Components
- **URL Queue**: `deque` for efficient FIFO operations per domain
- **Visited Set**: `set` for O(1) duplicate detection per domain
- **Rate Limiting**: Configurable delays between requests (default: 0.005s)
- **Error Handling**: Robust exception handling for network failures

### Key Data Structures

#### URL Queue (`deque`)
```python
from collections import deque
self.queue = deque(seed_urls)
```
- **Why deque**: O(1) append/pop operations vs O(n) for list
- **FIFO behavior**: Ensures breadth-first crawling
- **Per-domain isolation**: Each seed URL gets its own queue

#### Visited Set (`set`)
```python
self.visited = set()  # Reset for each domain
```
- **Why set**: O(1) lookup for duplicate detection
- **Domain isolation**: Reset for each seed URL to allow cross-domain crawling
- **Hash-based**: Fast membership testing

## Detailed Method Analysis

### `fetch_html(url)`
```python
def fetch_html(self, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
```

**Unusual Concepts:**
- **User-Agent Spoofing**: Mimics real browser to avoid blocking
- **Timeout Handling**: 10-second timeout prevents hanging on slow servers
- **Status Code Validation**: `raise_for_status()` for HTTP errors
- **Exception Handling**: Returns `(None, None)` on failure

### `extract_links(html, base_url)`
```python
soup = BeautifulSoup(html, 'lxml')
links = soup.find_all('a', href=True)
```

**Unusual Concepts:**
- **BeautifulSoup Parser**: HTML parsing with error tolerance
- **lxml Backend**: Fast C-based parser vs pure Python
- **Relative URL Resolution**: `urljoin()` for proper URL construction
- **Link Filtering**: Only processes `<a>` tags with `href` attributes

### `normalize_url(url)`
```python
def normalize_url(self, url):
    parsed = urlparse(url)
    normalized = parsed._replace(fragment='', query='')
    # Handle trailing slash normalization
```

**Unusual Concepts:**
- **URL Parsing**: Breaks URL into components (scheme, netloc, path)
- **Fragment Removal**: Removes `#fragment` parts
- **Query Removal**: Removes `?query=params` parts
- **Trailing Slash Handling**: Consistent slash normalization
- **Canonicalization**: Ensures consistent URL representation

### `is_valid_link(url)`
```python
def is_valid_link(self, url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ['http', 'https']
```

**Unusual Concepts:**
- **Scheme Validation**: Only HTTP/HTTPS protocols
- **Malformed URL Detection**: Catches invalid URL structures
- **Security Filtering**: Prevents malicious URL schemes

## Advanced Features

### Rate Limiting
```python
time.sleep(self.crawl_delay)  # 0.005 seconds
```
- **Respectful Crawling**: Prevents server overload
- **Configurable Delay**: Adjustable per crawler instance
- **Per-request delay**: Applied after each page crawl

### Content Storage
```python
url_hash = hashlib.md5(url.encode()).hexdigest()
html_filename = f"{self.data_dir}/{url_hash}.html"
```

**Unusual Concepts:**
- **MD5 Hashing**: Creates unique filenames from URLs
- **Collision Avoidance**: Hash-based naming prevents conflicts
- **Metadata Storage**: Separate JSON files for crawl info
- **Progress Reporting**: Only prints every 10th page to reduce spam

### Error Resilience
```python
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    print(f'Error fetching {url}: {e}')
    return None, None
```

**Unusual Concepts:**
- **Exception Hierarchy**: `RequestException` catches all HTTP errors
- **Graceful Degradation**: Continues crawling despite failures
- **Timeout Protection**: Prevents infinite waits
- **Visited Marking**: Marks failed URLs as visited to avoid retries

## Domain Isolation Strategy

### Per-Domain Processing
```python
for seed_url in self.seed_urls:
    self.queue = deque([seed_url])
    self.visited = set()  # Reset for each domain
```

**Unusual Concepts:**
- **Queue Reset**: Fresh queue for each seed URL
- **Visited Reset**: Allows cross-domain link discovery
- **Domain Independence**: Each domain processed separately
- **Page Limit**: `max_pages` limit per domain

## Performance Optimizations

### Memory Management
- **Streaming**: Processes one page at a time
- **Queue Size**: Limits memory usage with max_pages per domain
- **Garbage Collection**: Automatic cleanup of processed URLs

### Network Efficiency
- **Connection Reuse**: Requests library handles pooling
- **Compression**: Automatic gzip/deflate handling
- **Redirect Following**: Automatic HTTP redirect handling

## Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `crawl_delay` | 0.005s | Delay between requests |
| `max_pages` | 20 | Pages per domain limit |
| `timeout` | 10s | Request timeout |
| `user_agent` | Mozilla/5.0 | Browser identification |

## Output Format

### HTML Files
- **Location**: `data/pages/{url_hash}.html`
- **Encoding**: UTF-8
- **Content**: Raw HTML from crawled pages

### Metadata Files
```json
{
  "original_url": "https://example.com",
  "content_length": 15420,
  "filename": "data/pages/abc123.html",
  "status_code": 200,
  "crawl_timestamp": 1640995200.0
}
```

## Crawling Strategy

### Breadth-First Search
- **FIFO Queue**: Processes URLs in order discovered
- **Link Discovery**: Extracts all links from each page
- **Queue Management**: Adds new links to queue
- **Duplicate Prevention**: Checks visited set before processing

### Progress Tracking
```python
if domain_pages % 20 == 0:
    print(f"   📊 Progress: {domain_pages}/{self.max_pages} pages")
```
- **Progress Reporting**: Shows progress every 20 pages
- **Domain Summary**: Reports pages crawled per domain
- **Total Summary**: Reports total pages across all domains

## Limitations & Future Enhancements

### Current Limitations
- **Single-threaded**: No parallel processing
- **No robots.txt**: Doesn't respect robots.txt
- **Basic Filtering**: Limited content type filtering
- **No depth control**: Crawls all discovered links

### Future Enhancements
- **Multi-threading**: Parallel crawling
- **Robots.txt**: Respect crawling rules
- **Content Types**: Filter by MIME type
- **Depth Control**: Limit crawl depth
- **Domain Isolation**: Separate queues per domain

## Testing Strategy
- **Unit Tests**: Individual method testing
- **Integration Tests**: End-to-end crawling
- **Performance Tests**: Speed and memory usage
- **Edge Cases**: Malformed URLs, network errors 
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from typing import List
import os
import hashlib
import json
import time


class Crawler:
    def __init__(self, seed_urls: List[str], max_pages: int, data_dir='data/pages', crawl_delay=0.005):
        self.seed_urls = seed_urls
        self.visited = set()
        self.max_pages = max_pages
        self.data_dir = data_dir
        self.crawl_delay = crawl_delay
        self.queue = deque(seed_urls)
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    

    def fetch_html(self, url):
        """Fetch HTML content from URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text, response.status_code
        except requests.RequestException as e:
            print(f'Error fetching {url}: {e}')
            return None, None
    

    def save_page(self, url, html, status_code):
        """Save HTML page to file"""
        try:
            # Create filename from URL hash
            url_hash = hashlib.md5(url.encode()).hexdigest()
            html_filename = f"{self.data_dir}/{url_hash}.html"
            meta_filename = f"{self.data_dir}/{url_hash}.meta"

            metadata = {
                'original_url': url,
                'content_length': len(html),
                'filename': html_filename,
                'status_code': status_code,
                'crawl_timestamp': time.time()
            }

            # Save HTML content
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html)
            
            # Save metadata
            with open(meta_filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            
            # Only print every 10th page to reduce console spam
            if len(self.visited) % 10 == 0:
                print(f'📄 Saved: {url} -> {html_filename}')
            return True

        except IOError as e:
            
            print(f'Error saving {url}: {e}')
            return False

    def is_valid_link(self, url):
        """Filter out invalid links"""
        try:
            parsed_url = urlparse(url)

            if not parsed_url.scheme:
                return False
            
            if parsed_url.scheme not in ['http', 'https']:
                return False
            
            if parsed_url.scheme and not parsed_url.netloc:
                return False

            return True
        except:
            return False
    


    def extract_links(self, html, base_url):
        """Extract all links from HTML"""
        if not html:
            return []
            
        try:
            soup = BeautifulSoup(html, 'lxml')
            links = []

            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                
                if full_url and self.is_valid_link(full_url):
                    links.append(full_url)

            return links
        except Exception as e:
            print(f"Error extracting links from {base_url}: {e}")
            return []

    def crawl_page(self, url):
        try:
            html, status_code = self.fetch_html(url)
            
            if not html:
                print(f"⚠️  Skipping {url} - no content")
                self.visited.add(self.normalize_url(url))
                return

            self.save_page(url, html, status_code)
            links = self.extract_links(html, url)

            for link in links:
                if link not in self.visited and link not in self.queue:
                    self.queue.append(self.normalize_url(link))
            
            self.visited.add(self.normalize_url(url))
            
            # Delay to prevent overwhelming servers
            time.sleep(self.crawl_delay)
            
        except Exception as e:
            print(f"⚠️  Error crawling {url}: {e}")
            # Mark as visited to avoid infinite retries
            self.visited.add(self.normalize_url(url))
            return
    
    def start_crawling(self):
        print(f"Starting crawler with {len(self.seed_urls)} seed URLs")
        print(f"Max pages per URL: {self.max_pages}")

        total_pages = 0
        
        for i, seed_url in enumerate(self.seed_urls, 1):
            print(f"\n🕷️  Crawling {i}/{len(self.seed_urls)}: {seed_url}...")
            domain_pages = 0
            self.queue = deque([seed_url])
            self.visited = set()  # Reset visited for each domain
            
            while self.queue and domain_pages < self.max_pages:
                url = self.queue.popleft()
                if self.normalize_url(url) not in self.visited:
                    self.crawl_page(url)
                    domain_pages += 1
                    total_pages += 1
                    
                    # Show progress every 20 pages
                    if domain_pages % 20 == 0:
                        print(f"   📊 Progress: {domain_pages}/{self.max_pages} pages")
            
            print(f"✅ Crawled {domain_pages} pages from {seed_url}")

        print(f"\n🎉 Crawling complete! Visited {total_pages} pages total across all domains")
    
    def normalize_url(self, url):
        """Normalize URL to avoid duplicates like example.com/ and example.com"""
        parsed = urlparse(url)
        
        # Remove fragment and query
        normalized = parsed._replace(fragment='', query='')
        
        # Handle trailing slash - always remove it for consistency
        path = normalized.path
        if path.endswith('/') and len(path) > 1:
            # Remove trailing slash for non-root paths
            path = path.rstrip('/')
            normalized = normalized._replace(path=path)
        elif path == '/':
            # For root path, remove the slash to normalize
            normalized = normalized._replace(path='')
        
        return normalized.geturl()


        


    
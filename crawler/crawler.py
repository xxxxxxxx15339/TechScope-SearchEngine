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
    def __init__(self, seed_urls: List[str], max_pages: int, data_dir='data/pages'):
        self.seed_urls = seed_urls
        self.visited = set()
        self.max_pages = max_pages
        self.data_dir = data_dir
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
            
            print(f'Saved: {url} -> {html_filename}')
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
        soup = BeautifulSoup(html, 'lxml')
        links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if full_url and self.is_valid_link(full_url):
                links.append(full_url)

        return links

    def crawl_page(self, url):
        html, status_code = self.fetch_html(url)
        links = self.extract_links(html, url)

        if not html:
            return

        self.save_page(url, html, status_code)

        for link in links:
            if link not in self.visited and link not in self.queue:
                self.queue.append(self.normalize_url(link))
        
        self.visited.add(self.normalize_url(url))
    
    def start_crawling(self):
        print(f"Starting crawler with {len(self.seed_urls)} seed URLs")
        print(f"Max pages: {self.max_pages}")

        self.queue = deque(self.seed_urls)

        while self.queue and len(self.visited) < self.max_pages:
            url = self.queue.popleft()
            self.crawl_page(url)

        print(f"Crawling complete! Visited {len(self.visited)} pages total")
    
    def normalize_url(self, url):
        parsed = urlparse(url)
        return parsed._replace(fragment='', query='').geturl()


        


    
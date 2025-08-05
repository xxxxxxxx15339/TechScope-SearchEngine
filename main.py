#!/usr/bin/env python3
"""
TechScope Search Engine - Main Application
Provides a complete workflow for crawling, indexing, and searching web content.
"""

import argparse
import sys
import os
from typing import List, Dict

# Import our modules
from crawler.crawler import Crawler
from index.indexer import Indexer
from query.query import Query


class TechScopeSearchEngine:
    """Main application class that orchestrates the entire search engine workflow."""
    
    def __init__(self):
        self.crawler = None
        self.indexer = None
        self.query_engine = None
        
    def setup_crawler(self, urls: List[str], max_pages: int = 20, crawl_delay: float = 0.005):
        """Initialize the web crawler."""
        print("🕷️  Setting up web crawler...")
        self.crawler = Crawler(seed_urls=urls, max_pages=max_pages, crawl_delay=crawl_delay)
        print(f"✅ Crawler ready for {len(urls)} URLs, max {max_pages} pages each, delay: {crawl_delay}s")
        
    def auto_setup(self, crawl_delay=None):
        """Automatically setup crawler, indexer, and query engine with default seed URLs."""
        import json
        
        # Load seed URLs from config
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
            seed_urls = config['seed_urls']
            if crawl_delay is None:
                crawl_delay = config.get('crawl_delay', 0.005)
        except:
            # Fallback seed URLs if config.json not found
            seed_urls = [
                "https://stackoverflow.com",
                "https://developer.mozilla.org", 
                "https://docs.python.org",
                "https://w3schools.com"
            ]
            if crawl_delay is None:
                crawl_delay = 0.005
        
        # Always use 20 pages per URL
        max_pages = 20
        
        print(f"🚀 Auto-setup: Loading seed URLs and crawling...")
        
        # Setup and run crawler
        self.setup_crawler(seed_urls, max_pages=max_pages, crawl_delay=crawl_delay)
        self.crawl_websites()
        
        # Setup and run indexer
        self.setup_indexer()
        self.build_index()
        
        # Setup query engine
        self.setup_query_engine()
        
        print("✅ Auto-setup completed! Ready for queries.")
        
    def setup_indexer(self, data_dir: str = 'data/pages', index_dir: str = 'index/data'):
        """Initialize the indexer."""
        print("📚 Setting up indexer...")
        self.indexer = Indexer(data_dir=data_dir, index_dir=index_dir)
        print(f"✅ Indexer ready (data: {data_dir}, index: {index_dir})")
        
    def setup_query_engine(self, index_dir: str = 'index/data'):
        """Initialize the query engine."""
        print("🔍 Setting up query engine...")
        self.query_engine = Query(index_dir=index_dir)
        print("✅ Query engine ready")
        
    def crawl_websites(self):
        """Crawl the specified websites."""
        if not self.crawler:
            print("❌ Crawler not initialized!")
            return False
            
        print("\n🕷️  Starting web crawling...")
        try:
            self.crawler.start_crawling()
            print("✅ Crawling completed successfully!")
            return True
        except Exception as e:
            print(f"❌ Crawling failed: {e}")
            return False
            
    def build_index(self):
        """Build the search index from crawled data."""
        if not self.indexer:
            print("❌ Indexer not initialized!")
            return False
            
        print("\n📚 Building search index...")
        try:
            self.indexer.build_index()
            print("✅ Index built successfully!")
            return True
        except Exception as e:
            print(f"❌ Index building failed: {e}")
            return False
            
    def search(self, query: str, max_results: int = 10):
        """Search for a query and return results."""
        if not self.query_engine:
            print("❌ Query engine not initialized!")
            return []
            
        print(f"\n🔍 Searching for: '{query}'")
        try:
            results = self.query_engine.search(query, max_results)
            return results
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
            
    def get_stats(self):
        """Get search engine statistics."""
        if not self.query_engine:
            return {"status": "Query engine not initialized"}
            
        try:
            return self.query_engine.get_search_stats()
        except Exception as e:
            return {"status": f"Error getting stats: {e}"}
    
    def save_search_results(self, query: str, results: List[Dict], max_results: int):
        """Save search results to JSON file in root directory."""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_query = query.replace(' ', '_').replace('/', '_').replace('\\', '_')[:30]
        filename = f"search_results_{timestamp}_{safe_query}.json"
        
        search_data = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "max_results": max_results,
            "total_results": len(results),
            "results": results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(search_data, f, indent=2, ensure_ascii=False)
            print(f"📝 Search results saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error saving search results: {e}")
            return None


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="TechScope Search Engine - Complete web search solution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Crawl websites and build index
  python main.py --crawl https://example.com https://python.org --max-pages 5
  
  # Search for content
  python main.py --search "python programming"
  
  # Get statistics
  python main.py --stats
  
  # Complete workflow
  python main.py --crawl https://example.com --build-index --search "python"
        """
    )
    
    # Action arguments
    parser.add_argument('--crawl', nargs='+', metavar='URL', 
                       help='URLs to crawl')
    parser.add_argument('--max-pages', type=int, default=20,
                       help='Maximum pages to crawl per URL (default: 20, used only with --crawl)')
    parser.add_argument('--crawl-delay', type=float, default=None,
                       help='Delay between requests in seconds (default: from config.json)')
    parser.add_argument('--build-index', action='store_true',
                       help='Build search index from crawled data')
    parser.add_argument('--search', type=str, metavar='QUERY',
                       help='Search for a query')
    parser.add_argument('--max-results', type=int, default=10,
                       help='Maximum results to return (default: 10)')
    parser.add_argument('--stats', action='store_true',
                       help='Show search engine statistics')
    
    # Configuration arguments
    parser.add_argument('--data-dir', default='data/pages',
                       help='Directory for crawled data (default: data/pages)')
    parser.add_argument('--index-dir', default='index/data',
                       help='Directory for index files (default: index/data)')
    
    args = parser.parse_args()
    
    # Initialize the search engine
    engine = TechScopeSearchEngine()
    
    # Handle different actions
    if args.crawl:
        print("🚀 TechScope Search Engine - Manual Crawling Mode")
        print("=" * 50)
        
        # Load crawl_delay from config or use command line argument
        if args.crawl_delay is not None:
            crawl_delay = args.crawl_delay
        else:
            try:
                with open('config.json', 'r') as f:
                    config = json.load(f)
                crawl_delay = config.get('crawl_delay', 0.005)
            except:
                crawl_delay = 0.005
        
        engine.setup_crawler(args.crawl, args.max_pages, crawl_delay)
        if engine.crawl_websites():
            print("\n✅ Crawling completed successfully!")
        else:
            print("\n❌ Crawling failed!")
            sys.exit(1)
    
    if args.build_index:
        print("\n📚 Building search index...")
        engine.setup_indexer(args.data_dir, args.index_dir)
        if engine.build_index():
            print("✅ Index built successfully!")
        else:
            print("❌ Index building failed!")
            sys.exit(1)
    
    if args.search:
        print("\n🔍 Search Mode")
        print("=" * 30)
        
        # Auto-setup if not already done
        if not engine.query_engine:
            print("🔄 Auto-setup: Initializing crawler, indexer, and query engine...")
            crawl_delay = args.crawl_delay if args.crawl_delay is not None else None
            engine.auto_setup(crawl_delay=crawl_delay)
        
        results = engine.search(args.search, args.max_results)
        
        if results:
            print(f"\n📊 Found {len(results)} results:")
            print("-" * 50)
            for i, result in enumerate(results, 1):
                print(f"{i}. Score: {result.get('score', 0):.3f}")
                print(f"   Title: {result.get('title', 'No title')}")
                print(f"   URL: {result.get('url', 'No URL')}")
                print(f"   Doc ID: {result.get('doc_id', 'Unknown')}")
                print()
            
            # Save search results to JSON file
            engine.save_search_results(args.search, results, args.max_results)
        else:
            print("❌ No results found.")
    
    if args.stats:
        print("\n📊 Search Engine Statistics")
        print("=" * 35)
        
        engine.setup_query_engine(args.index_dir)
        stats = engine.get_stats()
        
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    # If no specific action, show help
    if not any([args.crawl, args.build_index, args.search, args.stats]):
        print("🚀 TechScope Search Engine - Auto Mode")
        print("=" * 50)
        print("💡 Usage: python main.py --search 'your query here'")
        print("💡 The system will automatically:")
        print("   1. Crawl 20 pages from all seed URLs")
        print("   2. Build the search index")
        print("   3. Search for your query")
        print("   4. Save results to JSON file")
        print("\n📋 Example: python main.py --search 'python tutorial'")
        print("📋 Manual mode: python main.py --crawl URL --build-index --search 'query'")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Test script for TechScope Search Engine Main Application
Demonstrates the complete workflow: crawl → index → search
"""

import os
import sys
from main import TechScopeSearchEngine

def test_complete_workflow():
    """Test the complete search engine workflow."""
    print("🧪 Testing TechScope Search Engine Complete Workflow")
    print("=" * 60)
    
    # Initialize the search engine
    engine = TechScopeSearchEngine()
    
    # Step 1: Setup crawler
    print("\n1️⃣ Setting up crawler...")
    engine.setup_crawler(['https://example.com'], max_pages=20, crawl_delay=0.005)
    
    # Step 2: Setup indexer
    print("\n2️⃣ Setting up indexer...")
    engine.setup_indexer('data/pages', 'index/data')
    
    # Step 3: Setup query engine
    print("\n3️⃣ Setting up query engine...")
    engine.setup_query_engine('index/data')
    
    # Step 4: Test statistics (before crawling)
    print("\n4️⃣ Testing statistics (before crawling)...")
    stats = engine.get_stats()
    print(f"Status: {stats.get('status', 'Unknown')}")
    print(f"Total Documents: {stats.get('total_documents', 0)}")
    print(f"Total Terms: {stats.get('total_terms', 0)}")
    
    # Step 5: Test search (before indexing)
    print("\n5️⃣ Testing search (before indexing)...")
    results = engine.search("example", max_results=5)
    print(f"Search results: {len(results)} found")
    
    print("\n✅ Complete workflow test finished!")
    print("\n💡 To test with real data, run:")
    print("   python main.py --crawl https://example.com --max-pages 3")
    print("   python main.py --build-index")
    print("   python main.py --search 'your query'")

if __name__ == '__main__':
    test_complete_workflow() 
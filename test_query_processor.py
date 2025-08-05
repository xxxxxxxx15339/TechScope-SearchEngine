#!/usr/bin/env python3
"""
Test script for QueryProcessor
"""

from query.query_processor import QueryProcessor

def test_query_processor():
    print("🧪 Testing QueryProcessor...")
    
    # Initialize processor
    processor = QueryProcessor()
    
    # Test cases
    test_queries = [
        "Python programming language",
        "  JavaScript   &   React  ",
        "Machine Learning with Python!",
        "the quick brown fox",
        "",
        "   "
    ]
    
    for query in test_queries:
        print(f"\n📝 Original: '{query}'")
        cleaned = processor.clean_query(query)
        print(f"🧹 Cleaned: '{cleaned}'")
        tokens = processor.tokenize_query(cleaned)
        print(f"🔤 Tokens: {tokens}")
        
        # Test full pipeline
        processed = processor.process_query(query)
        print(f"⚙️  Processed: {processed}")

if __name__ == "__main__":
    test_query_processor() 
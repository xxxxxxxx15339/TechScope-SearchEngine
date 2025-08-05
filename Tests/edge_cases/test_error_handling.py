import unittest
import sys
import os
import tempfile
import shutil

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.query import Query
from query.query_processor import QueryProcessor
from query.search_engine import SearchEngine
from query.result_formatter import ResultFormatter

class TestErrorHandling(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.query_processor = QueryProcessor()
    
    def test_search_without_index(self):
        """Test search when no index exists."""
        # Create query with non-existent index directory
        query = Query(index_dir='nonexistent_directory')
        results = query.search("python")
        
        # Should return empty results, not crash
        self.assertEqual(results, [])
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        # Create a minimal query instance
        query = Query()
        results = query.search("")
        self.assertEqual(results, [])
    
    def test_search_whitespace_only_query(self):
        """Test search with only whitespace."""
        query = Query()
        results = query.search("   ")
        self.assertEqual(results, [])
    
    def test_search_very_long_query(self):
        """Test search with very long query."""
        query = Query()
        long_query = "python " * 1000  # Very long query
        results = query.search(long_query, max_results=5)
        
        # Should not crash
        self.assertIsInstance(results, list)
    
    def test_search_special_characters(self):
        """Test search with special characters."""
        query = Query()
        special_query = "python & programming !@#$%^&*()"
        results = query.search(special_query, max_results=5)
        
        # Should handle special characters gracefully
        self.assertIsInstance(results, list)
    
    def test_search_unicode_characters(self):
        """Test search with unicode characters."""
        query = Query()
        unicode_query = "python программирование 编程"
        results = query.search(unicode_query, max_results=5)
        
        # Should handle unicode gracefully
        self.assertIsInstance(results, list)
    
    def test_search_numeric_query(self):
        """Test search with numeric query."""
        query = Query()
        numeric_query = "123 456 789"
        results = query.search(numeric_query, max_results=5)
        
        # Should handle numbers gracefully
        self.assertIsInstance(results, list)
    
    def test_search_max_results_edge_cases(self):
        """Test edge cases for max_results parameter."""
        query = Query()
        
        # Test with zero
        results = query.search("python", max_results=0)
        self.assertEqual(results, [])
        
        # Test with negative number
        results = query.search("python", max_results=-1)
        self.assertIsInstance(results, list)
        
        # Test with very large number
        results = query.search("python", max_results=1000000)
        self.assertIsInstance(results, list)
    
    def test_query_processor_edge_cases(self):
        """Test QueryProcessor with edge cases."""
        # Test with None
        result = self.query_processor.clean_query(None)
        self.assertEqual(result, "")
        
        # Test with very long string
        long_string = "a" * 10000
        result = self.query_processor.clean_query(long_string)
        self.assertIsInstance(result, str)
        
        # Test with only special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = self.query_processor.clean_query(special_chars)
        self.assertEqual(result, "")
    
    def test_search_engine_edge_cases(self):
        """Test SearchEngine with edge cases."""
        # Test with empty inverted index
        empty_index = {}
        empty_metadata = {}
        search_engine = SearchEngine(empty_index, empty_metadata)
        
        results = search_engine.search(['python'])
        self.assertEqual(results, {})
        
        # Test with None values
        search_engine = SearchEngine(None, None)
        results = search_engine.search(['python'])
        self.assertEqual(results, {})
    
    def test_result_formatter_edge_cases(self):
        """Test ResultFormatter with edge cases."""
        # Test with empty metadata
        empty_metadata = {}
        formatter = ResultFormatter(empty_metadata)
        
        search_results = {'doc1.html': 1.0}
        formatted = formatter.format_results(search_results, max_results=5)
        
        self.assertEqual(len(formatted), 1)
        self.assertEqual(formatted[0]['doc_id'], 'doc1.html')
        self.assertEqual(formatted[0]['score'], 1.0)
        self.assertNotIn('title', formatted[0])  # No metadata available
    
    def test_malformed_index_files(self):
        """Test handling of malformed index files."""
        # Create temporary directory
        test_dir = tempfile.mkdtemp()
        index_dir = os.path.join(test_dir, 'index')
        os.makedirs(index_dir)
        
        try:
            # Create malformed JSON files
            index_file = os.path.join(index_dir, 'inverted_index.json')
            with open(index_file, 'w') as f:
                f.write('{"malformed": json}')
            
            metadata_file = os.path.join(index_dir, 'document_metadata.json')
            with open(metadata_file, 'w') as f:
                f.write('{"also": malformed}')
            
            # Should handle gracefully
            query = Query(index_dir=index_dir)
            results = query.search("python")
            self.assertEqual(results, [])
            
        finally:
            shutil.rmtree(test_dir)
    
    def test_missing_metadata_fields(self):
        """Test handling of missing metadata fields."""
        # Create test data with missing fields
        test_metadata = {
            'doc1.html': {
                'title': 'Python Guide'
                # Missing url, timestamp, etc.
            },
            'doc2.html': {
                # Missing all fields
            }
        }
        
        formatter = ResultFormatter(test_metadata)
        search_results = {
            'doc1.html': 1.0,
            'doc2.html': 0.5
        }
        
        formatted = formatter.format_results(search_results, max_results=5)
        
        # Should handle missing fields gracefully
        self.assertEqual(len(formatted), 2)
        
        # doc1.html should have available fields
        self.assertEqual(formatted[0]['title'], 'Python Guide')
        self.assertNotIn('url', formatted[0])
        
        # doc2.html should have only basic fields
        self.assertEqual(formatted[1]['doc_id'], 'doc2.html')
        self.assertEqual(formatted[1]['score'], 0.5)
        self.assertNotIn('title', formatted[1])
    
    def test_concurrent_searches(self):
        """Test multiple searches happening simultaneously."""
        query = Query()
        
        # Simulate multiple searches
        import threading
        import time
        
        results_list = []
        errors_list = []
        
        def search_worker(query_text):
            try:
                results = query.search(query_text, max_results=3)
                results_list.append((query_text, results))
            except Exception as e:
                errors_list.append((query_text, str(e)))
        
        # Start multiple search threads
        threads = []
        search_terms = ["python", "javascript", "machine learning", "web development"]
        
        for term in search_terms:
            thread = threading.Thread(target=search_worker, args=(term,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check that all searches completed without errors
        self.assertEqual(len(errors_list), 0, f"Errors occurred: {errors_list}")
        self.assertEqual(len(results_list), len(search_terms))
        
        # All results should be lists
        for query_text, results in results_list:
            self.assertIsInstance(results, list, f"Results for '{query_text}' should be a list")

if __name__ == '__main__':
    unittest.main() 
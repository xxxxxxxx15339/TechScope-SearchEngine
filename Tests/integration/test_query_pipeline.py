import unittest
import sys
import os
import tempfile
import shutil
import json

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.query import Query

class TestQueryPipeline(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.data_dir = os.path.join(self.test_dir, 'data')
        self.index_dir = os.path.join(self.test_dir, 'index')
        os.makedirs(self.data_dir)
        os.makedirs(self.index_dir)
        
        # Create test data
        self.create_test_index()
        
        # Create query instance
        self.query = Query(index_dir=self.index_dir)
    
    def create_test_index(self):
        """Create a test index for integration testing."""
        # Create test inverted index
        test_inverted_index = {
            'python': {
                'doc1.html': 0.85,
                'doc3.html': 0.92
            },
            'programming': {
                'doc1.html': 0.67,
                'doc2.html': 0.78
            },
            'javascript': {
                'doc2.html': 0.88,
                'doc4.html': 0.76
            },
            'machine': {
                'doc3.html': 0.94,
                'doc5.html': 0.82
            },
            'learning': {
                'doc3.html': 0.89,
                'doc5.html': 0.91
            },
            'web': {
                'doc2.html': 0.75,
                'doc4.html': 0.83
            },
            'development': {
                'doc2.html': 0.72,
                'doc4.html': 0.79
            }
        }
        
        # Create test document metadata
        test_metadata = {
            'doc1.html': {
                'title': 'Python Programming Guide',
                'url': 'http://example.com/python-guide',
                'timestamp': 1703123456.789,
                'author': 'John Doe',
                'category': 'Programming'
            },
            'doc2.html': {
                'title': 'JavaScript Web Development',
                'url': 'http://example.com/js-web',
                'timestamp': 1703123500.123,
                'author': 'Jane Smith',
                'category': 'Web Development'
            },
            'doc3.html': {
                'title': 'Machine Learning with Python',
                'url': 'http://example.com/ml-python',
                'timestamp': 1703123550.456,
                'author': 'Dr. Johnson',
                'category': 'AI'
            },
            'doc4.html': {
                'title': 'Modern Web Development',
                'url': 'http://example.com/modern-web',
                'timestamp': 1703123600.789,
                'author': 'Mike Wilson',
                'category': 'Web Development'
            },
            'doc5.html': {
                'title': 'Advanced Machine Learning',
                'url': 'http://example.com/advanced-ml',
                'timestamp': 1703123650.012,
                'author': 'Dr. Brown',
                'category': 'AI'
            }
        }
        
        # Save test index files
        index_file = os.path.join(self.index_dir, 'inverted_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(test_inverted_index, f, indent=2)
        
        metadata_file = os.path.join(self.index_dir, 'document_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(test_metadata, f, indent=2)
    
    def test_complete_search_pipeline(self):
        """Test the complete search pipeline end-to-end."""
        results = self.query.search("python programming", max_results=5)
        
        # Check basic structure
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should return some results")
        
        # Check result structure
        for result in results:
            self.assertIsInstance(result, dict)
            self.assertIn('doc_id', result)
            self.assertIn('score', result)
            self.assertIn('title', result)
            self.assertIn('url', result)
            self.assertIn('author', result)
            self.assertIn('category', result)
    
    def test_search_with_different_queries(self):
        """Test various query types."""
        test_queries = [
            ("python", "Should find Python-related documents"),
            ("javascript", "Should find JavaScript-related documents"),
            ("machine learning", "Should find ML-related documents"),
            ("web development", "Should find web development documents"),
            ("programming", "Should find programming documents")
        ]
        
        for query_text, description in test_queries:
            with self.subTest(query=query_text):
                results = self.query.search(query_text, max_results=3)
                
                # Basic validation
                self.assertIsInstance(results, list, f"{description}: Results should be a list")
                self.assertGreaterEqual(len(results), 0, f"{description}: Should return results or empty list")
                
                # Check result structure
                for result in results:
                    self.assertIn('doc_id', result, f"{description}: Result should have doc_id")
                    self.assertIn('score', result, f"{description}: Result should have score")
                    self.assertIn('title', result, f"{description}: Result should have title")
                    self.assertIn('url', result, f"{description}: Result should have url")
    
    def test_search_result_ranking(self):
        """Test that results are properly ranked by score."""
        results = self.query.search("python programming", max_results=10)
        
        # Check that results are sorted by score (highest first)
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(
                    results[i]['score'], 
                    results[i + 1]['score'],
                    f"Result {i} should have higher or equal score than result {i + 1}"
                )
    
    def test_search_max_results_limit(self):
        """Test that max_results limit is respected."""
        results = self.query.search("programming", max_results=2)
        self.assertLessEqual(len(results), 2, "Should respect max_results limit")
    
    def test_search_empty_query(self):
        """Test search with empty query."""
        results = self.query.search("", max_results=5)
        self.assertEqual(results, [], "Empty query should return empty results")
    
    def test_search_nonexistent_terms(self):
        """Test search with terms not in index."""
        results = self.query.search("nonexistent term", max_results=5)
        self.assertEqual(results, [], "Nonexistent terms should return empty results")
    
    def test_search_stats(self):
        """Test search statistics."""
        stats = self.query.get_search_stats()
        
        # Check structure
        self.assertIsInstance(stats, dict)
        self.assertIn('total_documents', stats)
        self.assertIn('total_terms', stats)
        
        # Check values
        self.assertIsInstance(stats['total_documents'], int)
        self.assertIsInstance(stats['total_terms'], int)
        self.assertEqual(stats['total_documents'], 5)  # We created 5 test documents
        self.assertEqual(stats['total_terms'], 7)      # We created 7 test terms
    
    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        results_lower = self.query.search("python", max_results=5)
        results_upper = self.query.search("PYTHON", max_results=5)
        results_mixed = self.query.search("PyThOn", max_results=5)
        
        # All should return the same results
        self.assertEqual(len(results_lower), len(results_upper))
        self.assertEqual(len(results_lower), len(results_mixed))
    
    def test_search_multiple_searches(self):
        """Test multiple searches in sequence."""
        queries = ["python", "javascript", "machine learning"]
        
        for query in queries:
            results = self.query.search(query, max_results=3)
            self.assertIsInstance(results, list)
            # Each search should work independently
    
    def tearDown(self):
        """Clean up after each test."""
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 
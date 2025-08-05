import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.result_formatter import ResultFormatter

class TestResultFormatter(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_metadata = {
            'doc1.html': {
                'title': 'Python Programming Guide',
                'url': 'http://example.com/python',
                'timestamp': 1703123456.789,
                'author': 'John Doe',
                'category': 'Programming'
            },
            'doc2.html': {
                'title': 'JavaScript Tutorial',
                'url': 'http://example.com/js',
                'timestamp': 1703123500.123,
                'author': 'Jane Smith',
                'category': 'Web Development'
            },
            'doc3.html': {
                'title': 'Machine Learning Basics',
                'url': 'http://example.com/ml',
                'timestamp': 1703123550.456,
                'author': 'Dr. Johnson',
                'category': 'AI'
            }
        }
        
        self.formatter = ResultFormatter(self.test_metadata)
    
    def test_format_results_normal(self):
        """Test normal result formatting"""
        search_results = {
            'doc1.html': 1.85,
            'doc2.html': 0.67
        }
        
        formatted = self.formatter.format_results(search_results, max_results=10)
        
        self.assertEqual(len(formatted), 2)
        
        # Check first result (highest score)
        self.assertEqual(formatted[0]['doc_id'], 'doc1.html')
        self.assertEqual(formatted[0]['score'], 1.85)
        self.assertEqual(formatted[0]['title'], 'Python Programming Guide')
        self.assertEqual(formatted[0]['url'], 'http://example.com/python')
        self.assertEqual(formatted[0]['author'], 'John Doe')
        self.assertEqual(formatted[0]['category'], 'Programming')
        
        # Check second result
        self.assertEqual(formatted[1]['doc_id'], 'doc2.html')
        self.assertEqual(formatted[1]['score'], 0.67)
        self.assertEqual(formatted[1]['title'], 'JavaScript Tutorial')
    
    def test_format_results_limit(self):
        """Test result limiting"""
        search_results = {
            'doc1.html': 1.85,
            'doc2.html': 0.67,
            'doc3.html': 0.45
        }
        
        formatted = self.formatter.format_results(search_results, max_results=2)
        
        self.assertEqual(len(formatted), 2)
        self.assertEqual(formatted[0]['doc_id'], 'doc1.html')  # Highest score
        self.assertEqual(formatted[1]['doc_id'], 'doc2.html')  # Second highest
    
    def test_format_results_empty(self):
        """Test empty search results"""
        formatted = self.formatter.format_results({}, max_results=10)
        self.assertEqual(formatted, [])
    
    def test_format_results_missing_metadata(self):
        """Test results with missing metadata"""
        search_results = {
            'doc1.html': 1.85,
            'unknown_doc.html': 0.67
        }
        
        formatted = self.formatter.format_results(search_results, max_results=10)
        
        self.assertEqual(len(formatted), 2)
        
        # doc1.html should have metadata
        self.assertIn('title', formatted[0])
        self.assertIn('url', formatted[0])
        self.assertIn('author', formatted[0])
        
        # unknown_doc.html should only have basic info
        self.assertEqual(formatted[1]['doc_id'], 'unknown_doc.html')
        self.assertEqual(formatted[1]['score'], 0.67)
        self.assertNotIn('title', formatted[1])
        self.assertNotIn('url', formatted[1])
    
    def test_format_results_sorting(self):
        """Test that results are sorted by score (highest first)"""
        search_results = {
            'doc2.html': 0.67,
            'doc1.html': 1.85,
            'doc3.html': 0.45
        }
        
        formatted = self.formatter.format_results(search_results, max_results=10)
        
        self.assertEqual(len(formatted), 3)
        self.assertEqual(formatted[0]['score'], 1.85)  # Highest
        self.assertEqual(formatted[1]['score'], 0.67)  # Second
        self.assertEqual(formatted[2]['score'], 0.45)  # Lowest
    
    def test_format_results_max_results_zero(self):
        """Test with max_results = 0"""
        search_results = {
            'doc1.html': 1.85,
            'doc2.html': 0.67
        }
        
        formatted = self.formatter.format_results(search_results, max_results=0)
        self.assertEqual(formatted, [])
    
    def test_format_results_max_results_larger_than_results(self):
        """Test when max_results is larger than available results"""
        search_results = {
            'doc1.html': 1.85,
            'doc2.html': 0.67
        }
        
        formatted = self.formatter.format_results(search_results, max_results=10)
        self.assertEqual(len(formatted), 2)  # Should return all available results
    
    def test_format_results_all_metadata_fields(self):
        """Test that all metadata fields are included"""
        search_results = {
            'doc1.html': 1.85
        }
        
        formatted = self.formatter.format_results(search_results, max_results=10)
        
        self.assertEqual(len(formatted), 1)
        result = formatted[0]
        
        # Check all expected fields
        self.assertIn('doc_id', result)
        self.assertIn('score', result)
        self.assertIn('title', result)
        self.assertIn('url', result)
        self.assertIn('timestamp', result)
        self.assertIn('author', result)
        self.assertIn('category', result)
        
        # Check values
        self.assertEqual(result['doc_id'], 'doc1.html')
        self.assertEqual(result['score'], 1.85)
        self.assertEqual(result['title'], 'Python Programming Guide')
        self.assertEqual(result['url'], 'http://example.com/python')
        self.assertEqual(result['timestamp'], 1703123456.789)
        self.assertEqual(result['author'], 'John Doe')
        self.assertEqual(result['category'], 'Programming')

if __name__ == '__main__':
    unittest.main() 
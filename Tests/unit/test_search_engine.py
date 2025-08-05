import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.search_engine import SearchEngine

class TestSearchEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create test data
        self.test_inverted_index = {
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
            }
        }
        
        self.test_metadata = {
            'doc1.html': {'title': 'Python Guide', 'url': 'http://example.com/1'},
            'doc2.html': {'title': 'JS Tutorial', 'url': 'http://example.com/2'},
            'doc3.html': {'title': 'Python Advanced', 'url': 'http://example.com/3'},
            'doc4.html': {'title': 'JavaScript Basics', 'url': 'http://example.com/4'},
            'doc5.html': {'title': 'Machine Learning', 'url': 'http://example.com/5'}
        }
        
        self.search_engine = SearchEngine(self.test_inverted_index, self.test_metadata)
    
    def test_search_single_term(self):
        """Test searching for single term"""
        results = self.search_engine.search(['python'])
        expected = {
            'doc1.html': 0.85,
            'doc3.html': 0.92
        }
        self.assertEqual(results, expected)
    
    def test_search_multiple_terms(self):
        """Test searching for multiple terms"""
        results = self.search_engine.search(['python', 'programming'])
        expected = {
            'doc1.html': 1.52,  # 0.85 + 0.67
            'doc3.html': 0.92,  # only python
            'doc2.html': 0.78   # only programming
        }
        self.assertEqual(results, expected)
    
    def test_search_empty_query(self):
        """Test empty query"""
        results = self.search_engine.search([])
        self.assertEqual(results, {})
    
    def test_search_nonexistent_term(self):
        """Test searching for term not in index"""
        results = self.search_engine.search(['nonexistent'])
        self.assertEqual(results, {})
    
    def test_search_mixed_terms(self):
        """Test mix of existing and non-existing terms"""
        results = self.search_engine.search(['python', 'nonexistent'])
        expected = {
            'doc1.html': 0.85,
            'doc3.html': 0.92
        }
        self.assertEqual(results, expected)
    
    def test_search_three_terms(self):
        """Test searching for three terms"""
        results = self.search_engine.search(['machine', 'learning', 'python'])
        expected = {
            'doc3.html': 2.75,  # 0.94 + 0.89 + 0.92
            'doc5.html': 1.73,  # 0.82 + 0.91
            'doc1.html': 0.85   # only python
        }
        self.assertEqual(results, expected)
    
    def test_search_case_sensitivity(self):
        """Test that search is case insensitive (should be handled by query processor)"""
        results = self.search_engine.search(['PYTHON', 'PROGRAMMING'])
        expected = {
            'doc1.html': 1.52,
            'doc3.html': 0.92,
            'doc2.html': 0.78
        }
        self.assertEqual(results, expected)
    
    def test_search_single_document_match(self):
        """Test when only one document matches all terms"""
        results = self.search_engine.search(['machine', 'learning'])
        expected = {
            'doc3.html': 1.83,  # 0.94 + 0.89
            'doc5.html': 1.73   # 0.82 + 0.91
        }
        self.assertEqual(results, expected)
    
    def test_search_no_overlap(self):
        """Test when terms have no document overlap"""
        results = self.search_engine.search(['python', 'javascript'])
        expected = {
            'doc1.html': 0.85,  # only python
            'doc3.html': 0.92,  # only python
            'doc2.html': 0.88,  # only javascript
            'doc4.html': 0.76   # only javascript
        }
        self.assertEqual(results, expected)

if __name__ == '__main__':
    unittest.main() 
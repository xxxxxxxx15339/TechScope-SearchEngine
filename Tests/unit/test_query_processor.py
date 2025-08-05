import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.query_processor import QueryProcessor

class TestQueryProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.processor = QueryProcessor()
    
    def test_clean_query_normal(self):
        """Test normal query cleaning"""
        result = self.processor.clean_query("Python Programming")
        self.assertEqual(result, "python programming")
    
    def test_clean_query_special_chars(self):
        """Test query with special characters"""
        result = self.processor.clean_query("Python & Programming!")
        self.assertEqual(result, "python programming")
    
    def test_clean_query_empty(self):
        """Test empty query"""
        result = self.processor.clean_query("")
        self.assertEqual(result, "")
    
    def test_clean_query_whitespace(self):
        """Test query with extra whitespace"""
        result = self.processor.clean_query("  Python   Programming  ")
        self.assertEqual(result, "python programming")
    
    def test_clean_query_numbers(self):
        """Test query with numbers"""
        result = self.processor.clean_query("Python 3.9 Programming")
        self.assertEqual(result, "python 39 programming")
    
    def test_clean_query_mixed_case(self):
        """Test query with mixed case"""
        result = self.processor.clean_query("PyThOn PrOgRaMmInG")
        self.assertEqual(result, "python programming")
    
    def test_tokenize_query_normal(self):
        """Test normal tokenization"""
        result = self.processor.tokenize_query("python programming")
        self.assertEqual(result, ["python", "programming"])
    
    def test_tokenize_query_empty(self):
        """Test empty tokenization"""
        result = self.processor.tokenize_query("")
        self.assertEqual(result, [])
    
    def test_tokenize_query_single_word(self):
        """Test single word tokenization"""
        result = self.processor.tokenize_query("python")
        self.assertEqual(result, ["python"])
    
    def test_process_query_complete(self):
        """Test complete query processing"""
        result = self.processor.process_query("Python Programming!")
        self.assertEqual(result, ["python", "programming"])
    
    def test_process_query_complex(self):
        """Test complex query processing"""
        result = self.processor.process_query("Machine Learning with Python & TensorFlow!")
        self.assertEqual(result, ["machine", "learning", "with", "python", "tensorflow"])
    
    def test_process_query_empty(self):
        """Test empty query processing"""
        result = self.processor.process_query("")
        self.assertEqual(result, [])
    
    def test_process_query_whitespace_only(self):
        """Test query with only whitespace"""
        result = self.processor.process_query("   ")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main() 
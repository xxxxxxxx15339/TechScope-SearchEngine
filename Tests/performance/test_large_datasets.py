import unittest
import sys
import os
import time
import tempfile
import shutil
import json
import random
import string

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from query.query import Query

class TestPerformance(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.index_dir = os.path.join(self.test_dir, 'index')
        os.makedirs(self.index_dir)
        
        # Create large test dataset
        self.create_large_test_index()
        
        # Create query instance
        self.query = Query(index_dir=self.index_dir)
    
    def create_large_test_index(self):
        """Create a large test index for performance testing."""
        # Generate large inverted index
        num_documents = 1000
        num_terms = 5000
        
        # Generate random terms
        terms = [''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10))) 
                for _ in range(num_terms)]
        
        # Generate inverted index
        inverted_index = {}
        for term in terms:
            # Each term appears in 1-20 random documents
            num_docs = random.randint(1, 20)
            doc_ids = [f'doc{i}.html' for i in random.sample(range(num_documents), num_docs)]
            scores = {doc_id: round(random.uniform(0.1, 2.0), 3) for doc_id in doc_ids}
            inverted_index[term] = scores
        
        # Generate document metadata
        document_metadata = {}
        for i in range(num_documents):
            doc_id = f'doc{i}.html'
            document_metadata[doc_id] = {
                'title': f'Document {i} - {random.choice(terms)}',
                'url': f'http://example.com/doc{i}',
                'timestamp': 1703123456.789 + i,
                'author': f'Author {i % 100}',
                'category': random.choice(['Programming', 'Web Development', 'AI', 'Data Science'])
            }
        
        # Save test index files
        index_file = os.path.join(self.index_dir, 'inverted_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(inverted_index, f, indent=2)
        
        metadata_file = os.path.join(self.index_dir, 'document_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(document_metadata, f, indent=2)
        
        # Store for reference
        self.test_terms = terms
        self.test_documents = list(document_metadata.keys())
    
    def test_search_speed(self):
        """Test search response time with large dataset."""
        # Test with common search terms
        test_queries = [
            "python programming",
            "machine learning",
            "web development",
            "data science",
            "javascript"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                start_time = time.time()
                results = self.query.search(query, max_results=10)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # Performance assertions
                self.assertLess(response_time, 2.0, f"Search for '{query}' took {response_time:.3f}s, should be under 2s")
                self.assertIsInstance(results, list)
                
                print(f"Query: '{query}' - Time: {response_time:.3f}s - Results: {len(results)}")
    
    def test_large_result_set(self):
        """Test handling large result sets."""
        # Search for a term that appears in many documents
        results = self.query.search("python", max_results=100)
        
        # Should respect max_results limit
        self.assertLessEqual(len(results), 100, "Should respect max_results limit")
        
        # Should be sorted by score
        if len(results) > 1:
            for i in range(len(results) - 1):
                self.assertGreaterEqual(
                    results[i]['score'], 
                    results[i + 1]['score'],
                    "Results should be sorted by score (highest first)"
                )
    
    def test_multiple_searches_performance(self):
        """Test performance of multiple searches in sequence."""
        # Generate random search queries
        random_queries = []
        for _ in range(20):
            # Create random 2-3 word queries
            num_words = random.randint(2, 3)
            query_words = random.sample(self.test_terms, num_words)
            random_queries.append(' '.join(query_words))
        
        total_time = 0
        successful_searches = 0
        
        for query in random_queries:
            start_time = time.time()
            try:
                results = self.query.search(query, max_results=5)
                end_time = time.time()
                
                total_time += (end_time - start_time)
                successful_searches += 1
                
                # Each individual search should be fast
                individual_time = end_time - start_time
                self.assertLess(individual_time, 1.0, f"Individual search took {individual_time:.3f}s")
                
            except Exception as e:
                print(f"Error in search '{query}': {e}")
        
        # Calculate average time
        if successful_searches > 0:
            avg_time = total_time / successful_searches
            print(f"Average search time: {avg_time:.3f}s for {successful_searches} searches")
            
            # Average should be reasonable
            self.assertLess(avg_time, 0.5, f"Average search time {avg_time:.3f}s is too slow")
    
    def test_memory_usage(self):
        """Test memory usage during searches."""
        import psutil
        import os
        
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform multiple searches
        for i in range(50):
            query = f"search term {i}"
            results = self.query.search(query, max_results=10)
        
        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory usage - Initial: {initial_memory:.1f}MB, Final: {final_memory:.1f}MB, Increase: {memory_increase:.1f}MB")
        
        # Memory increase should be reasonable (less than 100MB)
        self.assertLess(memory_increase, 100, f"Memory increase {memory_increase:.1f}MB is too high")
    
    def test_concurrent_search_performance(self):
        """Test performance under concurrent search load."""
        import threading
        import queue
        
        # Test parameters
        num_threads = 10
        searches_per_thread = 5
        
        # Queue for results
        result_queue = queue.Queue()
        error_queue = queue.Queue()
        
        def search_worker(thread_id):
            """Worker function for concurrent searches."""
            for i in range(searches_per_thread):
                query = f"thread{thread_id}_search{i}"
                start_time = time.time()
                
                try:
                    results = self.query.search(query, max_results=5)
                    end_time = time.time()
                    
                    result_queue.put({
                        'thread_id': thread_id,
                        'search_id': i,
                        'time': end_time - start_time,
                        'results_count': len(results)
                    })
                    
                except Exception as e:
                    error_queue.put({
                        'thread_id': thread_id,
                        'search_id': i,
                        'error': str(e)
                    })
        
        # Start threads
        threads = []
        start_time = time.time()
        
        for i in range(num_threads):
            thread = threading.Thread(target=search_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect results
        results = []
        while not result_queue.empty():
            results.append(result_queue.get())
        
        errors = []
        while not error_queue.empty():
            errors.append(error_queue.get())
        
        # Performance assertions
        expected_searches = num_threads * searches_per_thread
        successful_searches = len(results)
        
        print(f"Concurrent test - Total time: {total_time:.3f}s")
        print(f"Successful searches: {successful_searches}/{expected_searches}")
        print(f"Errors: {len(errors)}")
        
        # Should have reasonable success rate
        success_rate = successful_searches / expected_searches
        self.assertGreater(success_rate, 0.8, f"Success rate {success_rate:.2%} is too low")
        
        # Should complete in reasonable time
        self.assertLess(total_time, 30, f"Total time {total_time:.3f}s is too slow")
        
        # Individual search times should be reasonable
        if results:
            avg_search_time = sum(r['time'] for r in results) / len(results)
            self.assertLess(avg_search_time, 1.0, f"Average search time {avg_search_time:.3f}s is too slow")
    
    def test_search_stats_performance(self):
        """Test performance of search statistics."""
        start_time = time.time()
        stats = self.query.get_search_stats()
        end_time = time.time()
        
        stats_time = end_time - start_time
        
        # Should be very fast
        self.assertLess(stats_time, 0.1, f"Stats calculation took {stats_time:.3f}s, should be under 0.1s")
        
        # Check stats structure
        self.assertIsInstance(stats, dict)
        self.assertIn('total_documents', stats)
        self.assertIn('total_terms', stats)
        
        print(f"Search stats - Time: {stats_time:.3f}s, Documents: {stats['total_documents']}, Terms: {stats['total_terms']}")
    
    def tearDown(self):
        """Clean up after each test."""
        shutil.rmtree(self.test_dir)

if __name__ == '__main__':
    unittest.main() 
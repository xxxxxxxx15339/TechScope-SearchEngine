import json
import os
from typing import List, Dict
from .query_processor import QueryProcessor
from .result_formatter import ResultFormatter
from .search_engine import SearchEngine
from index.indexer import Indexer


class Query:
    def __init__(self, index_dir='index/data'):
        self.index_dir = index_dir
        self.query_processor = QueryProcessor()
        # Initialize these to None - they'll be set when we load the index
        self.result_formatter = None
        self.search_engine = None

    
    def search(self, user_query: str, max_results: int = 10) -> List[Dict]:
        inverted_index, document_metadata = self.load_index()

        if inverted_index is None or document_metadata is None:
            print("Warning: Index files not found. Please run the indexer first.")
            return []
        
        # Initialize components with loaded data
        self.result_formatter = ResultFormatter(document_metadata)
        self.search_engine = SearchEngine(inverted_index, document_metadata)
        
        processed_query = self.query_processor.process_query(user_query)
        search_results = self.search_engine.search(processed_query)
        formatted_results = self.result_formatter.format_results(search_results, max_results)

        return formatted_results

    
    def load_index(self):
        indexer = Indexer()
        return indexer.load_index_metadata()
    

    def get_search_stats(self) -> Dict:
        inverted_index, document_metadata = self.load_index()
        
        if inverted_index is None or document_metadata is None:
            return {
                'status': 'No index data available',
                'total_documents': 0,
                'total_terms': 0,
                'index_size': 0
            }

        total_documents = len(document_metadata)
        total_terms = len(inverted_index)
        
        index_size = sum(len(docs) for docs in inverted_index.values())
        
        return {
            'status': 'Index loaded successfully',
            'total_documents': total_documents,
            'total_terms': total_terms,
            'index_size': index_size,
            'average_terms_per_document': round(index_size / total_documents, 2) if total_documents > 0 else 0,
            'index_directory': self.index_dir
        }
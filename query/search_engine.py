from index.indexer import Indexer
from typing import List, Dict


class SearchEngine:
    def __init__(self, inverted_index, document_metadata):
        self.inverted_index = inverted_index
        self.document_metadata = document_metadata

    
    def search(self, query_tokens: List[str]) -> Dict[str, float]:
        if not query_tokens:
            return {}
        
        if self.inverted_index is None:
            return {}

        search_results = {}
        for term in query_tokens:
            # Convert term to lowercase for case-insensitive search
            term_lower = term.lower()
            if term_lower in self.inverted_index:
                term_documents = self.inverted_index[term_lower]

                for doc_id, score in term_documents.items():
                    if doc_id in search_results:
                        search_results[doc_id] += score
                    else:
                        search_results[doc_id] = score 
        
        return search_results

from typing import List
from index.text_processor import TextProcessor

class QueryProcessor:
    def __init__(self):
        self.text_processor = TextProcessor()
    
    def clean_query(self, query: str) -> str:
        if query is None:
            return ""
        cleaned_query = self.text_processor.clean_text(query)
        return cleaned_query
        
    
    def tokenize_query(self, query: str) -> List[str]:
        return query.split()

    def process_query(self, user_query: str) -> List[str]:
        cleaned_query = self.clean_query(user_query)
        tokens = self.tokenize_query(cleaned_query)
        return tokens

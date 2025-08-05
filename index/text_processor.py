from bs4 import BeautifulSoup
import re
from typing import List
import time


class TextProcessor:
    def __init__(self):
        self.stopwords = {
                    # Articles
                    'the', 'a', 'an',
                    # Conjunctions
                    'and', 'or', 'but', 'nor', 'yet', 'so',
                    # Prepositions
                    'in', 'on', 'at', 'to', 'for', 'of', 'by', 'from', 'up', 'down', 'into', 'onto',
                    'through', 'during', 'before', 'after', 'since', 'until', 'against', 'among', 'between',
                    'behind', 'beneath', 'beside', 'beyond', 'inside', 'outside', 'under', 'over', 'above', 'below',
                    # Pronouns
                    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
                    'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs',
                    'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'yourselves', 'themselves',
                    # Common verbs
                    'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall',
                    # Demonstratives
                    'this', 'that', 'these', 'those',
                    # Common words
                    'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now', 'then', 'here', 'there'
        }

    
    def extract_text_from_html(self, html_content) -> str:
        soup = BeautifulSoup(html_content, 'lxml')

        for tag in ['script', 'style']:
            for element in soup.find_all(tag):
                element.decompose()

        text = ' '.join(soup.get_text(separator=' ', strip=True).split())

        return text

    def normalize_tokens(self, token: str) -> str:
        # Convert to lowercase first
        token = token.lower()
        # Replace hyphens with spaces
        token = token.replace('-', ' ')
        # Remove special characters but keep alphanumeric and spaces
        token = re.sub(r'[^a-zA-Z0-9\s]', '', token).strip()
        return token
    

    def clean_text(self, text: str) -> str:

        words = text.split()
        cleaned_words = []

        for word in words:
            cleaned_word = self.normalize_tokens(word)
            
            if ' ' in cleaned_word:
                split_words = cleaned_word.split()
                for split_word in split_words:
                    if split_word and split_word not in self.stopwords:
                        cleaned_words.append(split_word)
            else:           
                if cleaned_word and cleaned_word not in self.stopwords:
                    cleaned_words.append(cleaned_word)        
        
        return ' '.join(cleaned_words)
    
    
    def process_document(self, html_content, metadata=None):
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract title from HTML
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'No title'
        
        # Extract text content
        text = self.extract_text_from_html(html_content)
        cleaned_text = self.clean_text(text)
        tokens = cleaned_text.split()

        if metadata is None:
            metadata = {}
            
        # Add title and URL to metadata
        metadata.update({
            'title': title,
            'url': metadata.get('original_url', 'No URL'),
            'processed_tokens': len(tokens),
            'unique_tokens': len(set(tokens)),
            'processing_timestamp': time.time()
        })
        
        return tokens, metadata

import json
import os

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.document_metadata = {}

    def add_document(self, doc_id, tfidf_scores):
        for word, score in tfidf_scores.items():
            if word not in self.index:
                self.index[word] = {}
            self.index[word][doc_id] = score

    def build_index(self, documents_with_scores):
        for doc_id, tfidf_scores in documents_with_scores.items():
            self.add_document(doc_id, tfidf_scores)
        return self.index

    def get_documents_for_term(self, term):
        if term in self.index:
            return list(self.index[term].keys())  
        else:
            return []

    def get_index_stats(self):
        return {
            'total_documents': len(self.document_metadata),
            'total_terms': len(self.index),
            'index_size_bytes': len(str(self.index))  
        }

    def save_to_file(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.index, f, indent=2)
            print(f'Index saved to {filename}')
        except IOError as e:
            print(f'Error saving index: {e}')

    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
            return True
        except FileNotFoundError:
            print(f"File {filename} not found")
            return False
        except json.JSONDecodeError:
            print(f"Error reading JSON from {filename}")
            return False

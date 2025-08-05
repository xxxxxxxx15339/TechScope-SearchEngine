import json
import os
from text_processor import TextProcessor
from tfidf_calculator import TFIDFCalculator
from inverted_indexer import InvertedIndex

class Indexer:
    def __init__(self, data_dir='data/pages', index_dir='index/data'):
        self.data_dir = data_dir
        self.index_dir = index_dir

        self.text_processor = TextProcessor()
        self.tfidf_calculator = TFIDFCalculator()
        self.inverted_index = InvertedIndex()

    def load_crawled_data(self):
        documents = []
        try:
            all_files = os.listdir(self.data_dir)
            for file in all_files:
                if file.endswith('.html'):
                    documents.append(file)
        except IOError as e:
            print(f'Error reading directory: {e}')
        return documents

    def build_index(self):
        index = {}

        documents = self.load_crawled_data()
        processed_documents = self.process_documents(documents)

        document_metadata = {}
        for doc_id, doc_data in processed_documents.items():
            document_metadata[doc_id] = doc_data['metadata']

        all_tokens = []
        for doc_tokens in processed_documents.values():
            all_tokens.append(doc_tokens['tokens'])

        document_count = self.tfidf_calculator.calculate_document_count(all_tokens)

        for doc_id, doc_data in processed_documents.items():
            term_frequency = self.tfidf_calculator.calculate_term_frequency(doc_data['tokens'])
            tfidf_scores = self.tfidf_calculator.calculate_tfidf_scores(term_frequency, document_count, len(processed_documents))

            index[doc_id] = tfidf_scores

        index = self.inverted_index.build_index(index)

        self.save_index_metadata(index, document_metadata)

        return index

    def process_documents(self, documents):
        processed_documents = {}
        for document in documents:
            if document:
                doc_id = os.path.basename(document).replace('.html', '')
                metadata = {}

                meta_path = os.path.join(self.data_dir, document.replace('.html', '.meta'))

                if os.path.exists(meta_path):
                    try:
                        with open(meta_path, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                    except IOError as e:
                        print(f'Error reading metadata for {doc_id}: {e}')

                html_path = os.path.join(self.data_dir, document)
                html_content = self.read_html_file(html_path)
                if html_content:
                    tokens, metadata = self.text_processor.process_document(html_content, metadata)
                    processed_documents[doc_id] = {
                        'tokens': tokens,
                        'metadata': metadata,
                    }

        return processed_documents

    def read_html_file(self, document):
        try:
            with open(document, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            print(f'Error reading {document}: {e}')
            return None

    def save_index_metadata(self, inverted_index, document_metadata):
        os.makedirs(self.index_dir, exist_ok=True)

        index_file = os.path.join(self.index_dir, 'inverted_index.json')
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(inverted_index, f, indent=2)

        metadata_file = os.path.join(self.index_dir, 'document_metadata.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(document_metadata, f, indent=2)

    def load_index_metadata(self):
        index_file = os.path.join(self.index_dir, 'inverted_index.json')
        metadata_file = os.path.join(self.index_dir, 'document_metadata.json')

        inverted_index = {}
        document_metadata = {}

        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                inverted_index = json.load(f)
        else:
            print(f"Inverted index file not found: {index_file}")
            return None, None

        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                document_metadata = json.load(f)
        else:
            print(f"Metadata file not found: {metadata_file}")

        return inverted_index, document_metadata

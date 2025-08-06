# Indexing Module

## Overview
TF-IDF indexing system that processes crawled HTML content and builds search indices using term frequency-inverse document frequency scoring.

## Architecture

### Core Components
- **TextProcessor**: HTML parsing and text normalization
- **TFIDFCalculator**: TF-IDF score computation with normalization
- **InvertedIndex**: Inverted index construction for fast lookups
- **Indexer**: Main orchestrator for the indexing workflow

### Data Flow
```
HTML Files → Text Processing → TF-IDF Calculation → Inverted Index → Storage
```

## Detailed Component Analysis

### TextProcessor (`text_processor.py`)

#### HTML Text Extraction
```python
def extract_text_from_html(self, html_content) -> str:
    soup = BeautifulSoup(html_content, 'lxml')
    # Remove script and style tags
    for tag in ['script', 'style']:
        for element in soup.find_all(tag):
            element.decompose()
    text = ' '.join(soup.get_text(separator=' ', strip=True).split())
```

**Unusual Concepts:**
- **BeautifulSoup Parser**: HTML parsing with error tolerance
- **Tag Removal**: Eliminates `<script>` and `<style>` content
- **Text Normalization**: Converts HTML to clean text
- **Whitespace Handling**: Consistent space separation

#### Token Normalization
```python
def normalize_tokens(self, token: str) -> str:
    token = token.lower()
    token = token.replace('-', ' ')
    token = re.sub(r'[^a-zA-Z0-9\s]', '', token).strip()
```

**Unusual Concepts:**
- **Case Normalization**: Converts to lowercase
- **Hyphen Handling**: Splits hyphenated words
- **Special Character Removal**: Keeps only alphanumeric and spaces
- **Regex Processing**: Uses `re.sub()` for character filtering

#### Stop Word Filtering
```python
self.stopwords = {
    # Articles: 'the', 'a', 'an'
    # Conjunctions: 'and', 'or', 'but'
    # Prepositions: 'in', 'on', 'at', 'to', 'for'
    # Pronouns: 'i', 'you', 'he', 'she', 'it'
    # Common verbs: 'am', 'is', 'are', 'was', 'were'
    # Demonstratives: 'this', 'that', 'these', 'those'
}
```

**Unusual Concepts:**
- **Comprehensive Stop Words**: 80+ common English words
- **Categorized Filtering**: Articles, conjunctions, prepositions, etc.
- **Frequency-based Removal**: Eliminates high-frequency, low-meaning words
- **Manual Curation**: Carefully selected stop word list

### TFIDFCalculator (`tfidf_calculator.py`)

#### Term Frequency Calculation
```python
def calculate_term_frequency(self, tokens):
    token_count = {}
    for token in tokens:
        token_count[token] = token_count.get(token, 0) + 1
    
    total_tokens = len(tokens)
    for token in token_count:
        token_count[token] = token_count[token] / total_tokens
```

**Unusual Concepts:**
- **Frequency Normalization**: Divides by total tokens
- **Relative Frequency**: Measures term importance within document
- **Dictionary-based Counting**: Efficient token counting
- **Float Precision**: Maintains decimal precision for accuracy

#### Document Frequency Calculation
```python
def calculate_document_count(self, all_tokens):
    doc_count = {}
    for doc in all_tokens:
        unique_words = set(doc)  # Only count once per document
        for word in unique_words:
            doc_count[word] = doc_count.get(word, 0) + 1
```

**Unusual Concepts:**
- **Set-based Uniqueness**: Counts each term only once per document
- **Cross-document Analysis**: Measures term distribution across corpus
- **Inverse Relationship**: Rare terms get higher IDF scores
- **Corpus-wide Statistics**: Global term frequency analysis

#### TF-IDF Score Computation
```python
def calculate_tfidf_scores(self, term_frequencies, document_counts, total_documents):
    tfidf_scores = {}
    for word, tf in term_frequencies.items():
        df = document_counts.get(word, 0)
        if df > 0:
            idf = math.log(total_documents / df)
        else:
            idf = 0
        tfidf_scores[word] = tf * idf
```

**Unusual Concepts:**
- **Logarithmic IDF**: `log(N/df)` for inverse document frequency
- **Zero Division Protection**: Handles terms not in document count
- **Multiplication**: TF × IDF for final score
- **Mathematical Precision**: Uses `math.log()` for accuracy

#### Vector Normalization
```python
def normalize_score(self, tfidf_scores):
    magnitude = math.sqrt(sum(score ** 2 for score in tfidf_scores.values()))
    normalized_scores = {}
    for word, score in tfidf_scores.items():
        if magnitude > 0:
            normalized_scores[word] = score / magnitude
        else:
            normalized_scores[word] = 0
```

**Unusual Concepts:**
- **L2 Normalization**: Divides by vector magnitude
- **Cosine Similarity Preparation**: Enables cosine similarity calculations
- **Zero Magnitude Handling**: Prevents division by zero
- **Unit Vector Conversion**: Normalizes to unit vectors

### Indexer (`indexer.py`)

#### Document Processing Workflow
```python
def process_documents(self, documents):
    processed_documents = {}
    for document in documents:
        doc_id = os.path.basename(document).replace('.html', '')
        html_content = self.read_html_file(html_path)
        tokens, metadata = self.text_processor.process_document(html_content, metadata)
        processed_documents[doc_id] = {
            'tokens': tokens,
            'metadata': metadata,
        }
```

**Unusual Concepts:**
- **File-based Processing**: Processes HTML files from disk
- **Metadata Preservation**: Maintains crawl metadata
- **Token Extraction**: Converts documents to token lists
- **Batch Processing**: Handles multiple documents efficiently

#### Index Building Process
```python
def build_index(self):
    documents = self.load_crawled_data()
    processed_documents = self.process_documents(documents)
    
    all_tokens = [doc_tokens['tokens'] for doc_tokens in processed_documents.values()]
    document_count = self.tfidf_calculator.calculate_document_count(all_tokens)
    
    for doc_id, doc_data in processed_documents.items():
        term_frequency = self.tfidf_calculator.calculate_term_frequency(doc_data['tokens'])
        tfidf_scores = self.tfidf_calculator.calculate_tfidf_scores(
            term_frequency, document_count, len(processed_documents)
        )
        index[doc_id] = tfidf_scores
```

**Unusual Concepts:**
- **Two-pass Algorithm**: First pass for document frequency, second for TF-IDF
- **Corpus-wide Analysis**: Requires all documents for IDF calculation
- **Memory Management**: Processes documents in batches
- **Score Computation**: Calculates TF-IDF for each term-document pair

## Data Structures

### Document Metadata
```json
{
  "title": "Page Title",
  "url": "https://example.com",
  "processed_tokens": 150,
  "unique_tokens": 89,
  "processing_timestamp": 1640995200.0
}
```

### TF-IDF Matrix
```python
{
  "doc_id_1": {
    "python": 0.85,
    "programming": 0.72,
    "tutorial": 0.45
  },
  "doc_id_2": {
    "web": 0.91,
    "development": 0.68,
    "framework": 0.53
  }
}
```

### Inverted Index
```python
{
  "python": ["doc_id_1", "doc_id_3", "doc_id_7"],
  "web": ["doc_id_2", "doc_id_4", "doc_id_8"],
  "development": ["doc_id_2", "doc_id_5", "doc_id_9"]
}
```

## Performance Characteristics

### Time Complexity
- **Text Processing**: O(n) where n is document length
- **TF Calculation**: O(m) where m is unique terms
- **IDF Calculation**: O(k×d) where k is terms, d is documents
- **Index Building**: O(d×m) for complete index

### Memory Usage
- **Token Storage**: Stores all processed tokens
- **TF-IDF Matrix**: Sparse matrix representation
- **Metadata**: JSON storage for document info
- **Inverted Index**: Term-to-document mapping

## Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `data_dir` | 'data/pages' | HTML file location |
| `index_dir` | 'index/data' | Index storage location |
| `stop_words` | 80+ words | Filtered terms |
| `normalization` | L2 | Vector normalization |

## Output Files

### `inverted_index.json`
```json
{
  "term1": ["doc1", "doc2", "doc3"],
  "term2": ["doc2", "doc4", "doc5"]
}
```

### `document_metadata.json`
```json
{
  "doc_id_1": {
    "title": "Page Title",
    "url": "https://example.com",
    "processed_tokens": 150,
    "unique_tokens": 89
  }
}
```

## Limitations & Enhancements

### Current Limitations
- **Single-pass Processing**: Requires all documents in memory
- **Basic Normalization**: Simple text cleaning
- **No Stemming**: Doesn't reduce word variations
- **Fixed Stop Words**: Hard-coded stop word list

### Future Enhancements
- **Stemming**: Porter/Lancaster stemming
- **Lemmatization**: Word form normalization
- **Dynamic Stop Words**: Corpus-based stop word detection
- **Incremental Indexing**: Add documents without full rebuild
- **Compression**: Compress index for large datasets

## Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end indexing
- **Performance Tests**: Large document processing
- **Edge Cases**: Empty documents, special characters 
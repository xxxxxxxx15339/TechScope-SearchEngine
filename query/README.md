# Query Processing Module

## Overview
Search engine that processes user queries and returns ranked results using inverted index lookups and score aggregation.

## Architecture

### Core Components
- **QueryProcessor**: Query preprocessing and tokenization
- **SearchEngine**: Core search algorithm using inverted index
- **ResultFormatter**: Result ranking and metadata enrichment
- **Query**: Main interface orchestrating the search workflow

### Data Flow
```
User Query → Query Processing → Inverted Index Lookup → Score Aggregation → Result Formatting
```

## Detailed Component Analysis

### QueryProcessor (`query_processor.py`)

#### Query Processing
```python
def process_query(self, query: str) -> List[str]:
    # Uses same text processing as document indexing
    # Tokenization, normalization, stop word removal
```

**Unusual Concepts:**
- **Consistent Processing**: Same pipeline as document processing
- **Token Normalization**: Lowercase, special character removal
- **Stop Word Filtering**: Removes common words
- **Query-document Parity**: Ensures query and documents use same representation

### SearchEngine (`search_engine.py`)

#### Inverted Index Search
```python
def search(self, query_tokens: List[str]) -> Dict[str, float]:
    search_results = {}
    for term in query_tokens:
        term_lower = term.lower()
        if term_lower in self.inverted_index:
            term_documents = self.inverted_index[term_lower]
            for doc_id, score in term_documents.items():
                if doc_id in search_results:
                    search_results[doc_id] += score
                else:
                    search_results[doc_id] = score
```

**Unusual Concepts:**
- **Inverted Index Lookup**: O(1) term-to-document mapping
- **Score Aggregation**: Sums scores across multiple query terms
- **Case Insensitive**: Converts terms to lowercase
- **Document Scoring**: Accumulates scores for documents containing query terms

#### Search Algorithm Details
- **Boolean OR**: Documents containing any query term are considered
- **Score Addition**: Multiple matching terms increase document score
- **No Cosine Similarity**: Uses simple score aggregation instead
- **Term Independence**: Each query term contributes independently

### ResultFormatter (`result_formatter.py`)

#### Result Ranking
```python
def format_results(self, search_results: Dict[str, float], max_results: int):
    sorted_items = sorted(search_results.items(), key=lambda x: x[1], reverse=True)
    sorted_results = dict(sorted_items[:max_results])
```

**Unusual Concepts:**
- **Score-based Sorting**: Descending order by relevance score
- **Result Limiting**: Configurable maximum results
- **Tuple Sorting**: Uses `key=lambda x: x[1]` for score-based sort
- **Dictionary Conversion**: Converts back to dict after limiting

#### Metadata Enrichment
```python
def add_metadata(self, results: Dict[str, float]) -> List[Dict]:
    formatted_results = []
    for key, value in results.items():
        result_metadata = {'doc_id': key, 'score': value}
        for doc_id, metadata in self.document_metadata.items():
            if doc_id == key:
                for meta_key, meta_value in metadata.items():
                    if meta_key != 'score' and meta_key != 'doc_id':
                        result_metadata[meta_key] = meta_value
```

**Unusual Concepts:**
- **Metadata Merging**: Combines search scores with document metadata
- **Field Filtering**: Excludes redundant fields
- **Document Enrichment**: Adds title, URL, processing info
- **Result Structure**: Creates rich result objects

### Query (`query.py`)

#### Main Search Interface
```python
def search(self, user_query: str, max_results: int = 10) -> List[Dict]:
    inverted_index, document_metadata = self.load_index()
    processed_query = self.query_processor.process_query(user_query)
    search_results = self.search_engine.search(processed_query)
    formatted_results = self.result_formatter.format_results(search_results, max_results)
```

**Unusual Concepts:**
- **Index Loading**: Loads pre-built inverted index and metadata
- **Component Orchestration**: Coordinates all search components
- **Error Handling**: Returns empty list if index not found
- **Result Pipeline**: Processes query through complete pipeline

#### Statistics Interface
```python
def get_search_stats(self) -> Dict:
    total_documents = len(document_metadata)
    total_terms = len(inverted_index)
    index_size = sum(len(docs) for docs in inverted_index.values())
```

**Unusual Concepts:**
- **Index Statistics**: Provides corpus-level information
- **Term Distribution**: Counts unique terms in index
- **Document Coverage**: Measures index completeness
- **Performance Metrics**: Helps understand search capabilities

## Data Structures

### Inverted Index Format
```python
{
  "python": {
    "doc_id_1": 0.85,
    "doc_id_3": 0.72,
    "doc_id_7": 0.45
  },
  "web": {
    "doc_id_2": 0.91,
    "doc_id_4": 0.68,
    "doc_id_8": 0.53
  }
}
```

### Search Results Format
```python
[
  {
    "doc_id": "doc_id_1",
    "score": 0.85,
    "title": "Python Web Development Tutorial",
    "url": "https://example.com/tutorial",
    "processed_tokens": 150,
    "unique_tokens": 89
  },
  {
    "doc_id": "doc_id_2", 
    "score": 0.72,
    "title": "Django Framework Guide",
    "url": "https://example.com/django",
    "processed_tokens": 200,
    "unique_tokens": 120
  }
]
```

## Search Algorithm Analysis

### Scoring Mechanism
- **Term Matching**: Documents containing query terms get scores
- **Score Aggregation**: Multiple matching terms add their scores
- **No Normalization**: Raw TF-IDF scores used directly
- **Simple Addition**: `score = sum(term_scores)`

### Ranking Strategy
- **Score-based Sorting**: Higher scores rank first
- **No Cosine Similarity**: Doesn't use vector similarity
- **Boolean OR Logic**: Any matching term includes document
- **Configurable Results**: User-specified result limit

## Performance Characteristics

### Time Complexity
- **Query Processing**: O(n) where n is query length
- **Index Lookup**: O(k) where k is query terms
- **Score Aggregation**: O(d) where d is matching documents
- **Result Sorting**: O(d log d) for ranking

### Memory Usage
- **Index Loading**: Loads full inverted index into memory
- **Metadata Storage**: Keeps document metadata in memory
- **Result Processing**: Temporary storage for search results
- **Score Accumulation**: Dictionary for document scores

## Configuration Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `max_results` | 10 | Maximum results to return |
| `index_dir` | 'index/data' | Index file location |
| `case_sensitive` | False | Case-insensitive search |
| `score_threshold` | None | Minimum score filter |

## Search Features

### Query Processing
- **Tokenization**: Splits query into individual terms
- **Normalization**: Lowercase and special character removal
- **Stop Word Removal**: Filters common words
- **Consistent Processing**: Same pipeline as document indexing

### Result Formatting
- **Score Ranking**: Descending order by relevance
- **Metadata Enrichment**: Adds title, URL, processing info
- **Result Limiting**: Configurable maximum results
- **Rich Output**: Structured result objects

### Error Handling
- **Index Validation**: Checks for required index files
- **Empty Query**: Handles queries with no valid terms
- **Missing Metadata**: Graceful handling of missing document info
- **No Results**: Returns empty list when no matches

## Limitations & Enhancements

### Current Limitations
- **Simple Scoring**: No cosine similarity or advanced ranking
- **Boolean Logic**: Only OR operations, no AND/NOT
- **No Phrase Search**: Doesn't handle multi-word phrases
- **Fixed Ranking**: No personalization or context

### Future Enhancements
- **Cosine Similarity**: Vector-based relevance scoring
- **Phrase Matching**: Multi-word query support
- **Boolean Operators**: AND, OR, NOT query support
- **Result Highlighting**: Show matching terms in results
- **Query Expansion**: Synonym and related term matching
- **Personalization**: User-specific ranking adjustments

## Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end search workflow
- **Performance Tests**: Large index search speed
- **Edge Cases**: Empty queries, missing terms, malformed data 
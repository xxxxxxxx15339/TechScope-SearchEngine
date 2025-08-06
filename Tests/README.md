# Testing Suite

## Overview
Comprehensive testing suite for the TechScope Search Engine with 200+ tests covering unit, integration, performance, and edge case scenarios.

## Testing Strategy

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Large dataset and speed testing
- **Edge Case Tests**: Error handling and boundary conditions

### Test Coverage
- **Crawler Module**: URL processing, HTML extraction, link discovery
- **Index Module**: TF-IDF calculations, text processing, index building
- **Query Module**: Search algorithms, result formatting, query processing
- **Main Application**: Complete workflow integration

## Test Structure

```
Tests/
├── unit/                    # Unit tests for individual components
│   ├── test_query_processor.py
│   ├── test_search_engine.py
│   └── test_result_formatter.py
├── integration/             # End-to-end workflow tests
│   └── test_query_pipeline.py
├── performance/             # Performance and scalability tests
│   └── test_large_datasets.py
├── edge_cases/             # Error handling and boundary tests
│   └── test_error_handling.py
└── __init__.py
```

## Detailed Test Analysis

### Unit Tests (`unit/`)

#### TestQueryProcessor (`test_query_processor.py`)
```python
def test_clean_query_normal(self):
    """Test normal query cleaning"""
    result = self.processor.clean_query("Python Programming")
    self.assertEqual(result, "python programming")
```

**Test Coverage:**
- **Query Normalization**: Case conversion, special character removal
- **Tokenization**: Word splitting and processing
- **Edge Cases**: Empty queries, whitespace handling
- **Special Characters**: Numbers, punctuation, mixed case

**Unusual Test Cases:**
- **Mixed Case**: "PyThOn PrOgRaMmInG" → "python programming"
- **Special Characters**: "Python & Programming!" → "python programming"
- **Numbers**: "Python 3.9 Programming" → "python 39 programming"
- **Whitespace**: "  Python   Programming  " → "python programming"

#### TestSearchEngine (`test_search_engine.py`)
```python
def test_search_with_inverted_index(self):
    """Test search using inverted index"""
    # Tests inverted index lookup and score aggregation
```

**Test Coverage:**
- **Inverted Index Lookup**: Term-to-document mapping
- **Score Aggregation**: Multiple term score addition
- **Case Insensitive**: Lowercase term matching
- **Result Ranking**: Score-based sorting

#### TestResultFormatter (`test_result_formatter.py`)
```python
def test_format_results_with_metadata(self):
    """Test result formatting with document metadata"""
    # Tests result ranking and metadata enrichment
```

**Test Coverage:**
- **Result Ranking**: Score-based sorting
- **Metadata Enrichment**: Title, URL, processing info
- **Result Limiting**: Configurable maximum results
- **Output Formatting**: Structured result objects

### Integration Tests (`integration/`)

#### TestQueryPipeline (`test_query_pipeline.py`)
```python
def test_complete_search_pipeline(self):
    """Test complete search workflow from query to results"""
    # Tests end-to-end search functionality
```

**Test Coverage:**
- **Complete Workflow**: Query → Processing → Search → Results
- **Index Loading**: Inverted index and metadata loading
- **Component Integration**: All modules working together
- **Data Persistence**: File-based index storage

**Unusual Test Features:**
- **Temporary File System**: Creates isolated test environment
- **Mock Index Data**: Generates realistic test data
- **Cleanup Procedures**: Automatic test data removal
- **Multiple Scenarios**: Different query types and result sets

### Performance Tests (`performance/`)

#### TestPerformance (`test_large_datasets.py`)
```python
def test_search_speed(self):
    """Test search response time with large dataset"""
    # Tests performance with 1000 documents, 5000 terms
```

**Test Coverage:**
- **Large Datasets**: 1000 documents, 5000 unique terms
- **Response Time**: <2 second performance threshold
- **Memory Usage**: Efficient memory consumption
- **Concurrent Searches**: Multiple simultaneous queries

**Performance Metrics:**
- **Search Speed**: Measures response time for various queries
- **Memory Efficiency**: Monitors memory usage during operations
- **Scalability**: Tests with increasing dataset sizes
- **Concurrency**: Multiple simultaneous search operations

**Unusual Test Features:**
- **Random Data Generation**: Creates realistic test datasets
- **Performance Thresholds**: Enforces speed requirements
- **Memory Monitoring**: Tracks memory usage patterns
- **Concurrent Testing**: Simulates multiple users

### Edge Case Tests (`edge_cases/`)

#### TestErrorHandling (`test_error_handling.py`)
```python
def test_search_without_index(self):
    """Test search when no index exists"""
    # Tests graceful error handling
```

**Test Coverage:**
- **Missing Index**: Handles non-existent index files
- **Empty Queries**: Processes queries with no content
- **Special Characters**: Handles unicode and special chars
- **Malformed Data**: Processes corrupted or invalid data

**Edge Cases Tested:**
- **Very Long Queries**: 1000+ word queries
- **Unicode Characters**: Non-English text handling
- **Numeric Queries**: Number-only searches
- **Malformed Index**: Corrupted JSON files
- **Missing Metadata**: Incomplete document information

## Running Tests

### Complete Test Suite
```bash
# Run all tests
python run_tests.py

# Run with coverage
python -m pytest Tests/ --cov=. --cov-report=html
```

### Individual Test Categories
```bash
# Unit tests only
python -m pytest Tests/unit/

# Integration tests only
python -m pytest Tests/integration/

# Performance tests only
python -m pytest Tests/performance/

# Edge case tests only
python -m pytest Tests/edge_cases/
```

### Specific Test Files
```bash
# Test specific component
python -m pytest Tests/unit/test_query_processor.py

# Test with verbose output
python -m pytest Tests/unit/test_query_processor.py -v

# Test with coverage
python -m pytest Tests/unit/test_query_processor.py --cov=query
```

## Test Data Management

### Temporary Test Environment
```python
def setUp(self):
    """Create isolated test environment"""
    self.test_dir = tempfile.mkdtemp()
    self.data_dir = os.path.join(self.test_dir, 'data')
    self.index_dir = os.path.join(self.test_dir, 'index')
```

**Features:**
- **Isolated Environment**: Each test gets clean directory
- **Automatic Cleanup**: Removes test files after completion
- **No Cross-contamination**: Tests don't interfere with each other
- **Realistic Data**: Uses actual file formats and structures

### Mock Data Generation
```python
def create_test_index(self):
    """Generate realistic test data"""
    test_inverted_index = {
        'python': {'doc1.html': 0.85, 'doc3.html': 0.92},
        'programming': {'doc1.html': 0.67, 'doc2.html': 0.78}
    }
```

**Data Characteristics:**
- **Realistic Scores**: TF-IDF scores in expected ranges
- **Varied Content**: Different document types and sizes
- **Metadata Richness**: Complete document information
- **Edge Case Coverage**: Includes problematic data scenarios

## Performance Benchmarks

### Speed Requirements
- **Search Response**: <100ms for typical queries
- **Large Dataset**: <2s for 1000+ documents
- **Memory Usage**: Efficient for large indices
- **Concurrent Operations**: Multiple simultaneous searches

### Scalability Testing
- **Document Count**: 100 → 1000 → 10000 documents
- **Term Count**: 1000 → 5000 → 10000 unique terms
- **Query Complexity**: Single terms → Multi-term → Complex phrases
- **Result Sets**: 10 → 100 → 1000 results

## Error Handling Validation

### Graceful Degradation
- **Missing Files**: Continues operation with empty results
- **Corrupted Data**: Handles malformed JSON gracefully
- **Network Errors**: Continues despite connection issues
- **Memory Issues**: Handles large datasets efficiently

### Boundary Conditions
- **Empty Inputs**: Handles null/empty queries
- **Very Long Inputs**: Processes 1000+ word queries
- **Special Characters**: Unicode, symbols, numbers
- **Extreme Values**: Very large result limits

## Test Reporting

### Coverage Metrics
- **Line Coverage**: Percentage of code executed
- **Branch Coverage**: Decision point coverage
- **Function Coverage**: Method execution tracking
- **Statement Coverage**: Individual statement execution

### Performance Reports
- **Response Times**: Average, min, max search times
- **Memory Usage**: Peak memory consumption
- **Throughput**: Queries per second
- **Scalability**: Performance vs dataset size

## Continuous Integration

### Automated Testing
- **Pre-commit Hooks**: Run tests before commits
- **CI/CD Pipeline**: Automated test execution
- **Coverage Reports**: Track test coverage over time
- **Performance Regression**: Monitor speed changes

### Quality Gates
- **Minimum Coverage**: 95%+ test coverage required
- **Performance Thresholds**: Speed requirements enforced
- **Error Handling**: All edge cases must pass
- **Integration Tests**: End-to-end workflows validated

## Best Practices

### Test Design
- **Isolation**: Each test is independent
- **Deterministic**: Tests produce consistent results
- **Fast Execution**: Tests complete quickly
- **Clear Naming**: Descriptive test method names

### Data Management
- **Temporary Files**: Use tempfile for test data
- **Automatic Cleanup**: Remove test files after completion
- **Realistic Data**: Use data similar to production
- **Edge Cases**: Include problematic scenarios

### Performance Testing
- **Baseline Metrics**: Establish performance benchmarks
- **Regression Detection**: Monitor for performance degradation
- **Scalability Testing**: Test with increasing data sizes
- **Resource Monitoring**: Track memory and CPU usage

## Future Enhancements

### Planned Improvements
- **Property-based Testing**: Generate test cases automatically
- **Fuzzing Tests**: Random input testing
- **Load Testing**: High-concurrency scenarios
- **Stress Testing**: Resource exhaustion scenarios

### Advanced Features
- **Parallel Test Execution**: Run tests concurrently
- **Test Data Factories**: Generate realistic test data
- **Performance Profiling**: Detailed performance analysis
- **Visual Test Reports**: Graphical test result display 
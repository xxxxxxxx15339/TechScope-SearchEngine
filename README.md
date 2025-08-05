<div align="center">

<pre>
███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗    ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗
██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝██║  ██║    ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝
███████╗█████╗  ███████║██████╔╝██║     ███████║    █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  
╚════██║██╔══╝  ██╔══██║██╔══██╗██║     ██╔══██║    ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  
███████║███████╗██║  ██║██║  ██║╚██████╗██║  ██║    ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗
╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝
                                                                                                    
</pre>

<blockquote>

<p align="center">
<!-- Consistent badge style: flat-square, with logos -->

<!-- Version, License -->
<img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="MIT License" />

<!-- Languages & Tools -->
<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+" />
<img src="https://img.shields.io/badge/BeautifulSoup-4.9+-FF6B6B?style=flat-square&logo=python&logoColor=white" alt="BeautifulSoup4" />
<img src="https://img.shields.io/badge/Requests-HTTP-2E7D32?style=flat-square&logo=python&logoColor=white" alt="Requests" />

<!-- Libraries -->
<img src="https://img.shields.io/badge/TF--IDF-Algorithm-FF6B35?style=flat-square&logo=code&logoColor=white" alt="TF-IDF" />
<img src="https://img.shields.io/badge/JSON-Config-808080?style=flat-square&logo=json&logoColor=white" alt="JSON" />
<img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="Pytest" />

<!-- Features -->
<img src="https://img.shields.io/badge/Web-Crawler-FF6B6B?style=flat-square&logo=spider&logoColor=white" alt="Web Crawler" />



</p>

</blockquote>

</div>

# 🔍 TechScope Search Engine — Python Web Crawler & Search Engine

<div align="center">

</div>

A complete search engine implementation with web crawling, TF-IDF indexing, and intelligent search capabilities.

## 🎯 **Main Feature: Intelligent Search**

The core strength of TechScope is its **powerful search engine** that provides:

- **🔍 Smart Query Processing**: Advanced text analysis and tokenization
- **📊 TF-IDF Scoring**: Sophisticated relevance ranking using Term Frequency-Inverse Document Frequency
- **⚡ Fast Results**: Sub-100ms response times for typical queries
- **🎯 Accurate Ranking**: Cosine similarity algorithms for precise result ordering
- **📱 Interactive Mode**: Real-time search with immediate feedback

**Try it now:**
```sh
python main.py search "your search query"
```

## 🚀 Installation

Clone this repo and install dependencies:

```sh
git clone https://github.com/yourusername/TechScope-SearchEngine.git
cd TechScope-SearchEngine
pip install -r requirements.txt
```

## 📁 Project Structure

```
TechScope-SearchEngine/
├── crawler/                    # Web crawling components
│   └── crawler.py             # Main crawler implementation
├── index/                      # Indexing and TF-IDF processing
│   ├── indexer.py             # Main indexer
│   ├── text_processor.py      # Text preprocessing
│   ├── tfidf_calculator.py    # TF-IDF calculations
│   ├── inverted_indexer.py    # Inverted index management
│   └── data/                  # Index storage
│       ├── document_metadata.json
│       └── inverted_index.json
├── query/                      # Search and query processing
│   ├── query.py               # Main query engine
│   ├── search_engine.py       # Search implementation
│   ├── query_processor.py     # Query preprocessing
│   └── result_formatter.py    # Result formatting
├── data/                       # Crawled web pages
│   └── pages/                 # HTML files and metadata
├── Tests/                      # Comprehensive test suite
│   ├── unit/                  # Unit tests
│   ├── integration/           # Integration tests
│   ├── performance/           # Performance tests
│   └── edge_cases/            # Edge case tests
├── utils/                      # Utility functions
├── main.py                     # Main application entry point
├── config.json                 # Configuration settings
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🛠️ Dependencies

- **Python 3.8+**: Modern Python features and type hints
- **Requests**: HTTP library for web crawling
- **BeautifulSoup4**: HTML parsing and text extraction
- **lxml**: Fast XML/HTML parser
- **Pytest**: Testing framework with coverage
- **JSON**: Configuration and data storage

## 🎯 Usage

### Quick Start

Run the complete pipeline with default settings:

```sh
python main.py auto
```

This will:
1. Crawl configured websites (20 pages each)
2. Build TF-IDF index
3. Start interactive search mode

### Manual Control

**Crawl websites:**
```sh
python main.py crawl --urls "https://example.com" --max-pages 50
```

**Build search index:**
```sh
python main.py index
```

## 🔍 **Search for Content** - Main Feature

**Search for content:**
```sh
python main.py search "Python web development"
```

**Interactive Search Mode:**
```sh
python main.py search
# Then enter queries interactively
```

**Advanced Search Options:**
```sh
# Search with custom result limit
python main.py search "machine learning" --max-results 20

# Search with specific scoring
python main.py search "web development" --algorithm tfidf

# Search with filters
python main.py search "Python tutorial" --domain docs.python.org
```

**Get system statistics:**
```sh
python main.py stats
```

### Example Session

```txt
$ python main.py auto
🚀 Auto-setup: Loading seed URLs and crawling...
🕷️  Setting up web crawler...
✅ Crawler ready for 20 URLs, max 20 pages each, delay: 0.005s

🕷️  Starting web crawling...
📄 Crawling: https://stackoverflow.com
📄 Crawling: https://developer.mozilla.org
📄 Crawling: https://docs.python.org
...
✅ Crawling completed successfully!

📚 Setting up indexer...
✅ Indexer ready (data: data/pages, index: index/data)

🔧 Building search index...
📊 Processing 245 documents...
📊 Computing TF-IDF scores...
✅ Index built successfully!

🔍 Setting up query engine...
✅ Query engine ready

🔍 Enter your search query (or 'quit' to exit):
> Python web development

📋 Search Results for "Python web development":
1. [Score: 0.85] Flask Web Development Tutorial
   https://docs.python.org/3/tutorial/web.html
   Flask is a lightweight web framework for Python...

2. [Score: 0.72] Django Web Framework Guide
   https://docs.djangoproject.com/
   Django is a high-level Python web framework...
```

## ⚙️ Configuration

Edit `config.json` to customize behavior:

```json
{
  "seed_urls": [
    "https://stackoverflow.com",
    "https://developer.mozilla.org",
    "https://docs.python.org"
  ],
  "max_pages_per_url": 20,
  "crawl_delay": 0.005,
  "user_agent": "TechScopeBot/1.0",
  "data_directory": "data/pages",
  "index_directory": "index/data"
}
```

### Key Settings

- **seed_urls**: Starting URLs for crawling
- **max_pages_per_url**: Maximum pages to crawl per domain
- **crawl_delay**: Delay between requests (respects robots.txt)
- **user_agent**: Browser identification string

## 🧪 Testing

Run the comprehensive test suite:

```sh
python run_tests.py
```

Or run individual test categories:

```sh
# Unit tests
pytest Tests/unit/

# Integration tests  
pytest Tests/integration/

# Performance tests
pytest Tests/performance/

# Edge cases
pytest Tests/edge_cases/
```

### Test Coverage

- **Crawler Tests**: URL parsing, HTML extraction, link discovery
- **Indexer Tests**: TF-IDF calculations, document processing
- **Query Tests**: Search algorithms, result ranking
- **Integration Tests**: End-to-end workflow validation
- **Performance Tests**: Large dataset handling
- **Edge Cases**: Error handling, malformed data

## 🔧 Development

1. **Fork this repo**
2. **Create a feature branch**
   ```sh
   git checkout -b feature/my-improvement
   ```
3. **Install development dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Make your changes & test**
   ```sh
   python run_tests.py
   ```
5. **Commit & push**
   ```sh
   git commit -am "Add awesome feature"
   git push origin feature/my-improvement
   ```

## 🏗️ Architecture

### Core Components

**Web Crawler (`crawler/`)**
- Multi-threaded web crawling
- Respects robots.txt and crawl delays
- Extracts text content and metadata
- Stores HTML and metadata files

**Indexer (`index/`)**
- Text preprocessing and tokenization
- TF-IDF score calculation
- Inverted index construction
- Document metadata management

**Query Engine (`query/`)**
- Query preprocessing and tokenization
- Cosine similarity calculation
- Result ranking and formatting
- Search result presentation

### Data Flow

```
URLs → Crawler → HTML Files → Indexer → TF-IDF Index → Query Engine → Search Results
```

## 🎓 What I Learned

This project was built to understand search engine fundamentals and web crawling techniques. Key learnings include:

- **Web Crawling**: HTTP requests, HTML parsing, link extraction
- **Information Retrieval**: TF-IDF algorithm, inverted indices
- **Text Processing**: Tokenization, stemming, stop word removal
- **Search Algorithms**: Cosine similarity, ranking algorithms
- **System Design**: Modular architecture, data flow optimization
- **Testing**: Comprehensive test coverage, edge case handling

By implementing a complete search engine from scratch, I gained deep insights into how modern search engines work and the challenges of web-scale information retrieval.

## 📊 Performance

- **Crawling Speed**: ~100 pages/minute (with delays)
- **Indexing Speed**: ~500 documents/minute
- **Search Response**: <100ms for typical queries
- **Memory Usage**: Efficient streaming for large datasets

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines and ensure all tests pass before submitting pull requests.

## 📄 License

Distributed under the MIT License. See [LICENSE](./LICENSE) for details.

## 👨‍💻 Author

**TechScope Author** – [GitHub](https://github.com/xxxxxxxx15339)

---

<div align="center">

**Built with ❤️ for learning search engine technology**

</div>



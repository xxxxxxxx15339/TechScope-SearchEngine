
---

## 📁 Project Structure

```
search-engine/
├── crawler/           # Crawling logic (requests, URL parsing, queue)
│   └── crawler.py
├── index/             # Indexing logic (tokenization, TF-IDF)
│   └── indexer.py
├── query/             # Query interface (TF-IDF scoring)
│   └── search.py
├── data/              # Store crawled raw HTML or parsed text
│   └── pages/
├── utils/             # Common utilities (normalization, stopwords)
│   └── helpers.py
├── main.py            # Entry point
└── requirements.txt   # dependencies
```

---

## ✅ Day 1: Build the Web Crawler

**Goal**: Crawl starting from your seed URLs, store HTML and extract links.

### Tasks

1. **crawler.py** (in `crawler/`)

   * Define a `Crawler` class:

     * `seed_urls: List[str]`
     * `visited: Set[str]`
     * `max_pages: int`
   * Use `requests` to fetch HTML.
   * Use `BeautifulSoup` to:

     * Parse page text (store to `data/pages`)
     * Extract all `<a href>` links.
   * Filter:

     * Ignore external domains (optional)
     * Skip duplicates, anchors, and JS links.

2. **Saving data**

   * For each visited page:

     * Save HTML to `data/pages/<hash>.html` (or plain text)
     * Optionally save metadata (e.g., original URL).

3. **Queue system**

   * Implement a basic BFS-style URL queue using a list or `deque`.

---

## ✅ Day 2: Indexing Module (TF-IDF)

**Goal**: Convert crawled pages into searchable documents.

### Tasks

1. **indexer.py** (in `index/`)

   * Load raw text.
   * Preprocess: lowercasing, remove punctuation, tokenize.
   * Remove stopwords (use `nltk.corpus.stopwords`).
   * Compute:

     * TF (term frequency)
     * DF (document frequency)
     * TF-IDF: `TF * log(N/DF)`

2. **Build Inverted Index**

   * For each token:

     * Save list of documents where it appears.
     * Include TF-IDF scores.

---

## ✅ Day 3: Query & Ranking Engine

**Goal**: Accept user query → tokenize → compute cosine similarity → return top N results.

### Tasks

1. **search.py** (in `query/`)

   * Accept input query
   * Tokenize, clean, and compute query vector (TF-IDF)
   * Compare with indexed documents (cosine similarity)
   * Sort and return top matches with titles/snippets

---

## 🔄 main.py

Tie it all together:

* `main.py crawl` → start crawling
* `main.py index` → build index from data/
* `main.py query "how to build a class in Python"` → get ranked results

---

## ✅ Bonus: Later Extensions

* Multithreaded crawling
* Respect 'robots.txt'
* URL frontier prioritization (e.g., favor tutorial pages)
* Frontend (React or simple Flask UI)
* Query expansion / stemming
* Caching

Would you like me to begin by writing `crawler.py`?

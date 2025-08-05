import math

class TFIDFCalculator:
    def __init__(self):
        pass  # Optional, but kept since you defined it

    def calculate_term_frequency(self, tokens):
        token_count = {}
        for token in tokens:
            if token in token_count:
                token_count[token] += 1
            else:
                token_count[token] = 1

        total_tokens = len(tokens)
        for token in token_count:
            token_count[token] = token_count[token] / total_tokens

        return token_count

    def calculate_document_count(self, all_tokens):
        doc_count = {}
        for doc in all_tokens:
            unique_words = set(doc)
            for word in unique_words:
                if word in doc_count:
                    doc_count[word] += 1
                else:
                    doc_count[word] = 1
        return doc_count

    def calculate_tfidf_scores(self, term_frequencies, document_counts, total_documents):
        tfidf_scores = {}
        for word, tf in term_frequencies.items():
            df = document_counts.get(word, 0)

            if df > 0:
                idf = math.log(total_documents / df)
            else:
                idf = 0

            tfidf_scores[word] = tf * idf

        tfidf_scores = self.normalize_score(tfidf_scores)

        return tfidf_scores

    def normalize_score(self, tfidf_scores):
        magnitude = math.sqrt(sum(score ** 2 for score in tfidf_scores.values()))

        normalized_scores = {}
        for word, score in tfidf_scores.items():
            if magnitude > 0:
                normalized_scores[word] = score / magnitude
            else:
                normalized_scores[word] = 0

        return normalized_scores

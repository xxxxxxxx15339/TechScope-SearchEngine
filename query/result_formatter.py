from typing import List, Dict

class ResultFormatter:
    def __init__(self, document_metadata):
        self.document_metadata = document_metadata
    
    def format_results(self, search_results: Dict[str, float], max_results: int) -> List[Dict]:

        sorted_items = sorted(search_results.items(), key=lambda x: x[1], reverse=True)  # list of tuples
        sorted_results = dict(sorted_items[:max_results])  # limit, then convert back to dict

        formatted_results = self.add_metadata(sorted_results)

        return formatted_results

    def add_metadata(self, results: Dict[str, float]) -> List[Dict]:
        formatted_results = []
        for key, value in results.items():
            result_metadata = {'doc_id': key, 'score': value}
            for doc_id, metadata in self.document_metadata.items():
                if doc_id == key:
                    for meta_key, meta_value in metadata.items():
                        if meta_key != 'score' and meta_key != 'doc_id':
                            result_metadata[meta_key] = meta_value
            formatted_results.append(result_metadata)

        return formatted_results







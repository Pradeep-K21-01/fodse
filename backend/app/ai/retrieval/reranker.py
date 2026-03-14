def rerank(query: str, qdrant_hits: list, elastic_hits: list, top_n: int = 5) -> list:
    scores = {}
    def add_results(results, label):
        for rank, item in enumerate(results, start=1):
            key = item['text'][:100]
            if key not in scores:
                scores[key] = {**item, 'rrf_score': 0.0}
            scores[key]['rrf_score'] += 1.0 / (60 + rank)
    add_results(qdrant_hits, 'qdrant')
    add_results(elastic_hits, 'elasticsearch')
    ranked = sorted(scores.values(), key=lambda x: x['rrf_score'], reverse=True)
    return ranked[:top_n]

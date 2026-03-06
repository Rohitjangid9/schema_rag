from app_runtime import AppRuntime


class RetrievalService:
    """Shared retrieval flow for search, SQL generation, and chat."""

    def __init__(self, runtime: AppRuntime):
        self.runtime = runtime

    def search_and_expand(
        self,
        query: str,
        *,
        search_limit: int = 15,
        rerank_top_k: int = 5,
        depth: int = 1,
    ) -> dict:
        search_results = self.runtime.qdrant_manager.search(query, limit=search_limit)

        if self.runtime.reranker and search_results:
            reranked_results = self.runtime.reranker.rerank(query, search_results, top_k=rerank_top_k)
        else:
            reranked_results = search_results[:rerank_top_k]

        expansion = self.runtime.graph_logic.expand_search_results(reranked_results, depth=depth)
        return {
            "search_results": search_results,
            "reranked_results": reranked_results,
            "expansion": expansion,
        }
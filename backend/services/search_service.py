from app_runtime import AppRuntime
from schemas.api import QueryRequest, SearchResponse, SearchResult
from services.retrieval_service import RetrievalService


class SearchService:
    """Service-layer orchestration for the /search endpoint."""

    def __init__(self, runtime: AppRuntime):
        self.runtime = runtime
        self.retrieval_service = RetrievalService(runtime)

    def run(self, request: QueryRequest) -> SearchResponse:
        if not self.runtime.has_search():
            return SearchResponse(
                query=request.query,
                primary_tables=[],
                related_tables=[],
                all_tables=[],
                total_tables=0,
                search_results=[],
                error=self.runtime.initialization_error or "Managers not initialized",
            )

        try:
            retrieval = self.retrieval_service.search_and_expand(request.query)
            reranked_results = retrieval["reranked_results"]
            expansion = retrieval["expansion"]

            formatted_results = [
                SearchResult(
                    table_name=result["table_name"],
                    module=result["module"],
                    summary=result["summary"],
                    score=result.get("rerank_score", result["score"]),
                    columns=result["columns"],
                )
                for result in reranked_results
            ]

            return SearchResponse(
                query=request.query,
                primary_tables=expansion["primary_tables"],
                related_tables=expansion["related_tables"],
                all_tables=expansion["all_tables"],
                total_tables=expansion["total_tables"],
                search_results=formatted_results,
            )
        except Exception as exc:
            return SearchResponse(
                query=request.query,
                primary_tables=[],
                related_tables=[],
                all_tables=[],
                total_tables=0,
                search_results=[],
                error=str(exc),
            )
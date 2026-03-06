from app_runtime import AppRuntime
from schemas.api import Phase2Response, QueryRequest
from services.retrieval_service import RetrievalService


class SQLGenerationService:
    """Service-layer orchestration for the /generate-sql endpoint."""

    def __init__(self, runtime: AppRuntime):
        self.runtime = runtime
        self.retrieval_service = RetrievalService(runtime)

    def run(self, request: QueryRequest) -> Phase2Response:
        if not self.runtime.has_phase2():
            return Phase2Response(
                query=request.query,
                tables_used=[],
                sql_query="",
                status="error",
                error=self.runtime.initialization_error or "Managers not initialized",
            )

        try:
            retrieval = self.retrieval_service.search_and_expand(request.query)
            expansion = retrieval["expansion"]
            expanded_tables = expansion.get("all_tables", [])
            valid_tables, _ = self.runtime.prompt_builder.validate_tables(expanded_tables)
            tables_to_use = valid_tables or expansion.get("primary_tables", [])

            prompt = self.runtime.prompt_builder.build_prompt(request.query, tables_to_use)
            raw_sql = self.runtime.sql_generator.generate_sql(prompt)
            sql_query = self.runtime.sql_generator.clean_sql(raw_sql, request.query)
            is_valid, error = self.runtime.sql_generator.validate_sql(sql_query)

            if not is_valid:
                return Phase2Response(
                    query=request.query,
                    tables_used=tables_to_use,
                    sql_query=sql_query,
                    status="validation_failed",
                    error=error,
                )

            return Phase2Response(
                query=request.query,
                tables_used=tables_to_use,
                sql_query=sql_query,
                status="success",
            )
        except Exception as exc:
            return Phase2Response(
                query=request.query,
                tables_used=[],
                sql_query="",
                status="error",
                error=str(exc),
            )
"""LangGraph-based chat workflow for Phase 3 orchestration."""
from typing import Optional, TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, END

from app_runtime import AppRuntime
from core.chat_debug_logger import ChatDebugLogger
from schemas.api import Phase3Response, QueryRequest
from services.context_pruning_service import ContextPruningService
from services.query_history_service import QueryHistoryService
from services.retrieval_service import RetrievalService


class ChatState(TypedDict):
    """State schema for the /chat LangGraph workflow."""
    query: str
    context: Optional[str]
    search_results: List[Dict[str, Any]]
    reranked_results: List[Dict[str, Any]]
    expansion: Dict[str, Any]
    golden_examples: List[Dict[str, Any]]
    pruning_result: Dict[str, Any]
    tables_to_use: List[str]
    invalid_tables: List[str]
    prompt: str
    raw_sql: str
    sql_query: str
    sql_valid: bool
    sql_error: Optional[str]
    validation_repair_attempts: int
    execution_repair_attempts: int
    retry_execution: bool
    exec_result: Dict[str, Any]
    answer: str
    status: str
    error: Optional[str]
    debug_logger: ChatDebugLogger


class ChatGraphBuilder:
    """Builds the LangGraph for /chat orchestration."""

    def __init__(
        self,
        runtime: AppRuntime,
        debug_base_dir: Optional[str] = None,
        query_history_service: Optional[QueryHistoryService] = None,
        context_pruning_service: Optional[ContextPruningService] = None,
    ):
        self.runtime = runtime
        self.debug_base_dir = debug_base_dir
        self.retrieval_service = RetrievalService(runtime)
        self.query_history_service = query_history_service or QueryHistoryService()
        self.context_pruning_service = context_pruning_service or ContextPruningService()

    def _node_retrieval(self, state: ChatState) -> ChatState:
        """Node: Retrieve and rerank tables."""
        retrieval = self.retrieval_service.search_and_expand(state["query"])
        search_results = retrieval["search_results"]
        reranked_results = retrieval["reranked_results"]
        expansion = retrieval["expansion"]

        state["debug_logger"].add_qdrant_search(search_results, limit=15)
        state["debug_logger"].add_rerank(
            reranked_results=reranked_results,
            original_count=len(search_results),
            used_fallback=getattr(self.runtime.reranker, "last_rerank_used_fallback", not bool(self.runtime.reranker)),
            error=getattr(self.runtime.reranker, "last_error", None) if self.runtime.reranker else "Reranker unavailable",
            model=getattr(self.runtime.reranker, "model", None) if self.runtime.reranker else None,
            base_url=getattr(self.runtime.reranker, "base_url", None) if self.runtime.reranker else None,
        )

        state["search_results"] = search_results
        state["reranked_results"] = reranked_results
        state["expansion"] = expansion
        return state

    def _node_golden_query_lookup(self, state: ChatState) -> ChatState:
        examples = self.query_history_service.get_golden_examples(state["query"])
        state["golden_examples"] = examples
        state["debug_logger"].add_golden_examples(examples)
        return state

    def _node_graph_expansion(self, state: ChatState) -> ChatState:
        """Node: Expand with graph logic and validate tables."""
        expansion = state["expansion"]
        expanded_tables = expansion.get("all_tables", [])
        valid_tables, invalid_tables = self.runtime.prompt_builder.validate_tables(expanded_tables)
        tables_to_use = valid_tables or expansion.get("primary_tables", [])

        state["debug_logger"].add_graph_expansion(expansion)
        state["tables_to_use"] = tables_to_use
        state["invalid_tables"] = invalid_tables
        return state

    def _node_pruning(self, state: ChatState) -> ChatState:
        pruning_result = self.context_pruning_service.prune(
            query=state["query"],
            tables=state["tables_to_use"],
            search_results=state["search_results"],
            reranked_results=state["reranked_results"],
            expansion=state["expansion"],
        )
        state["pruning_result"] = pruning_result
        state["tables_to_use"] = pruning_result["selected_tables"]
        state["debug_logger"].add_pruning(
            original_tables=state["expansion"].get("all_tables", []),
            selected_tables=pruning_result["selected_tables"],
            dropped_tables=pruning_result["dropped_tables"],
            reasoning=pruning_result["reasoning"],
            max_tables=pruning_result["max_tables"],
        )
        return state

    def _node_prompt_building(self, state: ChatState) -> ChatState:
        """Node: Build SQL generation prompt."""
        prompt = self.runtime.prompt_builder.build_prompt(
            state["query"],
            state["tables_to_use"],
            golden_examples_text=self.query_history_service.format_examples_for_prompt(state["golden_examples"]),
            table_selection_notes=self.context_pruning_service.build_selection_notes(state["pruning_result"]),
        )
        state["debug_logger"].add_prompt(
            prompt,
            state["tables_to_use"],
            prompt_source="phase3_pruned_tables_with_golden_examples",
            excluded_tables=state["invalid_tables"],
        )
        state["prompt"] = prompt
        return state

    def _node_sql_generation(self, state: ChatState) -> ChatState:
        """Node: Generate SQL from prompt."""
        raw_sql = self.runtime.sql_generator.generate_sql(state["prompt"])
        sql_query = self.runtime.sql_generator.clean_sql(raw_sql, state["query"])
        is_valid, error = self.runtime.sql_generator.validate_sql(sql_query)

        state["raw_sql"] = raw_sql
        state["sql_query"] = sql_query
        state["sql_valid"] = is_valid
        state["sql_error"] = error
        state["debug_logger"].add_sql_generation(raw_sql, sql_query)
        state["debug_logger"].add_sql_validation(is_valid, error)
        return state

    def _node_sql_repair(self, state: ChatState) -> ChatState:
        """Node: Attempt to repair invalid SQL (self-healing)."""
        if state["sql_valid"] or state["validation_repair_attempts"] >= 2:
            return state

        state["validation_repair_attempts"] += 1
        repair_prompt = f"""The following SQL query has an error:

SQL: {state['sql_query']}
Error: {state['sql_error']}

Please fix the SQL query. Return ONLY the corrected SQL, no explanations.

Available tables and schemas:
{state['prompt']}

CORRECTED SQL:"""

        try:
            repaired_sql = self.runtime.sql_generator.generate_sql(repair_prompt)
            repaired_sql = self.runtime.sql_generator.clean_sql(repaired_sql, state["query"])
            is_valid, error = self.runtime.sql_generator.validate_sql(repaired_sql)
            state["debug_logger"].add_repair_attempt(
                "validation",
                state["validation_repair_attempts"],
                state["sql_error"],
                repaired_sql,
            )

            if is_valid:
                state["sql_query"] = repaired_sql
                state["sql_valid"] = True
                state["sql_error"] = None
        except Exception as e:
            state["debug_logger"].add_error("sql_repair_exception", str(e))

        return state

    def _node_execution_repair(self, state: ChatState) -> ChatState:
        """Node: Attempt to repair SQL based on execution failure."""
        state["retry_execution"] = False
        exec_error = state.get("exec_result", {}).get("error")
        if state.get("exec_result", {}).get("success") or state["execution_repair_attempts"] >= 2:
            return state

        state["execution_repair_attempts"] += 1
        repair_prompt = f"""The following SQL query failed during execution.

User question: {state['query']}
SQL: {state['sql_query']}
Execution error: {exec_error}

Please fix the SQL query using only the provided schemas and return ONLY the corrected SQL.

Available tables and schemas:
{state['prompt']}

CORRECTED SQL:"""

        try:
            repaired_sql = self.runtime.sql_generator.generate_sql(repair_prompt)
            repaired_sql = self.runtime.sql_generator.clean_sql(repaired_sql, state["query"])
            is_valid, error = self.runtime.sql_generator.validate_sql(repaired_sql)
            state["debug_logger"].add_repair_attempt(
                "execution",
                state["execution_repair_attempts"],
                exec_error,
                repaired_sql,
            )
            if is_valid:
                state["sql_query"] = repaired_sql
                state["sql_valid"] = True
                state["sql_error"] = None
                state["retry_execution"] = True
            else:
                state["sql_valid"] = False
                state["sql_error"] = error
        except Exception as exc:
            state["debug_logger"].add_error("execution_repair_exception", str(exc))

        return state

    def _node_execution(self, state: ChatState) -> ChatState:
        """Node: Execute SQL query."""
        if not state["sql_valid"]:
            state["exec_result"] = {
                "success": False,
                "error": state["sql_error"] or "SQL validation failed",
                "rows": [],
                "columns": [],
            }
            return state

        exec_result = self.runtime.query_executor.execute_query(state["sql_query"])
        state["retry_execution"] = False
        state["debug_logger"].add_execution(exec_result)
        state["exec_result"] = exec_result
        return state

    def _node_formatting(self, state: ChatState) -> ChatState:
        """Node: Format results into natural language answer."""
        if not state["exec_result"]["success"]:
            state["answer"] = ""
            state["status"] = "execution_failed"
            state["error"] = state["exec_result"]["error"]
            return state

        rows = state["exec_result"]["rows"]
        columns = state["exec_result"]["columns"]
        answer = self.runtime.result_formatter.format_results(state["query"], rows, columns)

        state["debug_logger"].add_answer(
            answer,
            used_fallback=getattr(self.runtime.result_formatter, "last_used_fallback", False),
            error=getattr(self.runtime.result_formatter, "last_error", None),
            model=getattr(self.runtime.result_formatter, "model", None),
        )
        state["answer"] = answer
        state["status"] = "success"
        return state

    def build(self) -> StateGraph:
        """Build and return the LangGraph."""
        graph = StateGraph(ChatState)

        # Add nodes
        graph.add_node("retrieval", self._node_retrieval)
        graph.add_node("golden_query_lookup", self._node_golden_query_lookup)
        graph.add_node("graph_expansion", self._node_graph_expansion)
        graph.add_node("pruning", self._node_pruning)
        graph.add_node("prompt_building", self._node_prompt_building)
        graph.add_node("sql_generation", self._node_sql_generation)
        graph.add_node("sql_repair", self._node_sql_repair)
        graph.add_node("execution", self._node_execution)
        graph.add_node("execution_repair", self._node_execution_repair)
        graph.add_node("formatting", self._node_formatting)

        # Add edges
        graph.add_edge("retrieval", "golden_query_lookup")
        graph.add_edge("golden_query_lookup", "graph_expansion")
        graph.add_edge("graph_expansion", "pruning")
        graph.add_edge("pruning", "prompt_building")
        graph.add_edge("prompt_building", "sql_generation")
        graph.add_conditional_edges(
            "sql_generation",
            lambda state: "execution" if state["sql_valid"] else "sql_repair",
            {"execution": "execution", "sql_repair": "sql_repair"},
        )
        graph.add_edge("sql_repair", "execution")
        graph.add_conditional_edges(
            "execution",
            lambda state: "formatting"
            if state["exec_result"].get("success") or state["execution_repair_attempts"] >= 2 or not state["sql_valid"]
            else "execution_repair",
            {"formatting": "formatting", "execution_repair": "execution_repair"},
        )
        graph.add_conditional_edges(
            "execution_repair",
            lambda state: "execution" if state["retry_execution"] else "formatting",
            {"execution": "execution", "formatting": "formatting"},
        )
        graph.add_edge("formatting", END)

        # Set entry point
        graph.set_entry_point("retrieval")

        return graph.compile()


class ChatWorkflow:
    """LangGraph-based /chat workflow orchestrator."""

    def __init__(
        self,
        runtime: AppRuntime,
        debug_base_dir: Optional[str] = None,
        query_history_service: Optional[QueryHistoryService] = None,
        context_pruning_service: Optional[ContextPruningService] = None,
    ):
        self.runtime = runtime
        self.debug_base_dir = debug_base_dir
        self.query_history_service = query_history_service or QueryHistoryService()
        self.graph_builder = ChatGraphBuilder(
            runtime,
            debug_base_dir,
            query_history_service=self.query_history_service,
            context_pruning_service=context_pruning_service,
        )
        self.graph = self.graph_builder.build()

    def run(self, request: QueryRequest) -> Phase3Response:
        """Execute the /chat workflow using LangGraph."""
        debug_logger = ChatDebugLogger(request.query, request.context, base_dir=self.debug_base_dir)

        if not self.runtime.has_chat():
            debug_logger.add_request(request.context)
            debug_logger.add_error("initialization", self.runtime.initialization_error or "Managers not initialized")
            debug_logger.write("error")
            return Phase3Response(
                query=request.query,
                tables_used=[],
                sql_query="",
                rows_returned=0,
                answer="",
                status="error",
                error=self.runtime.initialization_error or "Managers not initialized",
            )

        try:
            debug_logger.add_request(request.context)

            # Initialize state
            initial_state: ChatState = {
                "query": request.query,
                "context": request.context,
                "search_results": [],
                "reranked_results": [],
                "expansion": {},
                "golden_examples": [],
                "pruning_result": {},
                "tables_to_use": [],
                "invalid_tables": [],
                "prompt": "",
                "raw_sql": "",
                "sql_query": "",
                "sql_valid": False,
                "sql_error": None,
                "validation_repair_attempts": 0,
                "execution_repair_attempts": 0,
                "retry_execution": False,
                "exec_result": {},
                "answer": "",
                "status": "pending",
                "error": None,
                "debug_logger": debug_logger,
            }

            # Execute graph
            final_state = self.graph.invoke(initial_state)

            # Write debug log
            debug_logger.write(final_state["status"])

            rows_returned = len(final_state["exec_result"].get("rows", [])) if final_state["exec_result"].get("success") else 0
            self.query_history_service.record_chat_interaction(
                query=final_state["query"],
                context=final_state["context"],
                sql_query=final_state["sql_query"],
                tables_used=final_state["tables_to_use"],
                answer=final_state["answer"],
                rows_returned=rows_returned,
                status=final_state["status"],
                error=final_state["error"],
            )

            # Return response
            return Phase3Response(
                query=final_state["query"],
                tables_used=final_state["tables_to_use"],
                sql_query=final_state["sql_query"],
                rows_returned=rows_returned,
                answer=final_state["answer"],
                status=final_state["status"],
                error=final_state["error"],
            )

        except Exception as exc:
            debug_logger.add_error("workflow_exception", str(exc))
            debug_logger.write("error")
            return Phase3Response(
                query=request.query,
                tables_used=[],
                sql_query="",
                rows_returned=0,
                answer="",
                status="error",
                error=str(exc),
            )
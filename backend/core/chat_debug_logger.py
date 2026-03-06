from pathlib import Path
from datetime import datetime
import json
import re
import uuid
from typing import Any, Dict, List, Optional


class ChatDebugLogger:
    """Writes per-request markdown debug logs for the /chat pipeline."""

    def __init__(self, query: str, context: Optional[str] = None, base_dir: Optional[str] = None):
        backend_dir = Path(__file__).resolve().parent.parent
        self.base_dir = Path(base_dir) if base_dir else backend_dir / "debug_logs"
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.created_at = datetime.now()
        self.request_id = uuid.uuid4().hex[:8]
        self.query = query
        self.context = context
        self.sections: List[str] = []

        slug = self._slugify(query)
        timestamp = self.created_at.strftime("%Y%m%d_%H%M%S")
        self.file_path = self.base_dir / f"chat_{timestamp}_{slug}_{self.request_id}.md"
        self.latest_path = self.base_dir / "latest_chat_debug.md"

    def add_request(self, context: Optional[str] = None):
        lines = [f"- Query: `{self.query}`"]
        if context:
            lines.extend(["", "### Context", "", "```text", context, "```"])
        self._add_section("Request", "\n".join(lines))

    def add_qdrant_search(self, search_results: List[Dict[str, Any]], limit: int):
        body = "\n".join([
            f"- Requested top `{limit}` candidate tables from Qdrant.",
            f"- Returned `{len(search_results)}` candidate tables.",
            "",
            self._format_search_table(search_results, include_rerank=False),
        ])
        self._add_section("Qdrant Semantic Search", body)

    def add_rerank(
        self,
        reranked_results: List[Dict[str, Any]],
        original_count: int,
        used_fallback: bool,
        error: Optional[str],
        model: Optional[str],
        base_url: Optional[str],
    ):
        lines = [
            f"- Input candidates: `{original_count}`",
            f"- Output candidates: `{len(reranked_results)}`",
            f"- Fallback used: `{used_fallback}`",
            f"- Model: `{model or 'unknown'}`",
            f"- Endpoint: `{base_url or 'unknown'}`",
        ]
        if error:
            lines.append(f"- Error: `{error}`")
        lines.extend(["", self._format_search_table(reranked_results, include_rerank=True)])
        self._add_section("Rerank", "\n".join(lines))

    def add_graph_expansion(self, expansion: Dict[str, Any]):
        body = "\n".join([
            f"- Primary tables: `{', '.join(expansion.get('primary_tables', [])) or 'None'}`",
            f"- Related tables: `{', '.join(expansion.get('related_tables', [])) or 'None'}`",
            f"- All tables: `{', '.join(expansion.get('all_tables', [])) or 'None'}`",
            f"- Total tables: `{expansion.get('total_tables', 0)}`",
        ])
        self._add_section("Graph Expansion", body)

    def add_golden_examples(self, examples: List[Dict[str, Any]]):
        if not examples:
            self._add_section("Golden Query Retrieval", "- Retrieved examples: `0`")
            return

        lines = [f"- Retrieved examples: `{len(examples)}`", ""]
        for idx, example in enumerate(examples, 1):
            tables = ", ".join(example.get("tables_used") or []) or "None"
            lines.extend([
                f"### Example {idx}",
                f"- Similarity score: `{example.get('score', 'N/A')}`",
                f"- Query: `{example.get('query', '')}`",
                f"- Tables: `{tables}`",
                "```sql",
                example.get("sql_query", ""),
                "```",
                "",
            ])
        self._add_section("Golden Query Retrieval", "\n".join(lines))

    def add_pruning(
        self,
        original_tables: List[str],
        selected_tables: List[str],
        dropped_tables: List[str],
        reasoning: Dict[str, str],
        max_tables: int,
    ):
        lines = [
            f"- Max tables allowed: `{max_tables}`",
            f"- Original tables ({len(original_tables)}): `{', '.join(original_tables) or 'None'}`",
            f"- Selected tables ({len(selected_tables)}): `{', '.join(selected_tables) or 'None'}`",
            f"- Dropped tables ({len(dropped_tables)}): `{', '.join(dropped_tables) or 'None'}`",
            "",
        ]
        for table in selected_tables:
            lines.append(f"- `{table}` → {reasoning.get(table, 'kept')}")
        self._add_section("Deterministic Context Pruning", "\n".join(lines))

    def add_prompt(
        self,
        prompt: str,
        tables_to_use: List[str],
        prompt_source: str = "unknown",
        excluded_tables: Optional[List[str]] = None,
    ):
        body = "\n".join([
            f"- Prompt source: `{prompt_source}`",
            f"- Tables used for prompt ({len(tables_to_use)}): `{', '.join(tables_to_use) or 'None'}`",
            f"- Excluded tables without schema: `{', '.join(excluded_tables or []) or 'None'}`",
            f"- Prompt length: `{len(prompt)}` characters",
            "",
            "```text",
            prompt,
            "```",
        ])
        self._add_section("Prompt", body)

    def add_sql_generation(self, raw_sql: str, cleaned_sql: str):
        body = "\n".join([
            "### Raw SQL",
            "",
            "```sql",
            raw_sql or "",
            "```",
            "",
            "### Cleaned SQL",
            "",
            "```sql",
            cleaned_sql or "",
            "```",
        ])
        self._add_section("SQL Generation", body)

    def add_sql_validation(self, is_valid: bool, error: Optional[str]):
        lines = [f"- Valid: `{is_valid}`"]
        if error:
            lines.append(f"- Validation error: `{error}`")
        self._add_section("SQL Validation", "\n".join(lines))

    def add_repair_attempt(self, stage: str, attempt: int, error: Optional[str], repaired_sql: str):
        body = "\n".join([
            f"- Stage: `{stage}`",
            f"- Attempt: `{attempt}`",
            f"- Trigger error: `{error or 'None'}`",
            "",
            "```sql",
            repaired_sql or "",
            "```",
        ])
        self._add_section("SQL Repair Attempt", body)

    def add_execution(self, execution_result: Dict[str, Any]):
        rows = execution_result.get("rows", [])
        body = "\n".join([
            f"- Success: `{execution_result.get('success', False)}`",
            f"- Row count: `{execution_result.get('row_count', 0)}`",
            f"- Columns: `{', '.join(execution_result.get('columns', [])) or 'None'}`",
            f"- Error: `{execution_result.get('error') or 'None'}`",
            "",
            "### Executed SQL",
            "",
            "```sql",
            execution_result.get("executed_sql", "") or "",
            "```",
            "",
            "### Row Preview",
            "",
            "```json",
            json.dumps(rows[:5], indent=2, ensure_ascii=False),
            "```",
            "",
            "### Full Returned Rows",
            "",
            "```json",
            json.dumps(rows, indent=2, ensure_ascii=False),
            "```",
        ])
        self._add_section("Query Execution", body)

    def add_answer(self, answer: str, used_fallback: bool = False, error: Optional[str] = None, model: Optional[str] = None):
        lines = [
            f"- Formatter model: `{model or 'unknown'}`",
            f"- Fallback used: `{used_fallback}`",
        ]
        if error:
            lines.append(f"- Formatter error: `{error}`")
        lines.extend(["", "```text", answer or "", "```"])
        body = "\n".join(lines)
        self._add_section("Final Answer", body)

    def add_error(self, stage: str, error: str):
        body = "\n".join([
            f"- Stage: `{stage}`",
            f"- Error: `{error}`",
        ])
        self._add_section("Error", body)

    def write(self, final_status: str) -> Path:
        content = self._render(final_status)
        self.file_path.write_text(content, encoding="utf-8")
        self.latest_path.write_text(content, encoding="utf-8")
        return self.file_path

    def _render(self, final_status: str) -> str:
        header = [
            "# /chat Debug Log",
            "",
            f"- Request ID: `{self.request_id}`",
            f"- Created At: `{self.created_at.isoformat(timespec='seconds')}`",
            f"- Log File: `{self.file_path.name}`",
            "",
        ]
        footer = ["## Final Status", "", f"`{final_status}`", ""]
        return "\n".join(header + self.sections + footer)

    def _add_section(self, title: str, body: str):
        self.sections.append(f"## {title}\n\n{body}\n")

    def _format_search_table(self, results: List[Dict[str, Any]], include_rerank: bool) -> str:
        if not results:
            return "No results found."

        headers = ["#", "table", "module", "score"]
        if include_rerank:
            headers.append("rerank_score")
        headers.extend(["rows", "columns", "summary"])

        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]

        for idx, result in enumerate(results, 1):
            row = [
                str(idx),
                self._escape_cell(result.get("table_name", "")),
                self._escape_cell(result.get("module", "")),
                self._format_score(result.get("score")),
            ]
            if include_rerank:
                row.append(self._format_score(result.get("rerank_score")))
            row.extend([
                str(result.get("row_count", 0)),
                self._escape_cell(", ".join(result.get("columns", [])[:8])),
                self._escape_cell(self._truncate(result.get("summary", ""), 140)),
            ])
            lines.append("| " + " | ".join(row) + " |")

        return "\n".join(lines)

    def _format_score(self, value: Any) -> str:
        if isinstance(value, (int, float)):
            return f"{value:.4f}"
        return "N/A"

    def _truncate(self, value: str, max_chars: int) -> str:
        value = str(value or "")
        return value if len(value) <= max_chars else value[: max_chars - 3] + "..."

    def _escape_cell(self, value: str) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    def _slugify(self, value: str) -> str:
        cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
        return cleaned[:50] or "query"
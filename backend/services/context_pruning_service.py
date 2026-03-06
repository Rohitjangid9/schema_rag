import re
from typing import Any, Dict, List


class ContextPruningService:
    """Deterministically prune expanded tables before prompt construction."""

    def __init__(self, max_tables: int = 8):
        self.max_tables = max_tables

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9_]+", (text or "").lower()))

    def prune(
        self,
        *,
        query: str,
        tables: List[str],
        search_results: List[Dict[str, Any]],
        reranked_results: List[Dict[str, Any]],
        expansion: Dict[str, Any],
    ) -> Dict[str, Any]:
        if len(tables) <= self.max_tables:
            reasoning = {table: "kept because table count is already within limit" for table in tables}
            return {
                "selected_tables": list(tables),
                "dropped_tables": [],
                "reasoning": reasoning,
                "max_tables": self.max_tables,
            }

        query_tokens = self._tokenize(query)
        search_by_table = {item.get("table_name"): item for item in search_results}
        rerank_index = {item.get("table_name"): idx for idx, item in enumerate(reranked_results)}
        primary_tables = set(expansion.get("primary_tables", []))
        related_tables = set(expansion.get("related_tables", []))

        scored = []
        for table in tables:
            reasons = []
            score = 0

            if table in primary_tables:
                score += 100
                reasons.append("primary table")
            elif table in related_tables:
                score += 35
                reasons.append("graph-related table")

            if table in rerank_index:
                rerank_bonus = max(0, 50 - (rerank_index[table] * 5))
                score += rerank_bonus
                reasons.append(f"reranked candidate (+{rerank_bonus})")

            metadata = search_by_table.get(table, {})
            lexical_text = " ".join([
                table,
                metadata.get("summary", ""),
                " ".join(metadata.get("columns", []) or []),
            ])
            lexical_overlap = len(query_tokens & self._tokenize(lexical_text))
            if lexical_overlap:
                lexical_bonus = lexical_overlap * 7
                score += lexical_bonus
                reasons.append(f"lexical overlap (+{lexical_bonus})")

            scored.append((table, score, ", ".join(reasons) or "fallback keep"))

        scored.sort(key=lambda item: item[1], reverse=True)
        selected_tables = [table for table, _, _ in scored[: self.max_tables]]
        dropped_tables = [table for table, _, _ in scored[self.max_tables :]]
        reasoning = {table: reason for table, _, reason in scored}
        return {
            "selected_tables": selected_tables,
            "dropped_tables": dropped_tables,
            "reasoning": reasoning,
            "max_tables": self.max_tables,
        }

    def build_selection_notes(self, pruning_result: Dict[str, Any]) -> str:
        selected_tables = pruning_result.get("selected_tables", [])
        dropped_tables = pruning_result.get("dropped_tables", [])
        return (
            f"Use these prioritized tables first: {', '.join(selected_tables) or 'None'}. "
            f"Only reference dropped tables if absolutely necessary and infer joins from the provided schemas. "
            f"Dropped from context: {', '.join(dropped_tables) or 'None'}."
        )
import json
import re
from typing import Any, Dict, List, Optional

from database import SessionLocal
from models import Query as QueryModel


class QueryHistoryService:
    """Retrieve and persist chat history for lightweight golden-query reuse."""

    def _tokenize(self, text: Optional[str]) -> set[str]:
        return set(re.findall(r"[a-z0-9_]+", (text or "").lower()))

    def _parse_payload(self, raw_response: Optional[str]) -> Optional[Dict[str, Any]]:
        if not raw_response:
            return None
        try:
            payload = json.loads(raw_response)
        except (TypeError, ValueError):
            return None
        if not isinstance(payload, dict) or not payload.get("sql_query"):
            return None
        return payload

    def get_golden_examples(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        try:
            db = SessionLocal()
            records = (
                db.query(QueryModel)
                .filter(QueryModel.status == "success")
                .order_by(QueryModel.created_at.desc())
                .limit(100)
                .all()
            )
        except Exception:
            return []
        finally:
            try:
                db.close()
            except Exception:
                pass

        query_tokens = self._tokenize(query)
        ranked: List[Dict[str, Any]] = []
        for record in records:
            payload = self._parse_payload(record.response)
            if not payload:
                continue

            table_names = payload.get("tables_used") or []
            candidate_text = " ".join([
                record.query_text or "",
                payload.get("sql_query") or "",
                " ".join(table_names),
            ])
            candidate_tokens = self._tokenize(candidate_text)
            overlap = len(query_tokens & candidate_tokens)
            if overlap <= 0:
                continue

            ranked.append({
                "query": record.query_text,
                "sql_query": payload.get("sql_query", ""),
                "tables_used": table_names,
                "answer": payload.get("answer", ""),
                "score": overlap,
            })

        ranked.sort(key=lambda item: item["score"], reverse=True)
        return ranked[:limit]

    def format_examples_for_prompt(self, examples: List[Dict[str, Any]]) -> str:
        if not examples:
            return "None"

        chunks = []
        for idx, example in enumerate(examples, 1):
            tables = ", ".join(example.get("tables_used") or []) or "None"
            chunks.append(
                f"Example {idx}:\n"
                f"Question: {example.get('query', '')}\n"
                f"Tables: {tables}\n"
                f"SQL: {example.get('sql_query', '')}"
            )
        return "\n\n".join(chunks)

    def record_chat_interaction(
        self,
        *,
        query: str,
        context: Optional[str],
        sql_query: str,
        tables_used: List[str],
        answer: str,
        rows_returned: int,
        status: str,
        error: Optional[str],
    ) -> None:
        payload = {
            "sql_query": sql_query,
            "tables_used": tables_used,
            "answer": answer,
            "rows_returned": rows_returned,
            "error": error,
        }

        try:
            db = SessionLocal()
            db_query = QueryModel(
                query_text=query,
                context=context,
                response=json.dumps(payload),
                status=status,
            )
            db.add(db_query)
            db.commit()
        except Exception:
            try:
                db.rollback()
            except Exception:
                pass
        finally:
            try:
                db.close()
            except Exception:
                pass
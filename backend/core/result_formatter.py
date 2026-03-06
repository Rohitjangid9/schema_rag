"""
Result Formatter: Format raw query results into human-readable answers
Uses NVIDIA Llama 8B to convert data into natural language
"""
import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ResultFormatter:
    """Formats query results into human-readable answers"""

    def __init__(self):
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model = "meta/llama-3.1-8b-instruct"
        self.last_used_fallback = False
        self.last_error = None

    def format_results(self, query: str, rows: List[Dict[str, Any]], columns: List[str]) -> str:
        """Format raw query results into human-readable answer"""
        self.last_used_fallback = False
        self.last_error = None

        if not rows:
            return "No results found for your query."

        data_summary = self._summarize_data(rows, columns)

        prompt = f"""You are a helpful data analyst. Given the following query results, provide a clear and concise answer to the user's question.

USER QUESTION: {query}

QUERY RESULTS:
{data_summary}

Provide a natural language answer that directly answers the question.

ANSWER:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=512
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            self.last_used_fallback = True
            self.last_error = str(e)
            print(f"Error formatting results: {e}")
            return self._fallback_format(rows, columns)

    def _summarize_data(self, rows: List[Dict[str, Any]], columns: List[str]) -> str:
        """Create a readable summary of query results"""
        if not rows:
            return "No data"

        summary_rows = rows[:10]
        lines = []
        for i, row in enumerate(summary_rows, 1):
            row_str = ", ".join([f"{col}: {row.get(col, 'N/A')}" for col in columns])
            lines.append(f"Row {i}: {row_str}")

        if len(rows) > 10:
            lines.append(f"... and {len(rows) - 10} more rows")

        return "\n".join(lines)

    def _fallback_format(self, rows: List[Dict[str, Any]], columns: List[str]) -> str:
        """Fallback formatting if AI formatting fails"""
        if not rows:
            return "No results found."

        lines = []
        lines.append(f"Found {len(rows)} result(s):")
        header = " | ".join(columns)
        lines.append(header)
        lines.append("-" * len(header))

        for row in rows[:10]:
            row_values = [str(row.get(col, "N/A")) for col in columns]
            lines.append(" | ".join(row_values))

        if len(rows) > 10:
            lines.append(f"... and {len(rows) - 10} more rows")

        return "\n".join(lines)

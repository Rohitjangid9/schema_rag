"""Result Formatter: format query results with a YAML-backed prompt."""
import os
from typing import Any, Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

try:
    from prompt_loader import PromptLoader
except ImportError:
    from core.prompt_loader import PromptLoader

load_dotenv()


class ResultFormatter:
    """Formats query results into human-readable answers"""

    def __init__(self, prompt_loader: Optional[PromptLoader] = None, prompt_name: str = "result_formatter"):
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment")

        self.client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        )
        self.model = os.getenv("NVIDIA_FORMATTER_MODEL", "meta/llama-3.1-8b-instruct")
        self.prompt_loader = prompt_loader or PromptLoader()
        self.prompt_name = prompt_name
        self.last_used_fallback = False
        self.last_error = None

    def format_results(self, query: str, rows: List[Dict[str, Any]], columns: List[str]) -> str:
        """Format raw query results into human-readable answer"""
        self.last_used_fallback = False
        self.last_error = None

        if not rows:
            return "No results found for your query."

        data_summary = self._summarize_data(rows, columns)

        prompt = self.prompt_loader.render_prompt(
            self.prompt_name,
            query=query,
            data_summary=data_summary,
        )

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

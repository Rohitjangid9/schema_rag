"""
SQL Generator: Generate SQL queries using NVIDIA Llama 70B
Converts natural language queries to SQL using AI
"""
import os
import re
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class SQLGenerator:
    """Generates SQL queries using NVIDIA Llama 70B"""

    def __init__(self):
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://integrate.api.nvidia.com/v1"
        )
        self.model = "meta/llama-3.1-70b-instruct"

    def generate_sql(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Generate SQL query from prompt

        Args:
            prompt: Formatted prompt with schemas and question
            max_tokens: Maximum tokens in response

        Returns:
            Generated SQL query
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Low temperature for deterministic SQL
                top_p=0.9,
                max_tokens=max_tokens
            )

            sql_query = response.choices[0].message.content.strip()
            return sql_query

        except Exception as e:
            print(f"Error generating SQL: {e}")
            raise

    def generate_sql_stream(self, prompt: str, max_tokens: int = 512):
        """
        Generate SQL query with streaming

        Yields:
            Chunks of SQL query as they're generated
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                top_p=0.9,
                max_tokens=max_tokens,
                stream=True
            )

            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            print(f"Error in streaming: {e}")
            raise

    def validate_sql(self, sql_query: str) -> tuple[bool, Optional[str]]:
        """
        Validate SQL query for safety

        Returns:
            (is_valid, error_message)
        """
        # Check for dangerous operations
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER"]

        sql_upper = sql_query.upper()

        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                # Allow CREATE TABLE in schema definitions, but not in queries
                if keyword == "CREATE" and "CREATE TABLE" in sql_upper:
                    return False, f"CREATE TABLE not allowed in queries"
                elif keyword != "CREATE":
                    return False, f"{keyword} operation not allowed"

        # Check for SELECT statement
        if "SELECT" not in sql_upper:
            return False, "Query must be a SELECT statement"

        return True, None

    def _is_row_count_question(self, user_query: Optional[str]) -> bool:
        """Detect questions that are asking for counts of rows/records."""
        if not user_query:
            return False

        query = user_query.lower()
        count_indicators = [
            "how many",
            "count",
            "number of",
            "total number",
            "total count",
            "show total",
        ]
        disallowed_context = [
            "distinct",
            "unique",
            "non-null",
            "not null",
            "missing",
            "null",
            "sum",
            "average",
            "avg",
        ]

        return any(indicator in query for indicator in count_indicators) and not any(
            marker in query for marker in disallowed_context
        )

    def _normalize_row_count_sql(self, sql_query: str, user_query: Optional[str]) -> str:
        """Prefer COUNT(*) over COUNT(id/_id) for row-count questions."""
        if not self._is_row_count_question(user_query):
            return sql_query

        count_pattern = re.compile(
            r"COUNT\s*\(\s*(?!DISTINCT\b)(?:[A-Za-z_][A-Za-z0-9_]*\.)?([A-Za-z_][A-Za-z0-9_]*)\s*\)",
            re.IGNORECASE,
        )

        def replace_count(match: re.Match[str]) -> str:
            column_name = match.group(1).lower()
            if column_name == "id" or column_name.endswith("_id"):
                return "COUNT(*)"
            return match.group(0)

        return count_pattern.sub(replace_count, sql_query)

    def clean_sql(self, sql_query: str, user_query: Optional[str] = None) -> str:
        """
        Clean up generated SQL query

        - Remove markdown code blocks
        - Remove extra whitespace
        - Remove comments
        """
        # Remove markdown code blocks
        sql_query = sql_query.replace("```sql", "").replace("```", "")

        # Remove SQL comments
        lines = sql_query.split("\n")
        cleaned_lines = []
        for line in lines:
            # Remove -- comments
            if "--" in line:
                line = line[:line.index("--")]
            cleaned_lines.append(line.strip())

        sql_query = " ".join(cleaned_lines)

        # Remove extra whitespace
        sql_query = " ".join(sql_query.split())

        # Prefer COUNT(*) for row-count questions to avoid null-ID undercounting.
        sql_query = self._normalize_row_count_sql(sql_query, user_query)

        return sql_query.strip()


if __name__ == "__main__":
    from prompt_builder import PromptBuilder

    # Test SQL generation
    builder = PromptBuilder()
    generator = SQLGenerator()

    query = "Show me total revenue by city"
    tables = ["sales_order", "crm_customer", "customer_address"]

    print(f"\n✓ Generating SQL for: {query}")
    print(f"✓ Using tables: {tables}")

    prompt = builder.build_prompt(query, tables)

    print(f"\n✓ Calling Llama 70B...")
    sql = generator.generate_sql(prompt)

    print(f"\n✓ Generated SQL:\n{sql}")

    # Validate
    is_valid, error = generator.validate_sql(sql)
    print(f"\n✓ Validation: {'PASSED' if is_valid else 'FAILED'}")
    if error:
        print(f"  Error: {error}")

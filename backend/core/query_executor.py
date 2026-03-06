"""
Query Executor: Execute SQL queries safely against SQLite database
"""
import sqlite3
from typing import List, Dict, Any, Optional
from contextlib import contextmanager


class QueryExecutor:
    """Executes SQL queries safely against SQLite database"""

    def __init__(self, db_path: str = "data/erp_data.db"):
        self.db_path = db_path
        self.max_rows = 1000
        self.timeout = 30

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path, timeout=self.timeout)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def validate_query(self, sql_query: str) -> tuple:
        """Validate SQL query for safety"""
        import re
        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "CREATE", "ALTER"]

        for keyword in dangerous_keywords:
            pattern = re.compile(rf"\b{keyword}\b", re.IGNORECASE)
            if pattern.search(sql_query):
                return False, f"{keyword} operation not allowed"

        if not re.search(r"\bSELECT\b", sql_query, re.IGNORECASE):
            return False, "Query must be a SELECT statement"

        return True, None

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query safely"""
        executed_sql = sql_query
        is_valid, error = self.validate_query(sql_query)
        if not is_valid:
            return {
                "success": False,
                "error": error,
                "rows": [],
                "row_count": 0,
                "columns": [],
                "executed_sql": executed_sql
            }

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                if "LIMIT" not in sql_query.upper():
                    executed_sql = f"{sql_query} LIMIT {self.max_rows}"
                else:
                    executed_sql = sql_query

                cursor.execute(executed_sql)
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description] if cursor.description else []
                result_rows = [dict(row) for row in rows]

                return {
                    "success": True,
                    "rows": result_rows,
                    "row_count": len(result_rows),
                    "columns": columns,
                    "error": None,
                    "executed_sql": executed_sql
                }

        except sqlite3.OperationalError as e:
            return {
                "success": False,
                "error": f"Database error: {str(e)}",
                "rows": [],
                "row_count": 0,
                "columns": [],
                "executed_sql": executed_sql
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "rows": [],
                "row_count": 0,
                "columns": [],
                "executed_sql": executed_sql
            }

    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get column information for a table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                return {
                    "table_name": table_name,
                    "columns": [dict(col) for col in columns],
                    "column_count": len(columns)
                }

        except Exception as e:
            return {
                "table_name": table_name,
                "error": str(e),
                "columns": [],
                "column_count": 0
            }

    def get_row_count(self, table_name: str) -> int:
        """Get row count for a table"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cursor.fetchone()[0]
        except:
            return 0

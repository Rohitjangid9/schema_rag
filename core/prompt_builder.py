"""
Prompt Builder: Extract schemas and build SQL generation prompts
Constructs context-aware prompts for Llama 70B to generate SQL queries
"""
import re
from typing import List, Dict, Any
from pathlib import Path


class PromptBuilder:
    """Builds SQL generation prompts with relevant table schemas"""
    
    def __init__(self, schema_file: str = "data/erp_schema_dump.sql"):
        self.schema_file = schema_file
        self.all_schemas = self._load_all_schemas()
    
    def _load_all_schemas(self) -> Dict[str, str]:
        """Load all CREATE TABLE statements from schema file"""
        schemas = {}
        
        try:
            with open(self.schema_file, 'r') as f:
                content = f.read()
            
            # Extract all CREATE TABLE statements
            pattern = r'CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\);'
            matches = re.finditer(pattern, content, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                table_name = match.group(1)
                table_def = match.group(0)
                schemas[table_name] = table_def
            
            print(f"✓ Loaded {len(schemas)} table schemas")
            return schemas
        
        except Exception as e:
            print(f"Error loading schemas: {e}")
            return {}
    
    def get_table_schema(self, table_name: str) -> str:
        """Get CREATE TABLE statement for a specific table"""
        return self.all_schemas.get(table_name, f"-- Table {table_name} not found")

    def build_prompt(self, user_query: str, table_names: List[str]) -> str:
        """
        Build a prompt for SQL generation

        Args:
            user_query: Natural language query from user
            table_names: List of relevant table names

        Returns:
            Formatted prompt for Llama 70B
        """
        # Get schemas for selected tables
        schemas = []
        for table in table_names:
            schema = self.get_table_schema(table)
            if schema:
                schemas.append(schema)

        schemas_text = "\n\n".join(schemas)

        prompt = f"""You are an expert SQL developer. Given the following database schemas, write a SQL query to answer the user's question.

IMPORTANT RULES:
1. Only use the tables provided below
2. Use proper JOINs to connect related tables
3. Use WHERE clauses for filtering
4. Use GROUP BY and aggregate functions (SUM, COUNT, AVG) when needed
5. Return only the SQL query, no explanations
6. Use SQLite syntax
7. Do NOT use CREATE, DROP, DELETE, UPDATE, or INSERT statements
8. Do NOT use subqueries unless necessary
9. Limit results to 1000 rows

DATABASE SCHEMAS:
{schemas_text}

USER QUESTION: {user_query}

SQL QUERY:"""

        return prompt

    def build_safe_prompt(self, user_query: str, table_names: List[str]) -> str:
        """
        Build a prompt with additional safety constraints
        """
        base_prompt = self.build_prompt(user_query, table_names)

        safety_note = "\n\nSAFETY CHECK: Ensure the query does not contain DROP, DELETE, UPDATE, or CREATE statements."

        return base_prompt + safety_note

    def validate_tables(self, table_names: List[str]) -> tuple[List[str], List[str]]:
        """
        Validate that requested tables exist in schema

        Returns:
            (valid_tables, invalid_tables)
        """
        valid = [t for t in table_names if t in self.all_schemas]
        invalid = [t for t in table_names if t not in self.all_schemas]

        return valid, invalid

    def get_available_tables(self) -> List[str]:
        """Get list of all available tables"""
        return sorted(list(self.all_schemas.keys()))


if __name__ == "__main__":
    builder = PromptBuilder()

    # Test with sample query
    query = "Show me total revenue by city"
    tables = ["sales_order", "crm_customer", "customer_address"]

    print(f"\n✓ Building prompt for: {query}")
    print(f"✓ Using tables: {tables}")

    prompt = builder.build_prompt(query, tables)
    print(f"\n✓ Prompt length: {len(prompt)} characters")
    print(f"\n✓ Prompt preview (first 500 chars):\n{prompt[:500]}...")

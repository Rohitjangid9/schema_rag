"""Prompt Builder: extract schemas and build SQL prompts from YAML templates."""
import re
from pathlib import Path
from typing import Dict, List, Optional

try:
    from prompt_loader import PromptLoader
except ImportError:
    from core.prompt_loader import PromptLoader


class PromptBuilder:
    """Builds SQL generation prompts with relevant table schemas"""
    
    def __init__(
        self,
        schema_file: Optional[str] = None,
        prompt_loader: Optional[PromptLoader] = None,
        prompt_name: str = "sql_generation",
    ):
        backend_dir = Path(__file__).resolve().parent.parent
        self.schema_file = Path(schema_file) if schema_file else backend_dir / "data" / "erp_schema_dump.sql"
        self.prompt_loader = prompt_loader or PromptLoader()
        self.prompt_name = prompt_name
        self.all_schemas = self._load_all_schemas()
    
    def _load_all_schemas(self) -> Dict[str, str]:
        """Load all CREATE TABLE statements from schema file"""
        schemas = {}
        
        try:
            with open(self.schema_file, 'r', encoding='utf-8') as f:
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

    def build_prompt(
        self,
        user_query: str,
        table_names: List[str],
        *,
        golden_examples_text: Optional[str] = None,
        table_selection_notes: Optional[str] = None,
    ) -> str:
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

        return self.prompt_loader.render_prompt(
            self.prompt_name,
            schemas_text=schemas_text,
            user_query=user_query,
            golden_examples_text=golden_examples_text or "None",
            table_selection_notes=table_selection_notes or "Use the provided tables conservatively and only join related tables when needed.",
        )

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

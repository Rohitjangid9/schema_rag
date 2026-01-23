"""
Graph Logic: Find related tables via foreign keys and relationships
Expands search results to include contextually relevant tables
"""
import json
import sqlite3
from typing import List, Dict, Set, Any
from pathlib import Path


class GraphLogic:
    """Manages table relationships and graph expansion"""
    
    def __init__(self, db_path: str = "data/erp_data.db", metadata_file: str = "data/table_metadata.json"):
        self.db_path = db_path
        self.metadata_file = metadata_file
        self.metadata = self._load_metadata()
        self.relationships = self._build_relationships()
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load table metadata from JSON file"""
        try:
            if Path(self.metadata_file).exists():
                with open(self.metadata_file, 'r') as f:
                    metadata_list = json.load(f)
                    return {m['table_name']: m for m in metadata_list}
            else:
                print(f"⚠️  Metadata file not found: {self.metadata_file}")
                return {}
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return {}
    
    def _build_relationships(self) -> Dict[str, Set[str]]:
        """Build relationship graph from database schema"""
        relationships = {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                relationships[table] = set()
                
                # Get foreign keys for this table
                cursor.execute(f"PRAGMA foreign_key_list({table})")
                fk_rows = cursor.fetchall()
                
                for fk in fk_rows:
                    # fk[2] is the referenced table
                    referenced_table = fk[2]
                    relationships[table].add(referenced_table)
            
            conn.close()
            return relationships
        except Exception as e:
            print(f"Error building relationships: {e}")
            return {}
    
    def expand_search_results(self, search_results: List[Dict[str, Any]], depth: int = 1) -> Dict[str, Any]:
        """
        Expand search results to include related tables
        
        Args:
            search_results: List of tables from Qdrant search
            depth: How many levels of relationships to traverse (1-2)
        
        Returns:
            Dictionary with primary and related tables
        """
        primary_tables = {r['table_name'] for r in search_results}
        related_tables = set()
        
        # Level 1: Direct relationships
        for table in primary_tables:
            if table in self.relationships:
                related_tables.update(self.relationships[table])
        
        # Level 2: Relationships of related tables (if depth > 1)
        if depth > 1:
            secondary_related = set()
            for table in related_tables:
                if table in self.relationships:
                    secondary_related.update(self.relationships[table])
            related_tables.update(secondary_related)
        
        # Remove primary tables from related (avoid duplicates)
        related_tables -= primary_tables
        
        return {
            "primary_tables": sorted(list(primary_tables)),
            "related_tables": sorted(list(related_tables)),
            "all_tables": sorted(list(primary_tables | related_tables)),
            "total_tables": len(primary_tables | related_tables)
        }
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """Get detailed info about a specific table"""
        if table_name in self.metadata:
            return self.metadata[table_name]
        return {}
    
    def get_related_tables(self, table_name: str) -> List[str]:
        """Get tables directly related to a given table"""
        if table_name in self.relationships:
            return sorted(list(self.relationships[table_name]))
        return []
    
    def get_table_schema_snippet(self, table_name: str) -> str:
        """Get a formatted schema snippet for a table"""
        if table_name not in self.metadata:
            return f"-- Table {table_name} not found"
        
        metadata = self.metadata[table_name]
        columns = metadata.get('columns', [])
        
        columns_str = ",\n    ".join([
            f"{col['name']} {col['type']}" 
            for col in columns
        ])
        
        return f"""CREATE TABLE {table_name} (
    {columns_str}
);"""


if __name__ == "__main__":
    # Test the graph logic
    graph = GraphLogic()
    
    print("✓ Graph Logic initialized")
    print(f"✓ Loaded metadata for {len(graph.metadata)} tables")
    print(f"✓ Built relationships for {len(graph.relationships)} tables")
    
    # Test expansion
    test_results = [
        {"table_name": "sales_order", "summary": "Sales orders"},
        {"table_name": "crm_customer", "summary": "Customer info"}
    ]
    
    expanded = graph.expand_search_results(test_results)
    print(f"\n✓ Expansion test:")
    print(f"  Primary tables: {expanded['primary_tables']}")
    print(f"  Related tables: {expanded['related_tables'][:5]}...")
    print(f"  Total tables: {expanded['total_tables']}")


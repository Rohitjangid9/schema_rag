"""
Extract metadata from all tables in the database
Includes schema, foreign keys, and relationships for RAG retrieval
"""
import sqlite3
import json
from typing import List, Dict, Any, Tuple
from pathlib import Path


class TableMetadataExtractor:
    def __init__(self, db_path: str = "data/erp_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")  # Enable FK support
        self.cursor = self.conn.cursor()

    def get_all_tables(self) -> List[str]:
        """Get all table names from the database"""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        return [row[0] for row in self.cursor.fetchall()]

    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Get column information for a specific table"""
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for row in self.cursor.fetchall():
            columns.append({
                "name": row[1],
                "type": row[2],
                "not_null": bool(row[3]),
                "default": row[4],
                "primary_key": bool(row[5])
            })
        return columns

    def get_foreign_keys(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get foreign key relationships for a table

        Returns list of dicts with:
        - column: local column name
        - referenced_table: target table
        - referenced_column: target column
        """
        self.cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys = []
        for row in self.cursor.fetchall():
            foreign_keys.append({
                "column": row[3],              # from column
                "referenced_table": row[2],    # table
                "referenced_column": row[4]    # to column
            })
        return foreign_keys

    def get_table_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """Get indexes for a table"""
        self.cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = []
        for row in self.cursor.fetchall():
            index_name = row[1]
            is_unique = bool(row[2])

            # Get columns in this index
            self.cursor.execute(f"PRAGMA index_info({index_name})")
            columns = [col[2] for col in self.cursor.fetchall()]

            indexes.append({
                "name": index_name,
                "unique": is_unique,
                "columns": columns
            })
        return indexes

    def get_table_row_count(self, table_name: str) -> int:
        """Get row count for a specific table"""
        try:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Error counting rows in {table_name}: {e}")
            return 0

    def get_sample_data(self, table_name: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get sample rows from a table for context"""
        try:
            self.cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            columns = [desc[0] for desc in self.cursor.description]
            rows = []
            for row in self.cursor.fetchall():
                rows.append(dict(zip(columns, row)))
            return rows
        except Exception:
            return []

    def get_table_metadata(self, table_name: str, include_sample: bool = False) -> Dict[str, Any]:
        """Get complete metadata for a table including foreign keys"""
        columns = self.get_table_columns(table_name)
        foreign_keys = self.get_foreign_keys(table_name)
        row_count = self.get_table_row_count(table_name)

        # Extract module and entity from table name
        parts = table_name.split('_')
        module = parts[0] if len(parts) > 0 else "unknown"
        entity = '_'.join(parts[1:]) if len(parts) > 1 else table_name

        # Get related tables from foreign keys
        related_tables = list(set([fk["referenced_table"] for fk in foreign_keys]))

        # Identify primary key columns
        pk_columns = [col["name"] for col in columns if col["primary_key"]]

        metadata = {
            "table_name": table_name,
            "module": module,
            "entity": entity,
            "columns": columns,
            "column_count": len(columns),
            "primary_keys": pk_columns,
            "foreign_keys": foreign_keys,
            "related_tables": related_tables,
            "row_count": row_count,
            "description": f"Table {table_name} in {module} module with {len(columns)} columns"
        }

        # Optionally include sample data
        if include_sample:
            metadata["sample_data"] = self.get_sample_data(table_name)

        return metadata

    def extract_all_metadata(self, include_sample: bool = False) -> List[Dict[str, Any]]:
        """Extract metadata for all tables"""
        tables = self.get_all_tables()
        metadata_list = []

        print(f"\n{'='*60}")
        print(f"EXTRACTING TABLE METADATA")
        print(f"{'='*60}")
        print(f"Database: {self.db_path}")
        print(f"Tables found: {len(tables)}")
        print(f"Include sample data: {include_sample}")
        print(f"{'='*60}\n")

        for i, table_name in enumerate(tables, 1):
            print(f"  [{i}/{len(tables)}] {table_name}...", end=" ", flush=True)
            metadata = self.get_table_metadata(table_name, include_sample)
            metadata_list.append(metadata)
            fk_count = len(metadata["foreign_keys"])
            print(f"✓ ({metadata['column_count']} cols, {fk_count} FKs)")

        return metadata_list

    def extract_relationship_graph(self) -> Dict[str, List[str]]:
        """
        Extract a graph of table relationships (bidirectional)
        Returns dict: table_name -> list of related tables
        """
        tables = self.get_all_tables()
        graph = {table: set() for table in tables}

        for table in tables:
            fks = self.get_foreign_keys(table)
            for fk in fks:
                ref_table = fk["referenced_table"]
                if ref_table in graph:
                    # Bidirectional relationship
                    graph[table].add(ref_table)
                    graph[ref_table].add(table)

        # Convert sets to sorted lists
        return {table: sorted(list(related)) for table, related in graph.items()}

    def save_metadata_to_json(self, metadata_list: List[Dict], output_file: str = "table_metadata.json"):
        """Save metadata to JSON file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Metadata saved to {output_file}")

    def save_relationships_to_json(self, output_file: str = "table_relationships.json"):
        """Save relationship graph to JSON file"""
        graph = self.extract_relationship_graph()
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)
        print(f"✓ Relationships saved to {output_file}")
        return graph

    def close(self):
        """Close database connection"""
        self.conn.close()

    def get_statistics(self, metadata_list: List[Dict]) -> Dict[str, Any]:
        """Get statistics about the extracted metadata"""
        total_tables = len(metadata_list)
        total_columns = sum(m["column_count"] for m in metadata_list)
        total_rows = sum(m["row_count"] for m in metadata_list)
        tables_with_fk = sum(1 for m in metadata_list if len(m["foreign_keys"]) > 0)
        total_fks = sum(len(m["foreign_keys"]) for m in metadata_list)

        modules = {}
        for m in metadata_list:
            module = m["module"]
            if module not in modules:
                modules[module] = 0
            modules[module] += 1

        return {
            "total_tables": total_tables,
            "total_columns": total_columns,
            "total_rows": total_rows,
            "tables_with_foreign_keys": tables_with_fk,
            "total_foreign_keys": total_fks,
            "modules": modules,
            "avg_columns_per_table": round(total_columns / total_tables, 1) if total_tables > 0 else 0
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract database metadata")
    parser.add_argument("--db", default="data/erp_data.db", help="Database path")
    parser.add_argument("--output", default="data/table_metadata.json", help="Output file")
    parser.add_argument("--relationships", default="data/table_relationships.json", help="Relationships file")
    parser.add_argument("--sample", action="store_true", help="Include sample data")
    args = parser.parse_args()

    extractor = TableMetadataExtractor(args.db)

    # Extract metadata
    metadata = extractor.extract_all_metadata(include_sample=args.sample)
    extractor.save_metadata_to_json(metadata, args.output)

    # Extract and save relationships
    relationships = extractor.save_relationships_to_json(args.relationships)

    # Print statistics
    stats = extractor.get_statistics(metadata)
    print(f"\n{'='*60}")
    print("EXTRACTION STATISTICS")
    print(f"{'='*60}")
    print(f"  Total tables: {stats['total_tables']}")
    print(f"  Total columns: {stats['total_columns']}")
    print(f"  Total rows: {stats['total_rows']:,}")
    print(f"  Tables with FKs: {stats['tables_with_foreign_keys']}")
    print(f"  Total FKs: {stats['total_foreign_keys']}")
    print(f"  Avg cols/table: {stats['avg_columns_per_table']}")
    print(f"\n  Modules:")
    for module, count in sorted(stats['modules'].items()):
        print(f"    - {module}: {count} tables")
    print(f"{'='*60}")

    # Show sample metadata
    if metadata:
        print(f"\nSample metadata (first table):")
        sample = metadata[0].copy()
        sample["columns"] = sample["columns"][:3]  # Limit columns for display
        print(json.dumps(sample, indent=2))

    extractor.close()


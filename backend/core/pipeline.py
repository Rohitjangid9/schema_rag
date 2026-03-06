"""
Complete Schema RAG Pipeline Orchestrator
Coordinates: Metadata Extraction -> Summarization -> Embedding -> Qdrant Upload

Enhanced with:
- Foreign key extraction
- Relationship graph building
- RAG-optimized summaries
- Merged JSON output
"""
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from metadata_extractor import TableMetadataExtractor
from nvidia_summarizer import NVIDIASummarizer
from qdrant_manager import QdrantManager


class SchemaRAGPipeline:
    def __init__(
        self,
        db_path: str = "data/erp_data.db",
        output_dir: str = "data"
    ):
        self.db_path = db_path
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Output files
        self.metadata_file = self.output_dir / "table_metadata.json"
        self.summaries_file = self.output_dir / "table_summaries.json"
        self.relationships_file = self.output_dir / "table_relationships.json"
        self.merged_file = self.output_dir / "table_metadata_with_summaries.json"

    def step_1_extract_metadata(self) -> tuple[List[Dict], Dict[str, List[str]]]:
        """Step 1: Extract table metadata and relationships"""
        print("\n" + "="*60)
        print("STEP 1: EXTRACTING TABLE METADATA & RELATIONSHIPS")
        print("="*60)

        extractor = TableMetadataExtractor(self.db_path)

        # Extract metadata with foreign keys
        metadata = extractor.extract_all_metadata()
        extractor.save_metadata_to_json(metadata, str(self.metadata_file))

        # Extract relationship graph
        relationships = extractor.save_relationships_to_json(str(self.relationships_file))

        # Print statistics
        stats = extractor.get_statistics(metadata)
        print(f"\n  Statistics:")
        print(f"    Tables: {stats['total_tables']}")
        print(f"    Columns: {stats['total_columns']}")
        print(f"    Foreign Keys: {stats['total_foreign_keys']}")
        print(f"    Tables with relationships: {stats['tables_with_foreign_keys']}")

        extractor.close()
        return metadata, relationships

    def step_2_generate_summaries(
        self,
        metadata: List[Dict],
        relationships: Dict[str, List[str]]
    ) -> Dict[str, str]:
        """Step 2: Generate RAG-optimized summaries using NVIDIA API"""
        print("\n" + "="*60)
        print("STEP 2: GENERATING RAG-OPTIMIZED SUMMARIES")
        print("="*60)

        try:
            summarizer = NVIDIASummarizer()

            # Pass relationships for context in summaries
            summaries = summarizer.generate_summaries_batch(
                metadata,
                str(self.summaries_file),
                foreign_keys=relationships
            )

            return summaries

        except Exception as e:
            print(f"Error: Error generating summaries: {e}")
            print("  Using fallback summaries...")
            return self._generate_fallback_summaries(metadata)

    def _generate_fallback_summaries(self, metadata: List[Dict]) -> Dict[str, str]:
        """Generate fallback summaries if API fails"""
        summaries = {}
        for item in metadata:
            table_name = item["table_name"]
            module = item["module"]
            entity = item["entity"]
            columns = item["columns"]

            # Build a more descriptive fallback
            col_names = [c["name"] for c in columns[:5]]
            summaries[table_name] = (
                f"Table {table_name} in the {module} module stores {entity.replace('_', ' ')} data. "
                f"Contains {item['column_count']} columns including {', '.join(col_names)}. "
                f"Currently has {item['row_count']} records."
            )

        with open(self.summaries_file, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, indent=2, ensure_ascii=False)

        return summaries

    def step_3_create_merged_json(
        self,
        metadata: List[Dict],
        summaries: Dict[str, str],
        relationships: Dict[str, List[str]]
    ) -> List[Dict]:
        """Step 3: Create merged JSON with metadata + summaries + relationships"""
        print("\n" + "="*60)
        print("STEP 3: CREATING MERGED JSON")
        print("="*60)

        merged_data = []

        for item in metadata:
            table_name = item["table_name"]

            # Create merged record
            merged = item.copy()
            merged["ai_summary"] = summaries.get(table_name, "")
            merged["all_related_tables"] = relationships.get(table_name, [])

            merged_data.append(merged)

        # Save merged file
        with open(self.merged_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)

        print(f"Done: Merged JSON saved to {self.merged_file}")
        print(f"  Contains: metadata + AI summaries + relationships")

        return merged_data

    def step_4_create_embeddings_and_upload(
        self,
        metadata: List[Dict],
        summaries: Dict[str, str],
        relationships: Dict[str, List[str]],
        recreate: bool = False
    ) -> QdrantManager:
        """Step 4: Create embeddings and upload to Qdrant"""
        print("\n" + "="*60)
        print("STEP 4: CREATING EMBEDDINGS & UPLOADING TO QDRANT")
        print("="*60)

        try:
            manager = QdrantManager()
            manager.create_collection(recreate=recreate)

            # Prepare points with relationships for better context
            points = manager.prepare_points(
                metadata,
                summaries,
                foreign_keys=relationships
            )
            manager.upload_points(points)

            info = manager.get_collection_info()
            print(f"\nDone: Collection Info:")
            print(f"    Name: {info['name']}")
            print(f"    Points: {info['points_count']}")
            print(f"    Status: {info['status']}")

            return manager

        except Exception as e:
            print(f"Error: Error uploading to Qdrant: {e}")
            print("  Make sure Qdrant is running on localhost:6334")
            raise

    def step_5_test_retrieval(self, manager: QdrantManager):
        """Step 5: Test retrieval functionality"""
        print("\n" + "="*60)
        print("STEP 5: TESTING RETRIEVAL")
        print("="*60)

        test_queries = [
            "show me revenue by city",
            "customer sales orders",
            "employee salary and benefits",
            "inventory stock levels",
            "financial accounting records"
        ]

        for query in test_queries:
            print(f"\n  Query: '{query}'")
            results = manager.search(query, limit=3)
            for i, result in enumerate(results, 1):
                print(f"    {i}. {result['table_name']} (score: {result['score']:.3f})")
                if result['summary']:
                    print(f"       {result['summary'][:80]}...")

    def run_full_pipeline(self, skip_summaries: bool = False, recreate_qdrant: bool = False):
        """Run the complete pipeline"""
        print("\n" + "="*70)
        print("🚀 SCHEMA RAG PIPELINE - COMPLETE EXECUTION")
        print("="*70)
        print(f"  Database: {self.db_path}")
        print(f"  Output directory: {self.output_dir}")
        print("="*70)

        try:
            # Step 1: Extract metadata
            metadata, relationships = self.step_1_extract_metadata()

            # Step 2: Generate summaries
            if skip_summaries and self.summaries_file.exists():
                print("\n⏭️  Skipping summary generation (using existing file)")
                with open(self.summaries_file, 'r') as f:
                    summaries = json.load(f)
            else:
                summaries = self.step_2_generate_summaries(metadata, relationships)

            # Step 3: Create merged JSON
            self.step_3_create_merged_json(metadata, summaries, relationships)

            # Step 4: Create embeddings and upload
            manager = self.step_4_create_embeddings_and_upload(
                metadata, summaries, relationships, recreate=recreate_qdrant
            )

            # Step 5: Test retrieval
            self.step_5_test_retrieval(manager)

            print("\n" + "="*70)
            print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*70)
            print("\nOutput files created:")
            print(f"  📄 {self.metadata_file}")
            print(f"  📄 {self.summaries_file}")
            print(f"  📄 {self.relationships_file}")
            print(f"  📄 {self.merged_file}")
            print("\nYour Schema RAG is ready to use!")
            print("  - Qdrant collection: schema_metadata")
            print(f"  - Tables indexed: {len(metadata)}")
            print("  - Ready for semantic search queries")
            print("="*70)

        except Exception as e:
            print(f"\nError: Pipeline failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Schema RAG Pipeline")
    parser.add_argument("--db", default="data/erp_data.db", help="Database path")
    parser.add_argument("--output", default="data", help="Output directory")
    parser.add_argument("--skip-summaries", action="store_true", help="Skip summary generation")
    parser.add_argument("--recreate", action="store_true", help="Recreate Qdrant collection")
    args = parser.parse_args()

    pipeline = SchemaRAGPipeline(db_path=args.db, output_dir=args.output)
    pipeline.run_full_pipeline(
        skip_summaries=args.skip_summaries,
        recreate_qdrant=args.recreate
    )


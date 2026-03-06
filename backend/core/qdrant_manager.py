"""
Manage Qdrant vector database for schema embeddings
Uses NVIDIA's Llama 3.2 NemoRetriever embedding model
Optimized for RAG retrieval with enhanced text combining
"""
import json
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class QdrantManager:
    def __init__(self, host: str = "localhost", port: int = 6334, collection_name: str = "schema_metadata"):
        self.host = host
        self.port = port
        self.collection_name = collection_name

        # Initialize Qdrant client
        self.client = QdrantClient(host=host, port=port)

        # Initialize NVIDIA embedding client
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")

        self.embedding_client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
        )
        self.embedding_model = os.getenv("NVIDIA_EMBEDDING_MODEL", "nvidia/llama-3.2-nv-embedqa-1b-v2")
        self.embedding_dim = int(os.getenv("NVIDIA_EMBEDDING_DIM", "2048"))  # Dimension of NV-EmbedQA model

        print(f"✓ Connected to Qdrant at {host}:{port}")
        print(f"✓ Using NVIDIA embedding model: {self.embedding_model}")
        print(f"✓ Embedding dimension: {self.embedding_dim}")

        # Validate collection health on startup
        self.ensure_collection_ready()

    def _is_collection_healthy(self) -> bool:
        """Check if the collection exists and is not corrupted by doing a test scroll."""
        try:
            self.client.get_collection(self.collection_name)
            # Probe with a small scroll to detect index corruption early
            self.client.scroll(
                collection_name=self.collection_name,
                limit=1,
                with_vectors=False,
            )
            return True
        except Exception as e:
            err_msg = str(e).lower()
            if "not found" in err_msg or "doesn't exist" in err_msg:
                return False  # Collection doesn't exist yet — not an error
            if "panicked" in err_msg or "outputtoosmall" in err_msg or "internal error" in err_msg:
                print(f"⚠️  Collection '{self.collection_name}' is corrupted: {e}")
                return False
            # Unknown error — assume unhealthy
            print(f"⚠️  Collection health check failed: {e}")
            return False

    def _rebuild_from_saved_data(self):
        """
        Rebuild the Qdrant collection from saved metadata and summaries JSON files.
        This is used for auto-recovery when the collection is corrupted.
        """
        # Resolve data directory relative to this file (core/) -> parent (backend/) -> data/
        data_dir = Path(__file__).resolve().parent.parent / "data"
        metadata_file = data_dir / "table_metadata.json"
        summaries_file = data_dir / "table_summaries.json"
        relationships_file = data_dir / "table_relationships.json"

        if not metadata_file.exists() or not summaries_file.exists():
            print("⚠️  Cannot auto-rebuild: metadata/summaries files not found in data/")
            print(f"   Expected: {metadata_file}")
            print(f"   Expected: {summaries_file}")
            print("   Please re-run the pipeline: python core/pipeline.py")
            return False

        print("🔄 Auto-rebuilding collection from saved data...")
        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata_list = json.load(f)
        with open(summaries_file, "r", encoding="utf-8") as f:
            summaries = json.load(f)

        relationships = {}
        if relationships_file.exists():
            with open(relationships_file, "r", encoding="utf-8") as f:
                relationships = json.load(f)

        # Delete corrupted collection if it exists
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass

        # Create fresh collection
        self.create_collection(recreate=False)

        # Re-embed and upload
        points = self.prepare_points(metadata_list, summaries, foreign_keys=relationships)
        self.upload_points(points)
        print(f"✅ Auto-rebuilt collection with {len(points)} points")
        return True

    def ensure_collection_ready(self):
        """Ensure the collection exists and is healthy. Auto-recover if corrupted."""
        if self._is_collection_healthy():
            info = self.get_collection_info()
            if info.get("points_count", 0) > 0:
                print(f"✓ Collection '{self.collection_name}' is healthy ({info['points_count']} points)")
                return
            else:
                print(f"ℹ️  Collection '{self.collection_name}' exists but is empty.")
                # Try to rebuild from saved data
                self._rebuild_from_saved_data()
                return

        # Collection is missing or corrupted — try auto-recovery
        print(f"⚠️  Collection '{self.collection_name}' is missing or corrupted.")
        self._rebuild_from_saved_data()

    def create_collection(self, recreate: bool = False):
        """Create a collection in Qdrant if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            if recreate:
                print(f"  Deleting existing collection '{self.collection_name}'...")
                self.client.delete_collection(self.collection_name)
                raise Exception("Recreating")  # Force creation
            print(f"✓ Collection '{self.collection_name}' already exists")
        except Exception:
            # Create new collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_dim,
                    distance=Distance.COSINE
                )
            )
            print(f"✓ Created collection '{self.collection_name}'")
    
    def generate_embedding(self, text: str, input_type: str = "query") -> List[float]:
        """
        Generate embedding for text using NVIDIA API

        Args:
            text: Text to embed
            input_type: "query" for search queries, "passage" for documents
        """
        try:
            response = self.embedding_client.embeddings.create(
                input=[text],
                model=self.embedding_model,
                encoding_format="float",
                extra_body={"input_type": input_type, "truncate": "NONE"}
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise

    def _identify_important_columns(self, columns: List[Dict]) -> Dict[str, List[str]]:
        """Identify important columns by semantic meaning for better embedding"""
        important = {
            "business_terms": [],  # Columns with business meaning
            "all_names": []        # All column names
        }

        # Keywords that indicate important business columns
        business_keywords = [
            "amount", "price", "cost", "total", "revenue", "balance", "salary", "fee",
            "quantity", "count", "date", "name", "status", "type", "customer", "order",
            "product", "employee", "invoice", "payment", "address", "city", "region"
        ]

        for col in columns:
            col_name = col["name"]
            important["all_names"].append(col_name)

            # Check if column name contains business keywords
            name_lower = col_name.lower()
            for keyword in business_keywords:
                if keyword in name_lower:
                    important["business_terms"].append(col_name)
                    break

        return important

    def _build_embedding_text(
        self,
        metadata: Dict,
        summary: str,
        foreign_keys: Optional[List[str]] = None
    ) -> str:
        """
        Build optimized text for embedding that captures semantic meaning

        The text is structured to maximize retrieval accuracy:
        1. Table identity (name, module, entity)
        2. AI-generated summary (rich with search terms)
        3. Important column names (business-relevant)
        4. Related tables (via foreign keys)
        """
        table_name = metadata["table_name"]
        module = metadata["module"]
        entity = metadata["entity"]
        columns = metadata["columns"]

        # Get important columns
        important_cols = self._identify_important_columns(columns)

        # Build text parts
        parts = [
            # Core identity
            f"Table: {table_name}",
            f"Module: {module}",
            f"Entity: {entity.replace('_', ' ')}",

            # AI Summary (most important for semantic search)
            f"Description: {summary}" if summary else "",

            # Business columns (help match queries like "revenue", "customer", etc.)
            f"Key columns: {', '.join(important_cols['business_terms'])}" if important_cols['business_terms'] else "",

            # All columns (for exact column name matches)
            f"Columns: {', '.join(important_cols['all_names'][:15])}",  # Limit to avoid too much noise
        ]

        # Add related tables if available
        if foreign_keys and len(foreign_keys) > 0:
            parts.append(f"Related tables: {', '.join(foreign_keys)}")

        # Combine non-empty parts
        combined = ". ".join([p for p in parts if p])

        return combined

    def prepare_points(
        self,
        metadata_list: List[Dict],
        summaries: Dict[str, str],
        foreign_keys: Optional[Dict[str, List[str]]] = None,
        show_progress: bool = True
    ) -> List[PointStruct]:
        """
        Prepare points for Qdrant with enhanced embedding text

        Args:
            metadata_list: List of table metadata
            summaries: Dict mapping table_name -> AI summary
            foreign_keys: Optional dict mapping table_name -> list of related tables
            show_progress: Whether to show progress during embedding generation
        """
        points = []
        total = len(metadata_list)

        if show_progress:
            print(f"\nGenerating embeddings for {total} tables...")

        for i, metadata in enumerate(metadata_list):
            table_name = metadata["table_name"]
            summary = summaries.get(table_name, "")
            table_fks = foreign_keys.get(table_name, []) if foreign_keys else None

            # Build optimized embedding text
            combined_text = self._build_embedding_text(metadata, summary, table_fks)

            if show_progress:
                print(f"  [{i+1}/{total}] Embedding {table_name}...", end=" ", flush=True)

            # Generate embedding (use "passage" type for documents)
            embedding = self.generate_embedding(combined_text, input_type="passage")

            if show_progress:
                print("✓")

            # Prepare column names list
            column_names = [col["name"] for col in metadata["columns"]]

            # Create point with rich payload
            point = PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "table_name": table_name,
                    "module": metadata["module"],
                    "entity": metadata["entity"],
                    "summary": summary,
                    "columns": column_names,
                    "row_count": metadata["row_count"],
                    "column_count": metadata["column_count"],
                    "related_tables": table_fks if table_fks else [],
                    "embedding_text": combined_text,  # Store for debugging
                    "full_metadata": json.dumps(metadata)
                }
            )
            points.append(point)

        if show_progress:
            print(f"✓ Generated {len(points)} embeddings")

        return points
    
    def upload_points(self, points: List[PointStruct]):
        """Upload points to Qdrant"""
        print(f"Uploading {len(points)} points to Qdrant...")
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"✓ Successfully uploaded {len(points)} points")

    def _tokenize_terms(self, text: str) -> set[str]:
        """Tokenize text into normalized terms for lightweight lexical matching."""
        tokens = set()
        for raw_token in re.findall(r"[a-z0-9_]+", (text or "").lower()):
            for token in raw_token.split("_"):
                if len(token) < 2:
                    continue
                tokens.add(token)
                if token.endswith("ies") and len(token) > 4:
                    tokens.add(token[:-3] + "y")
                elif token.endswith("s") and not token.endswith("ss") and len(token) > 3:
                    tokens.add(token[:-1])
        return tokens

    def _calculate_lexical_boost(self, query: str, result: Dict[str, Any]) -> float:
        """Apply a small boost when query terms match table identity terms."""
        query_terms = self._tokenize_terms(query)
        if not query_terms:
            return 0.0

        identity_text = " ".join([
            result.get("table_name", ""),
            result.get("module", ""),
            result.get("entity", ""),
        ])
        identity_terms = self._tokenize_terms(identity_text)
        shared_identity_terms = query_terms & identity_terms

        boost = 0.0
        if shared_identity_terms:
            boost += min(0.14, 0.05 + (0.03 * len(shared_identity_terms)))

        query_text = query.lower()
        table_phrase = result.get("table_name", "").replace("_", " ").lower()
        entity_phrase = result.get("entity", "").replace("_", " ").lower()
        if table_phrase and table_phrase in query_text:
            boost += 0.05
        elif entity_phrase and entity_phrase in query_text:
            boost += 0.03

        return min(boost, 0.18)

    def _apply_lexical_rerank(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Blend Qdrant vector results with a conservative lexical boost."""
        reranked_results = []
        for result in results:
            vector_score = float(result.get("score", 0.0) or 0.0)
            lexical_boost = self._calculate_lexical_boost(query, result)
            reranked_results.append({
                **result,
                "vector_score": vector_score,
                "lexical_boost": lexical_boost,
                "score": vector_score + lexical_boost,
            })

        reranked_results.sort(
            key=lambda item: (item["score"], item.get("vector_score", 0.0)),
            reverse=True,
        )
        return reranked_results
    
    def search(self, query: str, limit: int = 5, score_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search for similar tables using semantic search.
        Auto-recovers from corrupted collections by rebuilding from saved data.

        Args:
            query: Natural language query
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0-1)
        """
        # Use "query" type for search queries
        query_embedding = self.generate_embedding(query, input_type="query")

        try:
            results = self._execute_search(query_embedding, limit, score_threshold)
        except Exception as e:
            err_msg = str(e).lower()
            if "panicked" in err_msg or "outputtoosmall" in err_msg or "internal error" in err_msg:
                print(f"⚠️  Qdrant search failed due to corruption: {e}")
                print("🔄 Attempting auto-recovery...")
                if self._rebuild_from_saved_data():
                    # Retry once after rebuild
                    results = self._execute_search(query_embedding, limit, score_threshold)
                else:
                    print("❌ Auto-recovery failed. Please re-run the pipeline.")
                    return []
            else:
                raise

        return self._apply_lexical_rerank(query, results)

    def _execute_search(
        self, query_embedding: List[float], limit: int, score_threshold: float
    ) -> List[Dict[str, Any]]:
        """Execute the actual Qdrant search query."""
        from qdrant_client.models import ScoredPoint

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
            score_threshold=score_threshold if score_threshold > 0 else None
        )

        # Handle QueryResponse object
        points = results.points if hasattr(results, 'points') else results

        return [
            {
                "table_name": point.payload["table_name"],
                "module": point.payload["module"],
                "entity": point.payload.get("entity", ""),
                "summary": point.payload["summary"],
                "score": point.score,
                "columns": point.payload["columns"],
                "related_tables": point.payload.get("related_tables", []),
                "row_count": point.payload.get("row_count", 0)
            }
            for point in points
        ]

    def search_with_context(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """
        Search with additional context about the search
        Returns results plus metadata about the search
        """
        results = self.search(query, limit)

        return {
            "query": query,
            "results": results,
            "total_found": len(results),
            "modules_found": list(set(r["module"] for r in results)),
            "top_score": results[0]["score"] if results else 0
        }

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "points_count": info.points_count,
                "status": "ready"
            }
        except Exception as e:
            return {
                "name": self.collection_name,
                "points_count": 0,
                "vectors_count": 0,
                "status": f"error: {e}"
            }

    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            print(f"✓ Deleted collection '{self.collection_name}'")
        except Exception as e:
            print(f"✗ Error deleting collection: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage Qdrant vector database")
    parser.add_argument("--metadata", default="data/table_metadata.json", help="Metadata file")
    parser.add_argument("--summaries", default="data/table_summaries.json", help="Summaries file")
    parser.add_argument("--recreate", action="store_true", help="Recreate collection from scratch")
    parser.add_argument("--test-query", default="customer sales orders", help="Test query")
    args = parser.parse_args()

    # Load metadata and summaries
    print(f"Loading metadata from {args.metadata}...")
    with open(args.metadata, 'r') as f:
        metadata_list = json.load(f)

    print(f"Loading summaries from {args.summaries}...")
    with open(args.summaries, 'r') as f:
        summaries = json.load(f)

    # Initialize Qdrant manager
    manager = QdrantManager()

    # Create collection
    manager.create_collection(recreate=args.recreate)

    # Prepare and upload points
    points = manager.prepare_points(metadata_list, summaries)
    manager.upload_points(points)

    # Get collection info
    info = manager.get_collection_info()
    print(f"\n✓ Collection Info: {info}")

    # Test search
    print(f"\n{'='*60}")
    print("TESTING SEARCH FUNCTIONALITY")
    print(f"{'='*60}")

    test_queries = [
        args.test_query,
        "show me revenue by city",
        "employee salary information",
        "inventory stock levels"
    ]

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = manager.search(query, limit=3)
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['table_name']} (score: {result['score']:.3f})")
            print(f"     {result['summary'][:100]}...")


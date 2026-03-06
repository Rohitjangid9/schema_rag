"""
Reranker using NVIDIA NIM nv-rerank-qa-mistral-4b:1 model.
Reranks Qdrant search results to improve relevance ordering.
"""
import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Reranker:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        if not self.api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables")

        self.base_url = os.getenv(
            "NVIDIA_RERANKER_URL",
            "https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking"
        )
        self.model = os.getenv("NVIDIA_RERANKER_MODEL", "nv-rerank-qa-mistral-4b:1")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.last_rerank_used_fallback = False
        self.last_error: Optional[str] = None
    
    def rerank(
        self, 
        query: str, 
        search_results: List[Dict[str, Any]], 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Rerank search results using NVIDIA's rerank model
        
        Args:
            query: The user's natural language query
            search_results: List of search results from Qdrant with 'table_name', 'summary', etc.
            top_k: Number of top results to return after reranking
            
        Returns:
            Reranked list of search results (top_k items)
        """
        if not search_results:
            return []
        
        self.last_rerank_used_fallback = False
        self.last_error = None

        # Build passages from search results
        # Each passage combines table info for better reranking
        passages = []
        for result in search_results:
            passage_text = self._build_passage_text(result)
            passages.append({"text": passage_text})

        # Build request payload
        payload = {
            "model": self.model,
            "query": {"text": query},
            "passages": passages
        }

        try:
            response = self.session.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()

            result = response.json()
            rankings = result.get("rankings", [])

            if not rankings:
                raise ValueError("Reranking API returned no rankings")

            # Sort by logit score (higher is better)
            rankings_sorted = sorted(rankings, key=lambda x: x.get("logit", float("-inf")), reverse=True)

            # Return top_k reranked results
            reranked_results = []
            for rank in rankings_sorted:
                original_index = rank.get("index")
                if original_index is None or not 0 <= original_index < len(search_results):
                    continue

                reranked_item = search_results[original_index].copy()
                if "logit" in rank:
                    reranked_item["rerank_score"] = rank["logit"]
                reranked_results.append(reranked_item)

                if len(reranked_results) >= top_k:
                    break

            if not reranked_results:
                raise ValueError("Reranking API returned no valid rankings")

            return reranked_results

        except requests.exceptions.HTTPError as e:
            self.last_rerank_used_fallback = True
            status_code = e.response.status_code if e.response is not None else "unknown"
            response_body = ""
            if e.response is not None:
                response_body = e.response.text[:500]

            self.last_error = f"HTTP {status_code}"
            print(f"⚠️  Reranking API error: HTTP {status_code} for {self.base_url}")
            if response_body:
                print(f"    Response body: {response_body}")
            return search_results[:top_k]
        except requests.exceptions.RequestException as e:
            self.last_rerank_used_fallback = True
            self.last_error = str(e)
            print(f"⚠️  Reranking API error: {e}")
            # Fallback: return original results (first top_k)
            return search_results[:top_k]
        except Exception as e:
            self.last_rerank_used_fallback = True
            self.last_error = str(e)
            print(f"⚠️  Reranking error: {e}")
            return search_results[:top_k]
    
    def _build_passage_text(self, result: Dict[str, Any]) -> str:
        """
        Build a text passage from a search result for reranking
        Includes table name, module, summary, and key columns
        """
        table_name = result.get("table_name", "unknown")
        module = result.get("module", "")
        summary = result.get("summary", "")
        columns = result.get("columns", [])
        
        # Build a rich passage for reranking
        parts = [f"Table: {table_name}"]
        
        if module:
            parts.append(f"Module: {module}")
        
        if summary:
            parts.append(f"Description: {summary}")
        
        if columns:
            # Include first 10 column names for context
            col_names = columns[:10] if len(columns) > 10 else columns
            parts.append(f"Columns: {', '.join(col_names)}")
        
        return " | ".join(parts)
    
    def rerank_with_scores(
        self, 
        query: str, 
        search_results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Rerank all results and return with scores (no top_k limit)
        Useful for debugging and analysis
        """
        return self.rerank(query, search_results, top_k=len(search_results))


if __name__ == "__main__":
    # Test the reranker
    reranker = Reranker()
    
    # Mock search results
    mock_results = [
        {
            "table_name": "sales_order",
            "module": "sales",
            "summary": "Stores sales order transactions including amounts and dates",
            "columns": ["id", "order_date", "total_amount", "customer_id"],
            "score": 0.85
        },
        {
            "table_name": "crm_customer",
            "module": "crm",
            "summary": "Customer master data with contact information",
            "columns": ["id", "name", "email", "phone", "address"],
            "score": 0.80
        },
        {
            "table_name": "inventory_product",
            "module": "inventory",
            "summary": "Product catalog with pricing and stock levels",
            "columns": ["id", "name", "price", "stock_qty"],
            "score": 0.75
        }
    ]
    
    query = "show me total revenue by customer"
    print(f"\nQuery: {query}")
    print(f"Original order: {[r['table_name'] for r in mock_results]}")
    
    reranked = reranker.rerank(query, mock_results, top_k=3)
    print(f"Reranked order: {[r['table_name'] for r in reranked]}")
    print(f"Rerank scores: {[r.get('rerank_score', 'N/A') for r in reranked]}")


from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import Query as QueryModel
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent / "core"))

from qdrant_manager import QdrantManager
from graph_logic import GraphLogic
from prompt_builder import PromptBuilder
from sql_generator import SQLGenerator
from query_executor import QueryExecutor
from result_formatter import ResultFormatter
from reranker import Reranker

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schema Rag", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
try:
    qdrant_manager = QdrantManager()
    graph_logic = GraphLogic()
    prompt_builder = PromptBuilder()
    sql_generator = SQLGenerator()
    query_executor = QueryExecutor()
    result_formatter = ResultFormatter()
    reranker = Reranker()
    print("✓ All managers initialized (Phase 1, 2, 3 + Reranker)")
except Exception as e:
    print(f"⚠️  Warning: Could not initialize managers: {e}")
    qdrant_manager = None
    graph_logic = None
    prompt_builder = None
    sql_generator = None
    query_executor = None
    result_formatter = None
    reranker = None


# Define request/response models
class QueryRequest(BaseModel):
    query: str
    context: Optional[str] = None


class QueryResponse(BaseModel):
    query: str
    response: str
    status: str
    tables_found: Optional[List[str]] = None
    related_tables: Optional[List[str]] = None


class SearchResult(BaseModel):
    table_name: str
    module: str
    summary: str
    score: float
    columns: List[str]


class SearchResponse(BaseModel):
    query: str
    primary_tables: List[str]
    related_tables: List[str]
    all_tables: List[str]
    total_tables: int
    search_results: List[SearchResult]


class Phase2Response(BaseModel):
    query: str
    tables_used: List[str]
    sql_query: str
    status: str
    error: Optional[str] = None


class Phase3Response(BaseModel):
    query: str
    tables_used: List[str]
    sql_query: str
    rows_returned: int
    answer: str
    status: str
    error: Optional[str] = None


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Schema Rag",
        "qdrant": "connected" if qdrant_manager else "disconnected",
        "graph_logic": "ready" if graph_logic else "not ready",
        "reranker": "ready" if reranker else "not ready"
    }


# Phase 1: Search endpoint
@app.post("/search", response_model=SearchResponse)
async def search_tables(request: QueryRequest):
    """
    PHASE 1: Search for relevant tables with RERANKING
    - Searches Qdrant for 15 candidate tables
    - Reranks using NVIDIA nv-rerank-qa-mistral-4b:1 → top 5
    - Expands results using graph logic to find related tables
    """
    if not qdrant_manager or not graph_logic:
        return {
            "query": request.query,
            "primary_tables": [],
            "related_tables": [],
            "all_tables": [],
            "total_tables": 0,
            "search_results": [],
            "error": "Managers not initialized"
        }

    try:
        # Step 1: Search Qdrant for 15 candidate tables
        search_results = qdrant_manager.search(request.query, limit=15)

        # Step 2: Rerank to get top 5
        if reranker and len(search_results) > 0:
            reranked_results = reranker.rerank(request.query, search_results, top_k=5)
        else:
            reranked_results = search_results[:5]

        # Step 3: Expand with graph logic to find related tables
        expansion = graph_logic.expand_search_results(reranked_results, depth=1)

        # Format search results (include rerank_score if available)
        formatted_results = [
            SearchResult(
                table_name=r['table_name'],
                module=r['module'],
                summary=r['summary'],
                score=r.get('rerank_score', r['score']),  # Use rerank score if available
                columns=r['columns']
            )
            for r in reranked_results
        ]

        return SearchResponse(
            query=request.query,
            primary_tables=expansion['primary_tables'],
            related_tables=expansion['related_tables'],
            all_tables=expansion['all_tables'],
            total_tables=expansion['total_tables'],
            search_results=formatted_results
        )

    except Exception as e:
        print(f"Error in search: {e}")
        return {
            "query": request.query,
            "primary_tables": [],
            "related_tables": [],
            "all_tables": [],
            "total_tables": 0,
            "search_results": [],
            "error": str(e)
        }


# Phase 2: SQL Generation endpoint
@app.post("/generate-sql", response_model=Phase2Response)
async def generate_sql(request: QueryRequest):
    """
    PHASE 2: Generate SQL query from natural language
    - Searches for relevant tables (Phase 1)
    - Reranks results using NVIDIA nv-rerank-qa-mistral-4b:1
    - Builds prompt with schemas
    - Generates SQL using Llama 70B
    """
    if not qdrant_manager or not graph_logic or not prompt_builder or not sql_generator:
        return Phase2Response(
            query=request.query,
            tables_used=[],
            sql_query="",
            status="error",
            error="Managers not initialized"
        )

    try:
        # Step 1: Search for 15 candidate tables
        search_results = qdrant_manager.search(request.query, limit=15)

        # Step 2: Rerank to get top 5
        if reranker and len(search_results) > 0:
            reranked_results = reranker.rerank(request.query, search_results, top_k=5)
        else:
            reranked_results = search_results[:5]

        # Step 3: Expand with graph logic
        expansion = graph_logic.expand_search_results(reranked_results, depth=1)
        tables_to_use = expansion['primary_tables']

        # Step 4: Build prompt with schemas
        prompt = prompt_builder.build_prompt(request.query, tables_to_use)

        # Step 5: Generate SQL using Llama 70B
        sql_query = sql_generator.generate_sql(prompt)

        # Step 6: Clean and validate SQL
        sql_query = sql_generator.clean_sql(sql_query)
        is_valid, error = sql_generator.validate_sql(sql_query)

        if not is_valid:
            return Phase2Response(
                query=request.query,
                tables_used=tables_to_use,
                sql_query=sql_query,
                status="validation_failed",
                error=error
            )

        return Phase2Response(
            query=request.query,
            tables_used=tables_to_use,
            sql_query=sql_query,
            status="success"
        )

    except Exception as e:
        print(f"Error in Phase 2: {e}")
        return Phase2Response(
            query=request.query,
            tables_used=[],
            sql_query="",
            status="error",
            error=str(e)
        )


# Phase 3: Complete workflow (Search + Rerank + SQL Generation + Execution + Formatting)
@app.post("/chat", response_model=Phase3Response)
async def chat(request: QueryRequest):
    """
    PHASE 3: Complete chatbot workflow with RERANKING
    - Step 1: Search Qdrant for 15 candidate tables
    - Step 2: RERANK using NVIDIA nv-rerank-qa-mistral-4b:1 → top 5
    - Step 3: Expand with graph logic for related tables
    - Step 4: Generate SQL using Llama 70B
    - Step 5: Execute query and format results
    """
    if not all([qdrant_manager, graph_logic, prompt_builder, sql_generator, query_executor, result_formatter]):
        return Phase3Response(
            query=request.query,
            tables_used=[],
            sql_query="",
            rows_returned=0,
            answer="",
            status="error",
            error="Managers not initialized"
        )

    try:
        # Step 1: Search Qdrant for 15 candidate tables (more than we need)
        search_results = qdrant_manager.search(request.query, limit=15)

        # Step 2: RERANK to get top 5 most relevant tables
        if reranker and len(search_results) > 0:
            reranked_results = reranker.rerank(request.query, search_results, top_k=5)
            print(f"✓ Reranked {len(search_results)} tables → top {len(reranked_results)}")
        else:
            # Fallback: use first 5 from Qdrant if reranker unavailable
            reranked_results = search_results[:5]
            print("⚠️  Reranker not available, using Qdrant order")

        # Step 3: Expand with graph logic for related tables (via foreign keys)
        expansion = graph_logic.expand_search_results(reranked_results, depth=1)
        tables_to_use = expansion['primary_tables']

        # Step 4: Generate SQL
        prompt = prompt_builder.build_prompt(request.query, tables_to_use)
        sql_query = sql_generator.generate_sql(prompt)
        sql_query = sql_generator.clean_sql(sql_query)

        # Validate SQL
        is_valid, error = sql_generator.validate_sql(sql_query)
        if not is_valid:
            return Phase3Response(
                query=request.query,
                tables_used=tables_to_use,
                sql_query=sql_query,
                rows_returned=0,
                answer="",
                status="sql_validation_failed",
                error=error
            )

        # Step 5: Execute query
        exec_result = query_executor.execute_query(sql_query)

        if not exec_result['success']:
            return Phase3Response(
                query=request.query,
                tables_used=tables_to_use,
                sql_query=sql_query,
                rows_returned=0,
                answer="",
                status="execution_failed",
                error=exec_result['error']
            )

        # Format results
        rows = exec_result['rows']
        columns = exec_result['columns']
        answer = result_formatter.format_results(request.query, rows, columns)

        return Phase3Response(
            query=request.query,
            tables_used=tables_to_use,
            sql_query=sql_query,
            rows_returned=len(rows),
            answer=answer,
            status="success"
        )

    except Exception as e:
        print(f"Error in Phase 3: {e}")
        return Phase3Response(
            query=request.query,
            tables_used=[],
            sql_query="",
            rows_returned=0,
            answer="",
            status="error",
            error=str(e)
        )


# Main API endpoint (Phase 1 integration)
@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a schema-based RAG query
    PHASE 1: Search and discover relevant tables
    """
    try:
        # Get search results
        search_results = qdrant_manager.search(request.query, limit=5) if qdrant_manager else []
        expansion = graph_logic.expand_search_results(search_results, depth=1) if graph_logic else {}

        tables_found = expansion.get('primary_tables', [])
        related = expansion.get('related_tables', [])

        response_text = f"Found {len(tables_found)} primary tables and {len(related)} related tables for your query."

        # Create query record in database
        db_query = QueryModel(
            query_text=request.query,
            context=request.context,
            response=response_text,
            status="phase1_complete"
        )
        db.add(db_query)
        db.commit()
        db.refresh(db_query)

        return QueryResponse(
            query=request.query,
            response=response_text,
            status="phase1_complete",
            tables_found=tables_found,
            related_tables=related
        )

    except Exception as e:
        print(f"Error processing query: {e}")
        return QueryResponse(
            query=request.query,
            response=f"Error: {str(e)}",
            status="error",
            tables_found=[],
            related_tables=[]
        )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Schema Rag API - Phase 1 Ready",
        "version": "1.0.0",
        "phase": "Phase 1: Search & Discovery",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "search": "/search (POST) - PHASE 1: Find relevant tables",
            "query": "/query (POST) - PHASE 1: Full search workflow",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "example_queries": [
            "Show me total revenue by city",
            "List all employees in sales department",
            "What's the inventory level for product X?"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app_runtime import create_runtime
from config import load_app_config
from database import Base, engine, get_db
from models import Query as QueryModel
from schemas.api import (
    Phase2Response,
    Phase3Response,
    QueryRequest,
    QueryResponse,
    SearchResponse,
    SearchResult,
)
from services.chat_workflow import ChatWorkflow
from services.search_service import SearchService
from services.sql_generation_service import SQLGenerationService

# Load environment variables
load_dotenv()

settings = load_app_config()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_title, version=settings.app_version)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runtime = create_runtime(settings)
search_service = SearchService(runtime)
sql_generation_service = SQLGenerationService(runtime)
chat_workflow = ChatWorkflow(runtime)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.app_title,
        "qdrant": "connected" if runtime.qdrant_manager else "disconnected",
        "graph_logic": "ready" if runtime.graph_logic else "not ready",
        "reranker": "ready" if runtime.reranker else "not ready",
        "prompt_dir": str(settings.prompt_dir),
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
    return search_service.run(request)


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
    return sql_generation_service.run(request)


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
    return chat_workflow.run(request)


# Main API endpoint (Phase 1 integration)
@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Process a schema-based RAG query
    PHASE 1: Search and discover relevant tables
    """
    try:
        # Get search results
        search_results = runtime.qdrant_manager.search(request.query, limit=5) if runtime.qdrant_manager else []
        expansion = runtime.graph_logic.expand_search_results(search_results, depth=1) if runtime.graph_logic else {}

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

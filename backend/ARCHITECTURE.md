# Backend Architecture - Phase 1 + Phase 2

## Directory Structure

```
backend/
├── config/                    # Centralized app config
│   ├── __init__.py
│   └── app_config.py         # AppConfig dataclass + load_app_config()
├── core/                      # Business logic modules
│   ├── chat_debug_logger.py   # Markdown debug logging
│   ├── graph_logic.py         # Bidirectional relationship expansion
│   ├── prompt_builder.py      # Schema extraction + prompt building
│   ├── prompt_loader.py       # YAML prompt loading
│   ├── qdrant_manager.py      # Vector search + lexical boost
│   ├── query_executor.py      # SQL execution against SQLite
│   ├── reranker.py            # NVIDIA reranking
│   ├── result_formatter.py    # LLM-based result formatting
│   └── sql_generator.py       # SQL generation + validation + repair
├── prompts/                   # YAML prompt templates
│   ├── sql_generation.yaml    # SQL generation prompt
│   └── result_formatter.yaml  # Result formatting prompt
├── schemas/                   # Shared API models
│   ├── __init__.py
│   └── api.py                 # QueryRequest, Phase2Response, Phase3Response, etc.
├── services/                  # Service layer (Phase 1 cleanup)
│   ├── __init__.py
│   ├── chat_workflow.py       # LangGraph-based /chat orchestration
│   ├── retrieval_service.py   # Shared retrieval logic
│   ├── search_service.py      # /search endpoint service
│   └── sql_generation_service.py  # /generate-sql endpoint service
├── tests/                     # Test suite
│   ├── test_langgraph_workflow.py
│   ├── test_chat_debug_logger.py
│   ├── test_prompt_loader.py
│   └── ...
├── app_runtime.py             # AppRuntime + create_runtime() factory
├── main.py                    # FastAPI app (173 lines, pure delegation)
├── database.py                # SQLAlchemy setup
├── models.py                  # SQLAlchemy models
└── data/                      # Data files
    ├── erp_data.db            # SQLite business DB
    └── erp_schema_dump.sql    # Schema definitions
```

## Key Concepts

### AppConfig (config/app_config.py)
- Centralized settings from environment
- Paths to schema file, business DB, prompts
- Qdrant connection details
- CORS origins

### AppRuntime (app_runtime.py)
- Holds all initialized managers
- `create_runtime(config)` factory function
- Health check methods: `has_search()`, `has_phase2()`, `has_chat()`

### ChatState (services/chat_workflow.py)
- TypedDict defining graph state
- Passed through all 7 nodes
- Includes debug_logger for logging at each step

### LangGraph Nodes
Each node is a pure function: `(state: ChatState) -> ChatState`
- Nodes are independent, testable
- State flows through edges
- Self-healing repair loop built in

### Prompts (prompts/*.yaml)
- Externalized from Python code
- YAML format with `template` and `input_variables`
- Loaded by PromptLoader, rendered with `.format(**variables)`

## API Endpoints

- `POST /search` → SearchService → SearchResponse
- `POST /generate-sql` → SQLGenerationService → Phase2Response
- `POST /chat` → ChatWorkflow (LangGraph) → Phase3Response
- `POST /query` → Direct search + graph expansion
- `GET /health` → Health check
- `GET /` → Root info

## Data Flow: /chat Endpoint

```
QueryRequest
    ↓
ChatWorkflow.run()
    ↓
graph.invoke(initial_state)
    ├─ retrieval node: Qdrant search + rerank
    ├─ graph_expansion node: Foreign-key relationships
    ├─ prompt_building node: Schema + user query
    ├─ sql_generation node: Llama 70B → SQL
    ├─ sql_repair node: Validate + repair if needed
    ├─ execution node: SQLite query
    ├─ formatting node: Llama 8B → natural language
    └─ END
    ↓
Phase3Response (with debug log written)
```

## Testing Strategy

- Unit tests for each service
- Integration tests for graph nodes
- Fake managers for isolated testing
- Debug logs for manual verification


# Schema Rag

A FastAPI-based application for Schema-based Retrieval-Augmented Generation (RAG).

## Overview

Schema Rag is a simple FastAPI application that provides endpoints for processing schema-based queries with RAG capabilities.

## Features

- FastAPI framework for high performance
- CORS middleware for cross-origin requests
- Health check endpoint
- Query processing endpoint with Pydantic models
- Interactive API documentation (Swagger UI and ReDoc)

## Project Structure

```
Schema Rag/
├── main.py              # Main application file
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:

```bash
python main.py
```

The application will be available at `http://localhost:8000`

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### GET /
Root endpoint providing welcome message and available endpoints.

### GET /health
Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "Schema Rag"
}
```

### POST /query
Process a schema-based RAG query.

**Request:**
```json
{
  "query": "Your query here",
  "context": "Optional context"
}
```

**Response:**
```json
{
  "query": "Your query here",
  "response": "Processing query: Your query here",
  "status": "success"
}
```

## Development

To run the server with auto-reload during development:

```bash
uvicorn main:app --reload
```

## Future Enhancements

- Implement actual RAG logic
- Add database integration
- Add authentication
- Add query logging and monitoring
- Add schema validation

## License

MIT

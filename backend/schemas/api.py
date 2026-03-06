from typing import List, Optional

from pydantic import BaseModel


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
    error: Optional[str] = None


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
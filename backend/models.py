from sqlalchemy import Column, Integer, String, Text, DateTime, func
from datetime import datetime
from database import Base


class Query(Base):
    """Query model for storing RAG queries"""
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    query_text = Column(String(500), nullable=False)
    response = Column(Text, nullable=True)
    context = Column(Text, nullable=True)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    class Config:
        from_attributes = True

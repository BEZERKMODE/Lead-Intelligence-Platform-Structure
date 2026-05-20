from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base, engine

# Detect if using SQLite fallback
is_sqlite = engine.url.drivername == "sqlite"

if is_sqlite:
    VectorType = Text
else:
    from pgvector.sqlalchemy import Vector
    VectorType = Vector(384)

class LeadModel(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True, nullable=False)
    domain = Column(String, unique=True, index=True, nullable=False)
    sector = Column(String, index=True)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    revenue = Column(String)
    employees = Column(String)
    technologies = Column(Text)
    contacts = Column(Text)
    priority_score = Column(Integer, default=0)
    ai_match_rate = Column(Integer, default=0)
    growth_trend = Column(String)
    status = Column(String, default="New", index=True)
    last_scraped = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    security_score = Column(String, default="A")
    subdomains = Column(Text)
    vulnerabilities = Column(Text)
    phone = Column(String)
    
    # Semantic embedding vector
    embedding = Column(VectorType)


class TenantModel(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    workspace_name = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    workflow_name = Column(String)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)

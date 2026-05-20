import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from backend.config import settings

# Attempt to create PostgreSQL engine with automatic SQLite fallback on any failure
engine_success = False
has_pgvector = False

try:
    if settings.DATABASE_URL and not settings.DATABASE_URL.startswith("sqlite"):
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        # Test connection to ensure the database actually exists and is accessible
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
            # Dynamically detect if pgvector extension is available/supported
            try:
                # Check if 'vector' type exists in the database already
                res = conn.execute(text("SELECT 1 FROM pg_type WHERE typname = 'vector'")).fetchone()
                if res:
                    has_pgvector = True
                else:
                    # Attempt to dynamically register it
                    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                    has_pgvector = True
            except Exception as ext_err:
                has_pgvector = False
                
        engine_success = True
        if has_pgvector:
            print("[DB] Successfully connected to PostgreSQL with pgvector support enabled!")
        else:
            print("[DB] Connected to PostgreSQL. pgvector is not available; falling back to text-based embeddings.")
except Exception as e:
    print(f"[DB] PostgreSQL connection failed ({e}). Falling back to local SQLite database.")

if not engine_success:
    # Use SQLite fallback
    sqlite_path = os.path.join(os.path.dirname(__file__), "database.db")
    sqlite_url = f"sqlite:///{sqlite_path}"
    engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
    print(f"[DB] SQLite database initialized at {sqlite_path}")

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

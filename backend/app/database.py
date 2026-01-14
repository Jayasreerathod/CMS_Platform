# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

# --- Get DB URL ---
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        " DATABASE_URL not set. Please export it before running. Example:\n"
        "   set DATABASE_URL=postgresql://<user>:<password>@<host>/<db_name>"
    )

# --- Fix Render-style postgres:// URLs ---
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# --- Handle SSL for Render Postgres ---
connect_args = {}
if "render.com" in DATABASE_URL:
    connect_args["sslmode"] = "require"

# --- Create engine ---
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# --- Session factory ---
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# --- Declarative base ---
Base = declarative_base()

# --- Dependency for FastAPI routes ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Health check helper ---
def test_connection():
    """Used in /health endpoint to verify DB connection."""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        return True
    except OperationalError:
        return False

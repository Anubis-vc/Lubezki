# i know this non-async version does work
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel
from app.core.config import settings
from contextlib import contextmanager

# Create engine with NullPool (no connection pooling)
engine = create_engine(settings.DB_CXN_STRING, client_encoding='utf8', poolclass=NullPool)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_session():
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def get_db_info():
    """Get database information"""
    try:
        with engine.connect() as conn:
            # Get PostgreSQL version
            version_result = conn.execute(text("SELECT version()"))
            version = version_result.scalar()
            
            # Get current database
            db_result = conn.execute(text("SELECT current_database()"))
            current_db = db_result.scalar()
            
            return {
                "connected": True,
                "version": version,
                "database": current_db,
                "connection_string": settings.DB_CXN_STRING
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e),
            "connection_string": settings.DB_CXN_STRING
        }
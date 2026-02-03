"""
Database module for presenter_app
Provides SQLAlchemy engine, session management, and base class for models
"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os

# Database URL from environment variable
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://presenter_app_user:password@localhost/presenter_app'
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_size=10,        # Connection pool size
    max_overflow=20,     # Max overflow connections
    echo=False           # Set to True for SQL query logging
)

# Create session factory
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Usage in Flask routes:
        db = next(get_db())
        try:
            # Use db here
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    Usage:
        with get_db_context() as db:
            # Use db here
            db.commit()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def execute_raw_sql(query, params=None):
    """
    Execute raw SQL query and return results.

    Args:
        query (str): SQL query with :param placeholders
        params (dict, optional): Parameters for query

    Returns:
        list: List of Row objects from query result

    Example:
        results = execute_raw_sql(
            "SELECT * FROM groups WHERE section = :section",
            {'section': 'A'}
        )
    """
    with get_db_context() as db:
        result = db.execute(text(query), params or {})
        return result.fetchall()


def execute_insert(query, params=None, return_id=False):
    """
    Execute INSERT query and optionally return inserted ID.

    Args:
        query (str): INSERT SQL query
        params (dict, optional): Parameters for query
        return_id (bool): Whether to return inserted ID

    Returns:
        int or None: Inserted ID if return_id=True, else None

    Example:
        group_id = execute_insert(
            "INSERT INTO groups (group_name, section) VALUES (:name, :section) RETURNING id",
            {'name': 'Group 1', 'section': 'A'},
            return_id=True
        )
    """
    with get_db_context() as db:
        result = db.execute(text(query), params or {})
        if return_id:
            # For RETURNING clause
            row = result.fetchone()
            return row[0] if row else None
        return None


def execute_update(query, params=None):
    """
    Execute UPDATE or DELETE query.

    Args:
        query (str): UPDATE or DELETE SQL query
        params (dict, optional): Parameters for query

    Returns:
        int: Number of rows affected

    Example:
        rows_affected = execute_update(
            "UPDATE groups SET status = :status WHERE id = :id",
            {'status': 'active', 'id': 123}
        )
    """
    with get_db_context() as db:
        result = db.execute(text(query), params or {})
        return result.rowcount


# Helper function to convert SQLAlchemy Row to dict
def row_to_dict(row):
    """Convert SQLAlchemy Row object to dictionary."""
    if row is None:
        return None
    return dict(row._mapping) if hasattr(row, '_mapping') else dict(row)


def rows_to_dicts(rows):
    """Convert list of SQLAlchemy Row objects to list of dictionaries."""
    return [row_to_dict(row) for row in rows]

# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.models import Base, Transactions, Portfolio, Log  # Import models

# Database URL for SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./api.db"

# Create the SQLAlchemy engine. For SQLite, `connect_args={"check_same_thread": False}` is used
# because SQLite has thread-safety issues when used with multiple threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

def create_tables():
    """
    Create all tables defined in the models by calling Base.metadata.create_all.
    This function will create the tables in the database if they do not already exist.
    """
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

# Create a sessionmaker instance that will be used to create new SQLAlchemy sessions.
# `autocommit=False` and `autoflush=False` are standard settings for FastAPI and SQLAlchemy.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function for providing a SQLAlchemy database session.

    This function uses a context manager to create a database session,
    ensuring that it is closed after use.

    Yields:
    - Session: An SQLAlchemy session object.
    """
    db = SessionLocal()
    try:
        yield db  # Yield the session for dependency injection
    finally:
        db.close()  # Ensure the session is closed after use

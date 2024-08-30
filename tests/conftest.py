# tests/conftest.py

import pytest
from app.database import Base, engine, SessionLocal
from app.models import Portfolio
from app.main import app

# Pytest fixture for setting up the database before running tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """
    Create the database tables before any tests are run.
    This fixture runs once per module (i.e., all tests in the module).
    """
    # Create all tables defined in the Base metadata
    Base.metadata.create_all(bind=engine)

# Pytest fixture for setting up sample portfolio data before each test
@pytest.fixture(scope="function")
def setup_portfolio():
    """
    Set up sample data in the portfolio table for testing.
    This fixture runs before each test function and ensures that
    the portfolio table is populated with consistent data.
    """
    db = SessionLocal()
    try:
        # Clear existing data from the Portfolio table
        db.query(Portfolio).delete()

        # Add sample portfolio entries to the database
        db.add(Portfolio(symbol="AAPL", shares=100, cost_basis=1000))
        db.add(Portfolio(symbol="GOOGL", shares=50, cost_basis=1000))
        db.commit()
        
        # Yield control back to the test function
        yield
    finally:
        # Close the database session to release resources
        db.close()

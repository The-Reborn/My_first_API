# tests/test_portfolio.py

from fastapi.testclient import TestClient
from app.main import app
from app.models import Base, Portfolio
from app.database import engine, SessionLocal, get_db
import pytest

# Create an instance of TestClient to interact with the FastAPI app
client = TestClient(app)

def test_get_all_portfolio(setup_portfolio):
    """
    Test the /api/portfolio endpoint to ensure it returns all portfolio entries
    when no symbol query parameter is provided.
    """
    # Send a GET request to the /api/portfolio endpoint
    response = client.get("/api/portfolio")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the JSON response data
    data = response.json()
    
    # Assert that the response contains two portfolio entries
    assert len(data) == 2  # Should return two portfolio entries
    
    # Assert that the response includes portfolio entries for AAPL and GOOGL
    assert any(entry['symbol'] == "AAPL" for entry in data)
    assert any(entry['symbol'] == "GOOGL" for entry in data)

def test_get_portfolio_by_symbol(setup_portfolio):
    """
    Test the /api/portfolio endpoint to ensure it returns portfolio entries
    for a specific symbol when the symbol query parameter is provided.
    """
    # Send a GET request to the /api/portfolio endpoint with symbol=AAPL
    response = client.get("/api/portfolio?symbol=AAPL")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the JSON response data
    data = response.json()
    
    # Assert that the response contains only one portfolio entry for AAPL
    assert len(data) == 1  # Should return only one portfolio entry for AAPL
    assert data[0]['symbol'] == "AAPL"

def test_get_portfolio_no_results():
    """
    Test the /api/portfolio endpoint to ensure it returns a 404 error when
    querying for a symbol that does not exist in the portfolio.
    """
    # Send a GET request to the /api/portfolio endpoint with a non-existent symbol
    response = client.get("/api/portfolio?symbol=NONEXISTENT")
    
    # Assert that the response status code is 404 (Not Found)
    assert response.status_code == 404  # Should return 404 for non-existent symbol
    
    # Parse the JSON response data
    data = response.json()
    
    # Assert that the response contains the expected error message
    assert data['detail'] == "No portfolio entry found"

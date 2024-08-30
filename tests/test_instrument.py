# tests/test_instrument.py

import pytest
from fastapi.testclient import TestClient
from app.main import app 

# Create an instance of TestClient to interact with the FastAPI app
client = TestClient(app)

def test_get_instrument():
    """
    Test the /api/instrument/{symbol} endpoint to ensure it returns the expected data
    when querying for a specific instrument symbol.
    """
    # Send a GET request to the /api/instrument/AAPL endpoint
    response = client.get("/api/instrument/AAPL")
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the JSON response data
    json_data = response.json()
    
    # Assert that the response JSON contains the expected fields
    assert "name" in json_data
    assert "bid" in json_data
    assert "ask" in json_data
    assert "current_price" in json_data
    assert "change_value" in json_data
    assert "change_percent" in json_data

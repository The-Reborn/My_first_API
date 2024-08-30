# tests/test_transaction.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Base, Transactions
from app.database import engine, SessionLocal

# Initialize the TestClient for sending requests to the FastAPI application
client = TestClient(app)

def test_get_all_transactions():
    """
    Test the /api/transactions endpoint to ensure it returns all transactions
    correctly. This test assumes there are at least two transactions in the
    database: one for 'AAPL' and one for 'GOOGL'.
    """
    response = client.get("/api/transactions")
    assert response.status_code == 200  # Check that the request was successful
    data = response.json()
    # Check if at least the two expected transactions are in the response
    assert any(txn['symbol'] == 'AAPL' for txn in data)
    assert any(txn['symbol'] == 'GOOGL' for txn in data)

def test_get_transactions_by_symbol():
    """
    Test the /api/transactions endpoint to ensure it returns transactions
    filtered by a specific symbol correctly. This test checks that transactions
    for the symbol 'AAPL' are returned when requested.
    """
    response = client.get("/api/transactions?symbol=AAPL")
    assert response.status_code == 200  # Check that the request was successful
    data = response.json()
    # Check if there's at least one transaction with the symbol 'AAPL'
    assert len(data) >= 1
    assert all(txn['symbol'] == 'AAPL' for txn in data)

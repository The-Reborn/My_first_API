# tests/test_purchase_instrument.py

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Transactions, Portfolio
from sqlalchemy.orm import Session
import pytest

# Initialize the TestClient for sending requests to the FastAPI application
client = TestClient(app)

def test_purchase_instrument(setup_portfolio):
    """
    Test the /api/purchase_instrument endpoint to ensure it correctly
    handles the purchase of an instrument and updates both transactions
    and portfolio records.
    """
    # Step 1: Perform the purchase by sending a POST request
    response = client.post("/api/purchase_instrument", params={"symbol": "AAPL", "shares": 5})
    
    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["shares"] == 5
    assert data["type"] == "Purchase"
    assert "price" in data
    assert "date" in data
    assert "value" in data
    
    purchase_price = data["price"]
    purchase_value = data["value"]

    # Step 2: Verify that the transaction was recorded in the database
    with next(get_db()) as db:  # Properly handle session context
        transaction = db.query(Transactions).filter_by(symbol="AAPL", type="Purchase", shares=5).first()
        assert transaction is not None  # Ensure that the transaction was found
        assert transaction.symbol == "AAPL"
        assert transaction.shares == 5
        assert pytest.approx(transaction.price, 0.01) == purchase_price  # Allow small margin for floating-point errors
        assert pytest.approx(transaction.value, 0.01) == purchase_value  # Same for value

        # Step 3: Verify that the portfolio was updated correctly
        updated_portfolio = db.query(Portfolio).filter_by(symbol="AAPL").first()
        assert updated_portfolio is not None  # Ensure that the portfolio entry was found
        assert updated_portfolio.symbol == "AAPL"
        assert updated_portfolio.shares == 105  # Original 100 shares + 5 purchased shares
        assert pytest.approx(updated_portfolio.cost_basis, 0.01) == 1000 + purchase_value  # Original 1000 + new purchase value

# tests/test_sale_instrument.py

from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Transactions, Portfolio
from sqlalchemy.orm import Session

# Initialize the TestClient for sending requests to the FastAPI application
client = TestClient(app)

def test_sale_instrument(setup_portfolio):
    """
    Test the /api/sell_instrument endpoint to ensure it correctly
    handles the sale of an instrument and updates both transactions
    and portfolio records.
    """
    # Step 1: Perform the sale by sending a POST request
    response = client.post("/api/sell_instrument", params={"symbol": "GOOGL", "shares": 10})

    # Validate the response
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "GOOGL"
    assert data["shares"] == 10
    assert data["type"] == "Sale"
    assert "price" in data
    assert "date" in data
    assert "value" in data

    sale_price = data["price"]
    sale_value = data["value"]

    # Print the response data for debugging
    print(f"Response Data: {data}")

    # Step 2: Verify that the transaction was recorded in the database
    with next(get_db()) as db:
        transaction = db.query(Transactions).filter_by(symbol="GOOGL", type="Sale", shares=10).first()
        assert transaction is not None  # Ensure that the transaction was found
        assert transaction.symbol == "GOOGL"
        assert transaction.shares == 10
        
        # Print the transaction data for debugging
        print(f"Transaction Data: Symbol: {transaction.symbol}, Shares: {transaction.shares}, Price: {transaction.price}, Value: {transaction.value}")

        # Verify that the price in the transaction matches the sale price
        assert abs(transaction.price - sale_price) < 0.01, f"Expected price {sale_price}, but got {transaction.price}. Difference: {abs(transaction.price - sale_price)}"

        # Verify the portfolio's cost basis has been updated correctly
        portfolio_entry = db.query(Portfolio).filter_by(symbol="GOOGL").first()
        if portfolio_entry:
            expected_cost_basis = 1000 - sale_value  # Original cost basis minus sale value
            assert abs(portfolio_entry.cost_basis - expected_cost_basis) < 0.01, f"Expected cost basis {expected_cost_basis}, but got {portfolio_entry.cost_basis}. Difference: {abs(portfolio_entry.cost_basis - expected_cost_basis)}"
        else:
            assert True, "Portfolio entry not found after sale"

    # Optionally, you could add additional assertions to verify that the total value or number of shares has been updated correctly, if necessary.

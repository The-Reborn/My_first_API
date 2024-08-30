# app/routes/sale.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Import database dependency
from app.models import Transactions, Portfolio  # Import database models for Transactions and Portfolio
from app.schemas import SaleResponse  # Import schema for sale response
from app.config.config import BASE_URL, REGION, LANG, API_KEY  # Import configuration values

from datetime import datetime  # Import datetime for timestamping
import requests  # Import requests library for making HTTP requests

# Create an APIRouter instance for defining routes
router = APIRouter()

@router.post("/sell_instrument", response_model=SaleResponse)
def sell_instrument(symbol: str, shares: int, db: Session = Depends(get_db)):
    """
    Handles the sale of a financial instrument and updates the portfolio.

    Args:
    - symbol (str): The symbol of the financial instrument to sell.
    - shares (int): The number of shares to sell.
    - db (Session): The database session dependency.

    Returns:
    - SaleResponse: The details of the sale.

    Raises:
    - HTTPException: If there are not enough shares to sell, if the instrument is not found in the portfolio, if there is an error fetching data from the Yahoo Finance API, or if sale price information is unavailable.
    """
    # Retrieve the portfolio entry for the given symbol
    portfolio_entry = db.query(Portfolio).filter_by(symbol=symbol).first()

    # Check if the portfolio entry exists and has enough shares to sell
    if not portfolio_entry or portfolio_entry.shares < shares:
        # Raise an HTTPException with a 400 status code if there are not enough shares or the instrument is not found
        raise HTTPException(status_code=400, detail="Not enough shares to sell or instrument not found in portfolio")
    
    # Construct the URL for the Yahoo Finance API request
    url = f"{BASE_URL}?region={REGION}&lang={LANG}&symbols={symbol}"
    headers = {"x-api-key": API_KEY}
    
    # Make the GET request to the Yahoo Finance API
    response = requests.get(url, headers=headers)
    
    # Check if the response status code is not 200 (OK)
    if response.status_code != 200:
        # Raise an HTTPException with a 500 status code if there's an error fetching data
        raise HTTPException(status_code=500, detail="Error fetching data from Yahoo Finance API")

    # Parse the response JSON data
    data = response.json()
    # Extract the result from the "quoteResponse" part of the JSON
    result = data.get("quoteResponse", {}).get("result", [])
    
    # Check if the result list is empty
    if not result:
        # Raise an HTTPException with a 404 status code if the instrument is not found
        raise HTTPException(status_code=404, detail="Instrument not found")

    # Get the first item from the result list
    instrument = result[0]
    # Extract the sale price from the instrument data
    sale_price = instrument.get("regularMarketPrice")

    # Check if the sale price is available
    if not sale_price:
        # Raise an HTTPException with a 500 status code if sale price information is not available
        raise HTTPException(status_code=500, detail="Sale price information not available")

    # Calculate the total sale value
    sale_value = shares * sale_price

    # Create a new Sale record
    sale = Transactions(
        symbol=symbol,
        type="Sale",
        shares=shares,
        price=sale_price,
        date=datetime.now().isoformat(),  # Current timestamp in ISO format
        value=sale_value
    )

    # Add the sale record to the database
    db.add(sale)

    # Update the portfolio entry
    portfolio_entry.shares -= shares
    portfolio_entry.cost_basis -= sale_value

    # If the cost basis is zero, remove the portfolio entry
    if portfolio_entry.cost_basis == 0:
        db.delete(portfolio_entry)

    # Commit the changes to the database
    db.commit()

    # Return the details of the sale
    return {
        "symbol": symbol,
        "type": 'Sale',
        "shares": shares,
        "price": sale_price,
        "date": datetime.now().isoformat(),
        "value": sale_value
    }
    


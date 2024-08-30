# app/routes/purchase.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Import database dependency
from app.models import Transactions, Portfolio  # Import database models for Transactions and Portfolio
from app.schemas import PurchaseResponse  # Import schema for purchase response
from app.config.config import BASE_URL, REGION, LANG, API_KEY  # Import configuration values

import requests  # Import requests library for making HTTP requests
from datetime import datetime  # Import datetime for timestamping

# Create an APIRouter instance for defining routes
router = APIRouter()

@router.post("/purchase_instrument", response_model=PurchaseResponse)
def purchase_instrument(symbol: str, shares: int, db: Session = Depends(get_db)):
    """
    Handles the purchase of a financial instrument and updates the portfolio.

    Args:
    - symbol (str): The symbol of the financial instrument to purchase.
    - shares (int): The number of shares to purchase.
    - db (Session): The database session dependency.

    Returns:
    - PurchaseResponse: The details of the purchase.

    Raises:
    - HTTPException: If there is an error fetching data from the Yahoo Finance API, if the instrument is not found, or if price information is unavailable.
    """
    # Construct the URL for the Yahoo Finance API request
    url = f"{BASE_URL}?region={REGION}&lang={LANG}&symbols={symbol}"
    
    # Set the API key in the headers
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
    # Extract the current market price from the instrument data
    price = instrument.get("regularMarketPrice")

    # Check if the price is available
    if not price:
        # Raise an HTTPException with a 500 status code if price information is not available
        raise HTTPException(status_code=500, detail="Price information not available")

    # Calculate the total purchase value
    purchase_value = shares * price

    # Create a new purchase record
    purchase = Transactions(
        symbol=symbol,
        type='Purchase',
        shares=shares,
        price=price,
        date=datetime.now().isoformat(),  # Current timestamp in ISO format
        value=purchase_value
    )

    # Add the purchase record to the database
    db.add(purchase)

    # Check if the symbol already exists in the portfolio
    portfolio_entry = db.query(Portfolio).filter_by(symbol=symbol).first()
    
    if portfolio_entry:
        # If the symbol exists, update the existing entry
        portfolio_entry.shares += shares
        portfolio_entry.cost_basis += purchase_value
    else:
        # If the symbol does not exist, create a new portfolio entry
        new_entry = Portfolio(symbol=symbol, shares=shares, cost_basis=purchase_value)
        db.add(new_entry)

    # Commit the changes to the database
    db.commit()

    # Return the details of the purchase
    return {
        "symbol": symbol,
        "type": 'Purchase',
        "shares": shares,
        "price": price,
        "date": datetime.now().isoformat(),
        "value": purchase_value
    }


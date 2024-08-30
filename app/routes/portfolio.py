# app/routes/get_portfolio.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db  # Import database dependency
from app.config.config import BASE_URL, REGION, LANG, API_KEY  # Import configuration values
from app.models import Portfolio  # Import the Portfolio model
from app.schemas import PortfolioResponse  # Import schema for response

from typing import Optional
import requests  # Import the requests library for making HTTP requests

# Create an APIRouter instance for defining routes
router = APIRouter()

def get_current_market_price(symbol: str) -> float:
    """
    Fetches the current market price of an instrument from Yahoo Finance API.

    Args:
    - symbol (str): The symbol of the financial instrument.

    Returns:
    - float: The current market price of the instrument.

    Raises:
    - HTTPException: If there is an error fetching data or if price information is not available.
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
    current_price = instrument.get("regularMarketPrice")
    
    # Check if the current price is available
    if not current_price:
        # Raise an HTTPException with a 500 status code if price information is not available
        raise HTTPException(status_code=500, detail="Price information not available")
    
    return current_price

@router.get("/portfolio", response_model=list[PortfolioResponse])
def get_portfolio(symbol: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Fetches portfolio entries and calculates their market values and returns them with additional metrics.

    Args:
    - symbol (Optional[str]): An optional symbol filter for the portfolio entries.
    - db (Session): The database session dependency.

    Returns:
    - list[PortfolioResponse]: A list of portfolio entries with calculated metrics.

    Raises:
    - HTTPException: If no portfolio entries are found.
    """
    # Query the Portfolio table
    query = db.query(Portfolio)
    
    # Filter the query by symbol if provided
    if symbol:
        query = query.filter_by(symbol=symbol)
    
    # Execute the query and get all portfolio entries
    portfolio_entries = query.all()
    
    # Check if no portfolio entries were found
    if not portfolio_entries:
        # Raise an HTTPException with a 404 status code if no entries are found
        raise HTTPException(status_code=404, detail="No portfolio entry found")
    
    result = []
    # Iterate over each portfolio entry to calculate metrics
    for entry in portfolio_entries:
        # Fetch the current market price for the symbol
        current_price = get_current_market_price(entry.symbol)
        # Calculate market value
        market_value = current_price * entry.shares
        # Calculate unrealized profit or loss
        unrealized_profit_loss = market_value - entry.cost_basis
        # Calculate unrealized return rate as a percentage
        unrealized_return_rate = (unrealized_profit_loss / entry.cost_basis) * 100 if entry.cost_basis != 0 else 0
        
        # Append the calculated metrics and portfolio entry data to the result list
        result.append({
            "symbol": entry.symbol,
            "shares": entry.shares,
            "cost_basis": entry.cost_basis,
            "market_value": market_value,
            "unrealized_return_rate": unrealized_return_rate,
            "unrealized_profit_loss": unrealized_profit_loss
        })
    
    # Return the list of portfolio entries with calculated metrics
    return result

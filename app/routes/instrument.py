# app/api/instruments.py

from fastapi import APIRouter, HTTPException  # Import required FastAPI classes
import requests  # Import the requests library for making HTTP requests
from app.config.config import BASE_URL, REGION, LANG, API_KEY  # Import configuration values

# Create an APIRouter instance for defining routes
router = APIRouter()

@router.get("/instrument/{symbol}")
def get_instrument(symbol: str):
    """
    Fetches instrument data from Yahoo Finance API based on the given symbol.

    Args:
    - symbol (str): The symbol of the financial instrument to fetch.

    Returns:
    - JSON response with instrument details if successful.
    - Raises HTTPException with appropriate status code and detail message if there's an error.
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

    # Return the instrument data in the desired format
    return {
        "name": instrument.get("longName"),  # Full name of the instrument
        "bid": instrument.get("bid"),  # Bid price of the instrument
        "ask": instrument.get("ask"),  # Ask price of the instrument
        "current_price": instrument.get("regularMarketPrice"),  # Current market price
        "change_value": instrument.get("regularMarketChange"),  # Change in value
        "change_percent": instrument.get("regularMarketChangePercent")  # Change percentage
    }

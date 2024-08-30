# app/routes/transactions.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc  # Import for sorting query results
from app.database import get_db  # Import database dependency
from app.models import Transactions  # Import Transactions model
from app.schemas import TransactionResponse  # Import schema for transaction response
from typing import List  # Import List for type hinting

# Create an APIRouter instance for defining routes
router = APIRouter()

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(symbol: str = None, db: Session = Depends(get_db)):
    """
    Fetches a list of transactions from the database, optionally filtered by symbol.

    Args:
    - symbol (str, optional): The symbol to filter transactions by. If not provided, fetches all transactions.
    - db (Session): The database session dependency.

    Returns:
    - List[TransactionResponse]: A list of transaction records.

    Notes:
    - Transactions are ordered by date in ascending order.
    """
    # Start a query for Transactions, ordered by date in ascending order
    query = db.query(Transactions).order_by(asc(Transactions.date))

    # If a symbol is provided, filter the transactions by symbol
    if symbol:
        query = query.filter(Transactions.symbol == symbol)

    # Execute the query and fetch all results
    transactions = query.all()

    # Return the list of transactions
    return transactions

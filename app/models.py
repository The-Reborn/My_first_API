# app/models.py

from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

# Create a base class for declarative class definitions
Base = declarative_base()

class Transactions(Base):
    """
    Model for storing transaction records.
    
    Represents a transaction entry in the database, which can be a purchase or a sale.
    """
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the transaction
    type = Column(String)  # Type of transaction: 'purchase' or 'sale'
    symbol = Column(String, index=True)  # Stock symbol for the transaction
    shares = Column(Integer)  # Number of shares involved in the transaction
    price = Column(Float)  # Price per share at the time of the transaction
    value = Column(Float)  # Total value of the transaction (shares * price)
    date = Column(String)  # Date of the transaction (ISO format)

class Portfolio(Base):
    """
    Model for storing portfolio entries.
    
    Represents individual holdings in a portfolio with stock symbols and their details.
    """
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the portfolio entry
    symbol = Column(String, unique=True, index=True)  # Stock symbol for the portfolio entry
    shares = Column(Integer)  # Number of shares held in the portfolio
    cost_basis = Column(Float)  # Total cost basis of the shares in the portfolio

class Log(Base):
    """
    Model for storing HTTP request/response logs.
    
    Represents log entries for monitoring and debugging HTTP requests and responses.
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the log entry
    path = Column(String, index=True)  # Request path (URL)
    method = Column(String)  # HTTP method used (GET, POST, etc.)
    status_code = Column(Integer)  # HTTP response status code
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # Timestamp of the log entry
    request_body = Column(Text, nullable=True)  # Body of the request, if applicable
    response_body = Column(Text, nullable=True)  # Body of the response, if applicable

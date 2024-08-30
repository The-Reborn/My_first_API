# app/schemas.py

from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# Base class for purchase-related data models
class PurchaseBase(BaseModel):
    """
    Base model for purchase data.
    Represents the common fields for purchase-related responses.
    """
    symbol: str  # Stock symbol
    shares: int  # Number of shares purchased
    price: float  # Price per share at the time of purchase
    date: datetime  # Date of the purchase
    value: float  # Total value of the purchase (shares * price)

# Class for creating a purchase (currently empty, but can be extended)
class PurchaseCreate(BaseModel):
    """
    Model for creating a new purchase.
    Currently does not add any new fields or validation.
    """
    pass

# Response model for purchase data
class PurchaseResponse(PurchaseBase):
    """
    Response model for purchase data.
    Includes the base purchase information along with a type field.
    """
    type: str  # Type of transaction: 'purchase'

# Base class for sale-related data models
class SaleBase(BaseModel):
    """
    Base model for sale data.
    Represents the common fields for sale-related responses.
    """
    symbol: str  # Stock symbol
    shares: int  # Number of shares sold
    price: float  # Price per share at the time of sale
    date: datetime  # Date of the sale
    value: float  # Total value of the sale (shares * price)

# Class for creating a sale (currently empty, but can be extended)
class SaleCreate(SaleBase):
    """
    Model for creating a new sale.
    Currently does not add any new fields or validation.
    """
    pass

# Response model for sale data
class SaleResponse(SaleBase):
    """
    Response model for sale data.
    Includes the base sale information along with a type field.
    """
    type: str  # Type of transaction: 'sale'

# Response model for transaction logs
class TransactionResponse(BaseModel):
    """
    Response model for transaction logs.
    Represents a transaction record with details such as ID, symbol, shares, and date.
    """
    id: int  # Unique identifier for the transaction
    symbol: str  # Stock symbol
    shares: int  # Number of shares involved in the transaction
    type: str  # Type of transaction (purchase or sale)
    value: float  # Total value of the transaction
    date: datetime  # Date of the transaction

    # Configuration for model attributes mapping
    model_config = ConfigDict(from_attributes=True)

# Response model for portfolio data
class PortfolioResponse(BaseModel):
    """
    Response model for portfolio data.
    Represents a portfolio entry with stock symbol, shares, cost basis, market value, and performance metrics.
    """
    symbol: str  # Stock symbol
    shares: int  # Number of shares held
    cost_basis: float  # Total cost basis of the shares
    market_value: float  # Current market value of the shares
    unrealized_return_rate: float  # Return rate of the shares (in percentage)
    unrealized_profit_loss: float  # Unrealized profit or loss of the shares

    # Configuration for model attributes mapping
    model_config = ConfigDict(from_attributes=True)

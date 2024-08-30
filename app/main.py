# app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.middleware.logging import LoggingMiddleware  # Import custom logging middleware
from app.database import create_tables  # Import function to create database tables
from app.routes import instrument, purchase, sale, transaction, portfolio  # Import routers for different routes
from app.config.otel_config import configure_tracing  # Import OpenTelemetry configuration

# Create a FastAPI instance
app = FastAPI()

# Configure OpenTelemetry for tracing
configure_tracing(app)

# Add custom logging middleware to the FastAPI app
app.add_middleware(LoggingMiddleware)

@asynccontextmanager
async def startup_event():
    """
    Async context manager for handling startup events.
    
    This function creates the database tables when the application starts.
    """
    create_tables()
    yield
    # Any teardown logic would go here (not needed in this case)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    This endpoint is available at the root URL ("/") and provides a basic welcome message.
    """
    return ["Welcome to the Yahoo-Finance-Extractor API"]

# Include routers from different route modules
app.include_router(instrument.router, prefix="/api", tags=["instrument"])
app.include_router(purchase.router, prefix="/api", tags=["purchase"])
app.include_router(sale.router, prefix="/api", tags=["sale"])
app.include_router(transaction.router, prefix="/api", tags=["transactions"])
app.include_router(portfolio.router, prefix="/api", tags=["portfolio"])

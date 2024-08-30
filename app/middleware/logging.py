# app/middleware/logging.py

# Import required libraries and modules
from fastapi import Request  # For handling incoming HTTP requests
from starlette.middleware.base import BaseHTTPMiddleware  # Base class for middleware in Starlette
from starlette.responses import Response  # For creating HTTP responses
from sqlalchemy.orm import Session  # For working with the SQLAlchemy database session
from app.database import get_db  # Function to get the database session
from app.models import Log  # Log model for database logging
import json  # For JSON operations (though not used here)
from opentelemetry import trace  # For OpenTelemetry tracing

# Define the custom middleware class
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Get a tracer instance
        tracer = trace.get_tracer(__name__)
        
        # Start a new trace span for the HTTP request
        with tracer.start_as_current_span("http_request"):
            # Extract request information
            path = str(request.url.path)  # Request URL path
            method = request.method  # HTTP method (GET, POST, etc.)
            request_body = await request.body()  # Request body
            
            # Pass the request to the next middleware or route handler
            response = await call_next(request)
            
            # Collect response body data
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Decode response body to string if it's not empty
            response_body_str = response_body.decode("utf-8") if response_body else ""

            # Obtain a database session
            db: Session = next(get_db())
            
            # Create a log entry object
            log_entry = Log(
                path=path,  # Request URL path
                method=method,  # HTTP method
                status_code=response.status_code,  # HTTP status code of the response
                request_body=request_body.decode("utf-8"),  # Request body as string
                response_body=response_body_str  # Response body as string
            )

            # Add log entry to the database and commit
            db.add(log_entry)
            db.commit()

            # Return the response to the client
            return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers))

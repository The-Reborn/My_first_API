# config/otel_config.py
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

def configure_tracing(app):
    # Set up the tracer provider with a resource (including service name)
    resource = Resource.create({"service.name": "my_fastapi_service"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer_provider = trace.get_tracer_provider()

    # Add a console exporter for debugging
    tracer_provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    # Instrument FastAPI and requests
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()

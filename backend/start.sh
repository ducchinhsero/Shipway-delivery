#!/bin/bash

# Start the FastAPI application
echo "Starting Shipway Backend..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

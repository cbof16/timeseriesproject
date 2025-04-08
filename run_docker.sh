#!/bin/bash

echo "Building Docker image (with no cache to ensure fresh dependencies)..."
docker build --no-cache -t temperature-forecasting .

echo "Running Docker container..."
docker run -p 8000:8000 -v $(pwd)/data:/app/data temperature-forecasting

# If you want to run in detached mode, use:
# docker run -d -p 8000:8000 -v $(pwd)/data:/app/data temperature-forecasting 
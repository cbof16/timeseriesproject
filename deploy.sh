#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the application with gunicorn
echo "Starting the application..."
gunicorn --bind 0.0.0.0:8000 \
         --workers 4 \
         --timeout 120 \
         --access-logfile logs/access.log \
         --error-logfile logs/error.log \
         "src.ui.app:create_app()" 2>&1 | tee logs/gunicorn.log

# Check if the application started successfully
if [ $? -eq 0 ]; then
    echo "Application started successfully!"
    echo "Access logs: logs/access.log"
    echo "Error logs: logs/error.log"
    echo "Gunicorn logs: logs/gunicorn.log"
else
    echo "Failed to start the application. Check logs/gunicorn.log for details."
fi 
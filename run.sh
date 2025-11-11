#!/bin/bash

# Script to run Hand Sign Detection Web App on Raspberry Pi

echo "======================================"
echo "Hand Sign Detection Web App"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
    echo "Please install dependencies first:"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Dependencies not installed!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Get IP address
IP=$(hostname -I | awk '{print $1}')

echo ""
echo "Starting Flask server..."
echo "Access the app at:"
echo "  - Local: http://localhost:5000"
echo "  - Network: http://$IP:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "======================================"
echo ""

# Run the app
python3 app.py

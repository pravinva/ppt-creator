#!/bin/bash

# Databricks Presentation Creator - Launch Script

echo "=========================================="
echo "Databricks Presentation Creator"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.deps_installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.deps_installed
    echo "✓ Dependencies installed"
fi

# Check Databricks CLI configuration
echo ""
echo "Checking Databricks CLI configuration..."
if ! command -v databricks &> /dev/null; then
    echo "⚠ Warning: Databricks CLI not found"
    echo "Please install it: pip install databricks-cli"
    echo "Then configure: databricks configure --token"
else
    if [ -f "$HOME/.databrickscfg" ]; then
        echo "✓ Databricks CLI is configured"
    else
        echo "⚠ Warning: Databricks CLI not configured"
        echo "Please run: databricks configure --token"
    fi
fi

echo ""
echo "=========================================="
echo "Starting application..."
echo "Open your browser to: http://localhost:8050"
echo "Press Ctrl+C to stop"
echo "=========================================="
echo ""

# Run the application
python app.py

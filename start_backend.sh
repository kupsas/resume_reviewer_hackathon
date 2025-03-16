#!/bin/bash

# Function to check if port is in use
check_port() {
    if lsof -i ":$1" > /dev/null 2>&1; then
        echo "Port $1 is already in use. Attempting to free it..."
        lsof -ti ":$1" | xargs kill -9 2>/dev/null
        sleep 1
        if lsof -i ":$1" > /dev/null 2>&1; then
            echo "Failed to free port $1. Please manually kill the process."
            return 1
        else
            echo "Port $1 freed successfully."
            return 0
        fi
    else
        echo "Port $1 is available."
        return 0
    fi
}

# Navigate to the correct directory
cd "$(dirname "$0")"
echo "Current directory: $(pwd)"

# Check if we're in the project root
if [ ! -d "backend" ]; then
    echo "Error: 'backend' directory not found. Make sure you're running this script from the project root."
    exit 1
fi

# Check and free port 8000 if needed
check_port 8000 || exit 1

# Navigate to backend directory
cd backend
echo "Changed to backend directory: $(pwd)"

# Activate virtual environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Error: Virtual environment not found in backend/venv"
    echo "Creating a new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    # Install requirements
    if [ -f "requirements.txt" ]; then
        echo "Installing requirements..."
        pip install -r requirements.txt
    else
        echo "Warning: requirements.txt not found. Skipping package installation."
    fi
fi

# Start the FastAPI server with proper Python path
echo "Starting FastAPI server..."
export PYTHONPATH=$(pwd)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
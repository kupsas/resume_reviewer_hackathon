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
if [ ! -d "frontend" ]; then
    echo "Error: 'frontend' directory not found. Make sure you're running this script from the project root."
    exit 1
fi

# Check and free port 3000 if needed
check_port 3000 || exit 1

# Navigate to frontend directory
cd frontend
echo "Changed to frontend directory: $(pwd)"

# Check if node_modules exists, if not install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the Next.js development server
echo "Starting Next.js development server..."
npm run dev 
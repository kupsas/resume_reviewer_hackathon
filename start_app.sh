#!/bin/bash

# Navigate to the correct directory
cd "$(dirname "$0")"
echo "Current directory: $(pwd)"

# Make scripts executable
chmod +x start_backend.sh
chmod +x start_frontend.sh

# Function to start a server in a new terminal window (macOS)
start_server() {
    echo "Starting $1 server..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        osascript -e "tell application \"Terminal\" to do script \"cd $(pwd) && ./$1\""
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd $(pwd) && ./$1; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd $(pwd) && ./$1; exec bash" &
        else
            echo "No supported terminal emulator found. Please run ./$1 manually."
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        # Windows with Git Bash or similar
        start bash -c "cd $(pwd) && ./$1"
    else
        echo "Unsupported OS. Please run ./$1 manually."
    fi
}

# Start backend server
start_server "start_backend.sh"

# Wait a moment before starting frontend
sleep 2

# Start frontend server
start_server "start_frontend.sh"

echo "Both servers should be starting in new terminal windows."
echo "Backend will be available at: http://localhost:8000"
echo "Frontend will be available at: http://localhost:3000" 
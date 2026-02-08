#!/bin/bash

# Start server script with proper Python path
# This ensures the app module can be found

# Get the directory of this script
BACKEND_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$BACKEND_DIR")"

# Activate virtual environment
source "$PROJECT_DIR/venv/bin/activate"

# Set PYTHONPATH to include backend directory
export PYTHONPATH="$BACKEND_DIR:$PYTHONPATH"

# Load environment variables
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
fi

# Start uvicorn
cd "$BACKEND_DIR"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

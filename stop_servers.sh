#!/bin/bash

# Stop Servers Script for Multi-Agent Document Intelligence System

echo "================================================"
echo "Stopping Multi-Agent Document Intelligence System"
echo "================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Stop backend
if [ -f "$SCRIPT_DIR/.backend.pid" ]; then
    BACKEND_PID=$(cat "$SCRIPT_DIR/.backend.pid")
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "🛑 Stopping backend (PID: $BACKEND_PID)..."
        kill $BACKEND_PID
        echo "✅ Backend stopped"
    else
        echo "ℹ️  Backend already stopped"
    fi
    rm "$SCRIPT_DIR/.backend.pid"
else
    echo "ℹ️  No backend PID file found"
fi

echo ""

# Stop frontend
if [ -f "$SCRIPT_DIR/.frontend.pid" ]; then
    FRONTEND_PID=$(cat "$SCRIPT_DIR/.frontend.pid")
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "🛑 Stopping frontend (PID: $FRONTEND_PID)..."
        kill $FRONTEND_PID
        echo "✅ Frontend stopped"
    else
        echo "ℹ️  Frontend already stopped"
    fi
    rm "$SCRIPT_DIR/.frontend.pid"
else
    echo "ℹ️  No frontend PID file found"
fi

echo ""

# Also try to kill any process on ports 8000 and 3000
echo "🔍 Checking for processes on ports 8000 and 3000..."

# Check port 8000
if lsof -Pi :8000 -sTCP:LISTEN -t > /dev/null 2>&1; then
    echo "🛑 Killing process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
fi

# Check port 3000
if lsof -Pi :3000 -sTCP:LISTEN -t > /dev/null 2>&1; then
    echo "🛑 Killing process on port 3000..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null || true
fi

echo ""
echo "✅ All servers stopped"

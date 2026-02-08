#!/bin/bash

# Full Stack Startup Script for Multi-Agent Document Intelligence System

set -e

echo "================================================"
echo "Multi-Agent Document Intelligence System"
echo "Full Stack Startup"
echo "================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check if backend virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "❌ Error: Python virtual environment not found"
    echo "Please run the setup first:"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Check if frontend dependencies are installed
if [ ! -d "$SCRIPT_DIR/frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd "$SCRIPT_DIR/frontend"
    npm install
    cd "$SCRIPT_DIR"
    echo ""
fi

# Check environment files
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "❌ Error: Backend .env file not found"
    echo "Please create .env from .env.example and add your API keys"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/frontend/.env" ]; then
    echo "⚙️  Creating frontend .env file..."
    cp "$SCRIPT_DIR/frontend/.env.example" "$SCRIPT_DIR/frontend/.env"
    echo ""
fi

echo "================================================"
echo "Starting Backend Server..."
echo "================================================"
echo ""

# Start backend in background
cd "$SCRIPT_DIR/backend"
source ../venv/bin/activate
export PYTHONPATH=$PWD:$PYTHONPATH

# Start backend server in background
uvicorn app.main:app --reload --port 8000 > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   Logs: backend.log"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"
echo ""

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "✅ Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start. Check backend.log for details."
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

echo ""
echo "================================================"
echo "Starting Frontend Server..."
echo "================================================"
echo ""

# Start frontend in background
cd "$SCRIPT_DIR/frontend"
npm run dev > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   Logs: frontend.log"
echo ""

# Wait for frontend to be ready
echo "⏳ Waiting for frontend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend is ready!"
        break
    fi
    sleep 1
done

echo ""
echo "================================================"
echo "🚀 System Ready!"
echo "================================================"
echo ""
echo "Frontend: http://localhost:3000"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Logs:"
echo "  - Backend:  tail -f backend.log"
echo "  - Frontend: tail -f frontend.log"
echo ""
echo "To stop the system:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Or save PIDs to file for later:"
echo "  echo $BACKEND_PID > .backend.pid"
echo "  echo $FRONTEND_PID > .frontend.pid"
echo ""

# Save PIDs
echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"
echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"

echo "PIDs saved to .backend.pid and .frontend.pid"
echo ""
echo "Press Ctrl+C to stop both servers..."
echo ""

# Trap Ctrl+C to cleanup
trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Keep script running
wait

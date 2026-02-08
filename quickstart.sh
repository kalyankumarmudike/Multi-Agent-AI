#!/bin/bash

# Quick Start Script for Multi-Agent Document Intelligence System
# This script sets up and runs the system

set -e  # Exit on error

echo "🚀 Multi-Agent Document Intelligence System - Quick Start"
echo "=========================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.10+ required. Found: $python_version"
    exit 1
fi
echo "✓ Python version: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env and add your API key!"
    echo ""
    echo "Quick setup:"
    echo "1. Get a free API key from https://console.groq.com"
    echo "2. Open .env in a text editor"
    echo "3. Set GROQ_API_KEY=your_actual_key_here"
    echo ""
    read -p "Press Enter when you've added your API key to .env..."
fi

# Verify API key is set
source .env
if [ -z "$GROQ_API_KEY" ] && [ -z "$OPENAI_API_KEY" ] && [ -z "$OPENROUTER_API_KEY" ]; then
    echo "❌ No API key found in .env file"
    echo "Please set GROQ_API_KEY, OPENAI_API_KEY, or OPENROUTER_API_KEY"
    exit 1
fi

echo "✓ API key configured"
echo ""

# Start the server
echo "Starting FastAPI server..."
echo "=========================================================="
echo ""
echo "Server will start at: http://localhost:8000"
echo "Interactive docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================================="
echo ""

cd backend
uvicorn app.main:app --reload --port 8000

#!/bin/bash

# Frontend Startup Script for Multi-Agent Document Intelligence System

set -e

echo "================================================"
echo "Multi-Agent Document Intelligence - Frontend"
echo "================================================"
echo ""

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found"
    echo "Please run this script from the frontend directory"
    exit 1
fi

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Error: Node.js version must be 18 or higher"
    echo "Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js version: $(node -v)"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    echo ""
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
fi

# Display configuration
echo "🔧 Configuration:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo ""

# Check if backend is running
echo "🔍 Checking backend status..."
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Warning: Backend is not running on port 8000"
    echo "   Please start the backend first:"
    echo "   cd ../backend && ./start_server.sh"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "================================================"
echo "🚀 Starting Frontend Development Server..."
echo "================================================"
echo ""
echo "The app will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the development server
npm run dev

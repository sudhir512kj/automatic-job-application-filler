#!/bin/bash
# Activation script for Auto Form Filling Agent

echo "🚀 Activating Auto Form Filling Agent Environment..."

# Activate virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated"
echo "📦 Python version: $(python --version)"
echo "📍 Virtual environment: $VIRTUAL_ENV"

# Check if API keys are set
if [ -f "backend/.env" ]; then
    echo "🔑 Environment file found"
else
    echo "⚠️  Please configure API keys in backend/.env"
fi

echo ""
echo "🛠️  Available commands:"
echo "  Backend: cd backend && python main.py"
echo "  Frontend: cd frontend && npm start"
echo "  Deactivate: deactivate"